from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct
import os
from typing import List
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pandas import DataFrame
import pandas as pd
import ast
import math
from tqdm import tqdm


load_dotenv()

def convert(v):
    if isinstance(v, list):
        return v
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return []
    return ast.literal_eval(str(v))

def load_and_process_data(file_path: str) -> DataFrame:
    df = pd.read_csv(file_path)
    columns = ["ingredients", "NER", "directions"]
    for col in columns:
        df[col] = df[col].apply(convert)
    return df

async def get_points(model: SentenceTransformer, df: DataFrame)-> List[PointStruct]:
    points=[]
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Generating embeddings"):
        embedding = model.encode(row["title"]+" ".join(row["NER"]), normalize_embeddings=True)
        embedding_list = embedding.tolist()
        point = PointStruct(
            id=index,
            vector=embedding_list,
            payload={
                "_id": row["_id"],
            },
        )
        points.append(point)
    return points

async def get_embedding_model():
    providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
    provider_options = [
        {"device_id": 0, "gpu_mem_limit": "0"},
        {}
    ]

    model = SentenceTransformer(
        "models/all-MiniLM-L6-v2",
        backend="onnx",
        model_kwargs={
            "file_name": "model.onnx",
            "providers": providers,
            "provider_options": provider_options,
        },
    )
    return model

async def main():
    model = await get_embedding_model()
    qdrant_client = AsyncQdrantClient(
        url=os.getenv("QDRANT_URI"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )
    collection_exists = await qdrant_client.collection_exists(collection_name="Recipes")
    if collection_exists:
        await qdrant_client.delete_collection(collection_name="Recipes")
        await qdrant_client.create_collection(
            collection_name="Recipes",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
    else:
        await qdrant_client.create_collection(
            collection_name="Recipes",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
    df = load_and_process_data(r"datasets//RecipeDB.Recipes.csv")
    points = await get_points(model, df)
    batch = 100
    for i in tqdm(range(0, len(points), batch),desc="Uploading points to Qdrant"):
        await qdrant_client.upsert(
            collection_name="Recipes",
            points=points[i:i + batch],
        )
    
        

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())