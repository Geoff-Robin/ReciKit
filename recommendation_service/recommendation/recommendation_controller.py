from async_lru import alru_cache
from fastembed import TextEmbedding
import numpy as np
from main import get_mongo_client, get_qdrant_client
from bson import ObjectId


embedder = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


async def get_recommendation(inventory: str, likes: str, allergies: str):
    mongo_client = await get_mongo_client()
    qdrant_client = await get_qdrant_client()

    inventory_vec = next(embedder.embed(inventory))
    like_vec = next(embedder.embed(likes))
    allergies_vec = next(embedder.embed(allergies))

    result = await qdrant_client.query_points(
        collection_name="Recipes",
        query=inventory_vec,
        limit=40,
        with_vectors=True,
    )

    points = result.points
    for point in points:
        point.score = (point.score + cosine_similarity(like_vec, np.array(point.vector))) / 2
    points.sort(key=lambda x: x.score, reverse=True)
    
    for point in points:
        point.score = cosine_similarity(
            allergies_vec,
            np.array(point.vector)
        )
    points.sort(key=lambda x: x.score)

    out = []
    for p in points:
        rid = p.payload["_id"]
        recipe = await mongo_client.RecipeDB.Recipes.find_one({"_id": ObjectId(rid)})
        if not recipe:
            continue
        p.payload.update(
            {
                "title": recipe.get("title"),
                "ingredients": recipe.get("ingredients"),
                "directions": recipe.get("directions"),
                "NER": recipe.get("NER"),
            }
        )
        out.append(p.payload)

    return out
