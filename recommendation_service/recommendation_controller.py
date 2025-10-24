from async_lru import alru_cache
from qdrant_client import AsyncQdrantClient
from sentence_transformers import SentenceTransformer
import pandas as pd
import os


@alru_cache(maxsize=40)
async def get_recommendation(match: str):

    global qdrant_client 
    qdrant_client = AsyncQdrantClient(url=os.getenv("QDRANT_URL"),api_key=os.getenv("QDRANT_API_KEY"))
    embedder = SentenceTransformer(
        "./models/all-MiniLM-L6-v2", device="cpu", backend="openvino"
    )

    embedded_query = embedder.encode(match, normalize_embeddings=True)
    search_results = await qdrant_client.search(
        collection_name="recipes",
        query_vector=embedded_query,
        limit = 30
    )
    recommendations = [result.payload for result in search_results]
    return recommendations