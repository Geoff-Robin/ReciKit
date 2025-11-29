from async_lru import alru_cache
from sentence_transformers import SentenceTransformer
import numpy as np
from main import get_mongo_client, get_qdrant_client
from bson import ObjectId

# load once
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


@alru_cache(maxsize=40)
async def get_recommendation(likes: str, dislikes: str):
    mongo_client = await get_mongo_client()
    qdrant_client = await get_qdrant_client()

    like_vec = embedder.encode(likes, normalize_embeddings=True)
    dislike_vec = embedder.encode(dislikes, normalize_embeddings=True)

    result = await qdrant_client.query_points(
        collection_name="Recipes",
        query=like_vec,
        limit=30,
        with_vectors=True,
    )

    points = result.points

    for point in points:
        point.score -= cosine_similarity(
            dislike_vec,
            np.array(point.vector)
        )

    points.sort(key=lambda x: x.score, reverse=True)

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
