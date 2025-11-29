from recommendation.recommendation_controller import get_recommendation
import pytest
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="function", autouse=True)
def env_vars(monkeypatch):
    monkeypatch.setenv("MONGO_DB_URI", os.getenv("MONGO_DB_URI"))
    monkeypatch.setenv("QDRANT_URI", os.getenv("QDRANT_URI"))
    monkeypatch.setenv("QDRANT_API_KEY", os.getenv("QDRANT_API_KEY"))
    return None


@pytest.mark.asyncio
async def test_get_recommendation_logging(caplog):
    caplog.set_level(logging.DEBUG)
    logger.debug("Starting test_get_recommendation_logging")
    likes = "chicken salad"
    dislikes = "spicy"
    recommendations = await get_recommendation(likes, dislikes)
    logger.debug(f"Recommendations received: {recommendations}")
    assert isinstance(recommendations, list), "Should return a list"
    for rec in recommendations:
        assert "title" in rec, f"Missing title in {rec}"
        assert "ingredients" in rec, f"Missing ingredients in {rec}"
        assert "directions" in rec, f"Missing directions in {rec}"
        assert "NER" in rec, f"Missing NER in {rec}"
    logger.debug("Completed test_get_recommendation_logging")
