from mcp.server.fastmcp import FastMCP
import os
from typing import List
from recommendation.models import Ingredient
from async_lru import alru_cache
from groq import AsyncGroq
import json
import ast
from fastapi.routing import APIRouter
from recommendation.logger import logger

recommendation_route = APIRouter()
logger.info("Initializing MCP Server for RecSys")
stateless_http_flag = True if not os.environ.get("STDIO_TRANSPORT") == 'true' else False
mcp_app = FastMCP("MCP Server for RecSys", stateless_http=stateless_http_flag)


@mcp_app.tool()
async def get_recommendation_tool(likes: str, dislikes: str):
	from recommendation.recommendation_controller import get_recommendation

	logger.info(f"Tool 'get_recommendation' invoked (likes: {likes}, dislikes: {dislikes})")
	try:
		results = await get_recommendation(likes, dislikes)
		logger.info(f"Returning {len(results)} recommendations")
		return results
	except Exception as e:
		logger.error(f"Error in get_recommendation tool: {e}", exc_info=True)
		raise

def parse_directions(directions: str):
    try:
        return ast.literal_eval(directions)
    except (ValueError, SyntaxError):
        try:
            return json.loads(directions)
        except json.JSONDecodeError:
             logger.warning(f"Failed to parse directions: {directions}")
             return []

@alru_cache(maxsize=20)
async def get_meal_plan(inventory: str, likes: str, allergies: str):
	from recommendation.recommendation_controller import get_recommendation
	from recommendation.models import WeeklyMealPlan
	import recommendation.prompts as prompts

	logger.info(f"Tool 'get_meal_plan' invoked (inventory size: {len(inventory)})")
	try:
		search_results = await get_recommendation(inventory, likes, allergies)
		filtered_results = []
		for result in search_results:
			directions_list = parse_directions(result["directions"])
			directions = "\n".join(directions_list)
			filtered_results.append(
				{
					"title": result["title"],
					"directions": directions,
					"ingredients": result["NER"],
				}
			)
		groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
		response = await groq_client.chat.completions.create(
			model=os.getenv("MODEL_NAME"),
			messages=[
				{
					"role": "system",
					"content": prompts.SYSTEM_PROMPT,
				},
				{
					"role": "user",
					"content": f"Recipes DataFrame:\n{str(filtered_results)}\n\nUser Inventory: {inventory}\n\nDisclude Recipes with Ingredients: {allergies}",
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

@mcp_app.tool()
async def get_meal_plan_tool(inventory: str, likes: str, allergies: str):
    return await get_meal_plan(inventory,likes,allergies)

@mcp_app.tool()
async def add_item_to_inventory(ingredients: List[Ingredient], username: str):
    from main import get_mongo_client
    mongo_client = await get_mongo_client()
    await mongo_client["ReciKit"]["Users"].update_one(
        {"username": username},
        {
            "$push": {
                "inventory": {
                    "$each": [ingredient.model_dump() for ingredient in ingredients]
                }
            }
        }
    )

@mcp_app.tool()
async def get_user_profile(username: str):
    """
    Fetch the user's current inventory, likes, and allergies.
    """
    from main import get_mongo_client
    mongo_client = await get_mongo_client()
    user = await mongo_client["ReciKit"]["Users"].find_one({"username": username})
    if not user:
        return {"error": "User not found"}
    # Convert BSON types if necessary, though simple dict should work for MCP return
    return {
        "username": user.get("username"),
        "inventory": user.get("inventory", []),
        "likes": user.get("likes", ""),
        "allergies": user.get("allergies", ""),
        "mealPlan": user.get("mealPlan", "")
    }

@mcp_app.tool()
async def update_preferences(username: str, likes: str, allergies: str):
    from main import get_mongo_client
    mongo_client = await get_mongo_client()
    await mongo_client["ReciKit"]["Users"].update_one(
        {"username": username},
        {
            "$set": {
                "likes": likes,
                "allergies": allergies
            }
        }
    )