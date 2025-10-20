from mcp.server.fastmcp import FastMCP
import lancedb
import os
from sentence_transformers import SentenceTransformer
from groq import AsyncGroq
from dotenv import load_dotenv
from models import WeeklyMealPlan
import prompts
import pandas as pd
import json
import logging
from async_lru import alru_cache
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("mcp_server.log")],
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


load_dotenv()

logger.info("Initializing MCP Server for RecSys")
mcp = FastMCP("MCP Server for RecSys")


@alru_cache(maxsize=40)
async def get_recommendation_controller(match: str) -> pd.DataFrame:
    # TODO: Disclude is to disclude recipes and match is to match recipes, imma work on that using lancedb real quick
    logger.info(f"get_recommendation_controller called with match: '{match}'")
    try:
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
    except Exception as e:
        logger.error(f"Error in get_recommendation_controller: {e}", exc_info=True)
        raise
    return results


@mcp.tool()
async def get_recommendation(match: str):
    logger.info(f"Tool 'get_recommendation' invoked with match: '{match}'")
    try:
        results = await get_recommendation_controller(match)
        logger.info(f"Returning {len(results)} recommendations")
        return results
    except Exception as e:
        logger.error(f"Error in get_recommendation tool: {e}", exc_info=True)
        raise


@mcp.tool()
async def get_meal_plan(match: str):
    logger.info(f"Tool 'get_meal_plan' invoked with match: '{match}'")
    try:
        search_results = await get_recommendation_controller(match)
        client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        response = await client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": prompts.SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": f"Recipes DataFrame:\n{search_results.to_string(index=False)}",
                },
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "weekly_meal_plan",
                    "schema": WeeklyMealPlan.model_json_schema(),
                },
            },
        )
        raw_content = response.choices[0].message.content
        meal_plan_json = json.loads(raw_content)
        return meal_plan_json
    except Exception as e:
        logger.error(f"Error in get_meal_plan tool: {e}", exc_info=True)
        raise


async def main():
    await mcp.run_streamable_http_async()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
