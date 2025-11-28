from fastapi import FastAPI
from fastapi.logger import logger
import contextlib
from pymongo import AsyncMongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_client = AsyncMongoClient(os.getenv("MONGO_DB_URI"))


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    yield
    logger.info("Shutting down...")
    mongo_client.close()

async def get_mongo_client() -> AsyncMongoClient:
    global mongo_client
    return mongo_client

app = FastAPI(lifespan=lifespan)

PORT = os.getenv("PORT", "3000")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(PORT))
