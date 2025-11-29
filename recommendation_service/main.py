from fastapi import FastAPI
from fastapi.logger import logger
import contextlib
from recommendation import mcp_app, recommendation_route
from pymongo import AsyncMongoClient
from qdrant_client import AsyncQdrantClient
from dotenv import load_dotenv
import os

load_dotenv()

qdrant_client = AsyncQdrantClient(url = os.getenv("QDRANT_URI"), api_key=os.getenv("QDRANT_API_KEY"))
mongo_client = AsyncMongoClient(os.getenv("MONGO_DB_URI"))

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp_app.session_manager.run())
        yield
        await mongo_client.close()
        await qdrant_client.close()
        
async def get_mongo_client() -> AsyncMongoClient:
    global mongo_client
    return mongo_client

async def get_qdrant_client() -> AsyncQdrantClient:
    global qdrant_client
    return qdrant_client

fast_api_app = FastAPI(lifespan=lifespan)
fast_api_app.mount("/mcp", mcp_app.streamable_http_app())
fast_api_app.include_router(recommendation_route, prefix="/api")
PORT = os.getenv("PORT", "3000")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(fast_api_app, host="0.0.0.0", port=int(PORT))
