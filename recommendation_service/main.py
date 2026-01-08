from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback
import contextlib
from recommendation import mcp_app, get_meal_plan
from pymongo import AsyncMongoClient
from qdrant_client import AsyncQdrantClient
from dotenv import load_dotenv
import os

load_dotenv()

qdrant_client = AsyncQdrantClient(
    url=os.getenv("QDRANT_URI"), api_key=os.getenv("QDRANT_API_KEY")
)
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

@fast_api_app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_msg = f"Unhandled error: {str(exc)}\n{traceback.format_exc()}"
    from recommendation.logger import logger
    logger.error(error_msg)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)},
    )


@fast_api_app.get("/health")
async def health_check():
    return {"status": "ok"}


@fast_api_app.get("/api/mealplan/")
async def get_meal_plan_endpoint(inventory: str, likes: str, allergies: str):
    return await get_meal_plan(inventory, likes, allergies)


fast_api_app.mount("/", mcp_app.streamable_http_app())

if __name__ == "__main__":
    import uvicorn

    PORT = os.getenv("PORT", "8000")
    HOST = "0.0.0.0" if os.getenv("ENV") == "production" else "127.0.0.1"
    uvicorn.run(fast_api_app, host=HOST, port=int(PORT))
