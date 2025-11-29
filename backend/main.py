from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.logger import logger
import contextlib
from pymongo import AsyncMongoClient
from Routes.auth_routes import auth
from Routes.routes import routes
import os

load_dotenv()

mongo_client = AsyncMongoClient(os.getenv("MONGO_DB_URI"))


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    yield
    logger.info("Shutting down...")
    await mongo_client.close()

async def get_mongo_client() -> AsyncMongoClient:
    global mongo_client
    return mongo_client

app = FastAPI(lifespan=lifespan)

from Routes.auth_routes import auth
from Routes.routes import routes
app.include_router(auth, prefix="/api/auth")
app.include_router(routes, prefix="/api")

PORT = os.getenv("PORT", "3000")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=int(PORT))
