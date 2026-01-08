from async_lru import alru_cache
from fastembed import TextEmbedding
import numpy as np
from main import get_mongo_client, get_qdrant_client
from recommendation.logger import logger
from bson import ObjectId


embedder = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


async def get_recommendation(inventory: str, likes: str, allergies: str):
    mongo_client = await get_mongo_client()
    qdrant_client = await get_qdrant_client()

    logger.info(f"Generating embeddings for inventory, likes, and allergies")
    try:
        inventory_vec = next(embedder.embed(inventory)) if inventory else np.zeros(384)
        like_vec = next(embedder.embed(likes)) if likes else np.zeros(384)
        allergies_vec = next(embedder.embed(allergies)) if allergies else np.zeros(384)
    except Exception as e:
        logger.error(f"Embedding failed: {e}")
        raise

    result = await qdrant_client.query_points(
        collection_name="Recipes",
        query=inventory_vec,
        limit=40,
        with_vectors=True,
    )

    points = result.points
    for point in points:
        point.score = (
            point.score + cosine_similarity(like_vec, np.array(point.vector))
        ) / 2
    points.sort(key=lambda x: x.score, reverse=True)

    for point in points:
        point.score = cosine_similarity(allergies_vec, np.array(point.vector))
    points.sort(key=lambda x: x.score)

    out = []
    for p in points:
        try:
            rid = p.payload.get("_id")
            if not rid:
                continue
                
            recipe = await mongo_client.RecipeDB.Recipes.find_one({"_id": ObjectId(rid)})
            if not recipe:
                continue
            
            # Ensure fields are safe to join or process later
            ner = recipe.get("NER")
            if isinstance(ner, list):
                ner = ", ".join(str(n) for n in ner)
            elif not isinstance(ner, str):
                ner = str(ner) if ner else ""

            p.payload.update(
                {
                    "title": str(recipe.get("title", "Untitled")),
                    "ingredients": recipe.get("ingredients", []),
                    "directions": recipe.get("directions", []),
                    "NER": ner,
                }
            )
            out.append(p.payload)
        except Exception as e:
            logger.warning(f"Failed to process recipe {rid}: {e}")
            continue

    return out
