from fastapi import FastAPI
import contextlib
from recommendation import mcp_app, recommendation_route
from pymongo import AsyncMongoClient
import os


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp_app.session_manager.run())
        app.state.mongo_client = AsyncMongoClient(os.getenv("MONGO_DB_URI"))
        yield
        
async def get_mongo_client() -> AsyncMongoClient:
    return fast_api_app.state.mongo_client


fast_api_app = FastAPI(lifespan=lifespan)
fast_api_app.mount("/", mcp_app.streamable_http_app(), name="mcp")
fast_api_app.mount("/api", recommendation_route)
PORT = os.getenv("PORT", "3000")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(fast_api_app, host="0.0.0.0", port=int(PORT))
