from async_lru import alru_cache
from qdrant_client import AsyncQdrantClient
from sentence_transformers import SentenceTransformer
import numpy as np
import os
from main import get_mongo_client
from pymongo import AsyncMongoClient
from bson import ObjectId


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


@alru_cache(maxsize=40)
async def get_recommendation(likes: str, dislikes: str):
    global qdrant_client
    global a_mongo
    a_mongo = await get_mongo_client()
    qdrant_client = AsyncQdrantClient(
        url=os.getenv("QDRANT_URI"), api_key=os.getenv("QDRANT_API_KEY")
    )
    model_name = (
        "all-MiniLM-L6-v2"
        if os.getenv("ENV") == "production"
        else r"models/all-MiniLM-L6-v2"
    )
    embedder = SentenceTransformer(model_name, device="cpu", backend="onnx")

    embedded_query_likes = embedder.encode(likes, normalize_embeddings=True)
    embedded_query_dislikes = embedder.encode(dislikes, normalize_embeddings=True)
    result = await qdrant_client.query_points(
        collection_name="Recipes",
        query=embedded_query_likes,
        limit=30,
        with_vectors=True,
    )
    points = result.points
    for point in points:
        point.score -= cosine_similarity(
            embedded_query_dislikes, np.array(point.vector)
        )

    search_results_likes = sorted(points, key=lambda x: x.score, reverse=True)
    for i in range(len(search_results_likes)):
        recipe_id = search_results_likes[i].payload["_id"]
        recipe = await a_mongo.RecipeDB.Recipes.find_one({"_id": ObjectId(recipe_id)})
        if recipe is None:
            continue
        search_results_likes[i].payload.update(
            {
                "title": recipe.get("title"),
                "ingredients": recipe.get("ingredients"),
                "directions": recipe.get("directions"),
                "NER": recipe.get("NER"),
            }
        )
    recommendations = [result.payload for result in search_results_likes]
    return recommendations
