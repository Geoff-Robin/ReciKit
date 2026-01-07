from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
import contextlib
from pymongo import AsyncMongoClient
from Routes.auth_routes import auth
from Routes.routes import routes
import os
from Agent.chatbot import ChatbotApp

load_dotenv()

mongo_client = AsyncMongoClient(os.getenv("MONGO_DB_URI"))


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    app.state.chatbot = ChatbotApp()
    try:
        await app.state.chatbot.initialize()
        logger.info("Chatbot initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize chatbot: {e}")
    
    yield
    logger.info("Shutting down...")
    await mongo_client.close()


async def get_mongo_client() -> AsyncMongoClient:
    global mongo_client
    return mongo_client


app = FastAPI(lifespan=lifespan)

app.include_router(auth, prefix="/api/auth")
app.include_router(routes, prefix="/api")

# CORS Configuration
origins = ["http://localhost:5173", "https://reci-kit.vercel.app"]
env_origins = os.getenv("ALLOWED_ORIGINS")
if env_origins:
    origins.extend([o.strip() for o in env_origins.split(",")])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

if __name__ == "__main__":
    import uvicorn

    PORT = os.getenv("PORT", "3000")
    host = "127.0.0.1" if os.getenv("ENV") == "development" else "0.0.0.0"
    uvicorn.run(app, host=host, port=int(PORT))
