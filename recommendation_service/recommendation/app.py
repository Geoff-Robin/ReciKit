from mcp.server.fastmcp import FastMCP
import os
from async_lru import alru_cache
from groq import AsyncGroq
import json
from fastapi.routing import APIRouter
import logging
import sys

recommendation_route = APIRouter()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("mcp_server.log")],
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


logger.info("Initializing MCP Server for RecSys")
mcp_app = FastMCP("MCP Server for RecSys", stateless_http=True)


@recommendation_route.get("/mealplan/")
async def get_meal_plan(likes: str, dislikes: str):
    return await get_meal_plan_tool(likes, dislikes)

@mcp_app.tool()
async def get_recommendation_tool(likes: str, dislikes: str):
	from recommendation.recommendation_controller import get_recommendation

	logger.info(
		f"Tool 'get_recommendation' invoked with likes: '{likes}', dislikes: '{dislikes}'"
	)
	try:
		results = await get_recommendation(likes, dislikes)
		logger.info(f"Returning {len(results)} recommendations")
		return results
	except Exception as e:
		logger.error(f"Error in get_recommendation tool: {e}", exc_info=True)
		raise

# TODO: Gotta test this.
@alru_cache(maxsize=5)
@mcp_app.tool()
async def get_meal_plan_tool(likes: str, dislikes: str):
	from recommendation.recommendation_controller import get_recommendation
	from recommendation.models import WeeklyMealPlan
	import recommendation.prompts as prompts

	logger.info(
		f"Tool 'get_meal_plan' invoked with parameters: match- '{likes}', mismatch- '{dislikes}'"
	)
	try:
		search_results = await get_recommendation(likes, dislikes)
		filtered_results = []
		for result in search_results:
			filtered_results.append(
				{
					"title": result["title"],
					"directions": result["directions"],
					"ingredients": result["NER"],
				}
			)
		groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
		response = await groq_client.chat.completions.create(
			model="openai/gpt-oss-20b",
			messages=[
				{
					"role": "system",
					"content": prompts.SYSTEM_PROMPT,
				},
				{
					"role": "user",
					"content": f"Recipes DataFrame:\n{str(filtered_results)}\n\n\nDisclude Recipes with Ingredients: {dislikes}",
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
