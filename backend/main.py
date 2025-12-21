from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
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

app.include_router(auth, prefix="/api/auth")
app.include_router(routes, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials = True,
    allow_headers = ["*"],
    allow_methods = ["*"]
)

if __name__ == "__main__":
    import uvicorn
    PORT = os.getenv("PORT", "3000")
    host = "127.0.0.1" if os.getenv("ENV") else "0.0.0.0"
    uvicorn.run(app, host=host, port=int(PORT))
