from async_lru import alru_cache
import lancedb
from sentence_transformers import SentenceTransformer
import pandas as pd


@alru_cache(maxsize=40)
async def get_recommendation(match: str) -> pd.DataFrame:

    vector_db = await lancedb.connect_async("lance_db")
    table = await vector_db.open_table("recipes")
    embedder = SentenceTransformer(
        "./models/all-MiniLM-L6-v2", device="cpu", backend="openvino"
    )

    embedded_query = embedder.encode(match, normalize_embeddings=True)
    search_results = (await table.search(embedded_query)).limit(30)

    results = await search_results.to_pandas()
    results = results[["title", "directions", "NER"]]
    results.rename(columns={"NER": "ingredients"}, inplace=True)
    return results