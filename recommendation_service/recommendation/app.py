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
stateless_http_flag = True if not os.environ.get("STDIO_TRANSPORT") == "true" else False
mcp_app = FastMCP("MCP Server for RecSys", stateless_http=stateless_http_flag)


def parse_directions(directions: str | List[str]):
    if not directions:
        return []
    if isinstance(directions, list):
        return directions
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
        logger.info("Calling get_recommendation...")
        search_results = await get_recommendation(inventory, likes, allergies)
        logger.info(f"Search results found: {len(search_results)}")
        
        filtered_results = []
        for result in search_results:
            directions_list = parse_directions(result.get("directions", []))
            # Ensure all elements are strings before joining
            directions = "\n".join(str(d) for d in directions_list if d)
            filtered_results.append(
                {
                    "title": result.get("title", "Untitled"),
                    "directions": directions,
                    "ingredients": result.get("NER", ""),
                }
            )
        
        logger.info("Sending request to Groq for meal plan...")
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
        try:
            meal_plan_json = json.loads(raw_content)
            return meal_plan_json
        except json.JSONDecodeError as e:
            logger.error(f"Groq returned invalid JSON: {raw_content[:500]}...")
            raise HTTPException(status_code=500, detail="LLM returned invalid meal plan format")
    except Exception as e:
        logger.error(f"Error in get_meal_plan tool: {e}", exc_info=True)
        raise


@mcp_app.tool()
async def get_meal_plan_tool(inventory: str, likes: str, allergies: str):
    return await get_meal_plan(inventory, likes, allergies)


@mcp_app.tool()
async def add_item_to_inventory(ingredients: List[Ingredient], username: str):
    from main import get_mongo_client

    logger.info(
        f"Tool 'add_item_to_inventory' invoked (ingredients: {ingredients}, username: {username})"
    )
    mongo_client = await get_mongo_client()
    try:
        await mongo_client["RecipeDB"]["Users"].update_one(
            {"username": username},
            {
                "$push": {
                    "inventory": {
                        "$each": [ingredient.model_dump() for ingredient in ingredients]
                    }
                }
            },
        )
    except Exception as e:
        logger.info(f"Error in add_item_to_inventory tool: {e}", exc_info=True)
        return {"error": "Failed to add item to inventory"}


@mcp_app.tool()
async def get_user_inventory(username: str):
    """
    Fetch the user's current inventory.
    """
    from main import get_mongo_client

    logger.info(f"Tool 'get_user_inventory' invoked (username: {username})")
    mongo_client = await get_mongo_client()
    user = await mongo_client["RecipeDB"]["Users"].find_one({"username": username})
    if not user:
        return {"error": "User not found"}
    return {
        "username": user.get("username"),
        "inventory": user.get("inventory", []),
    }


@mcp_app.tool()
async def get_user_interests(username: str):
    """
    Fetch the user's likes, dislikes, and allergies.
    """
    from main import get_mongo_client

    logger.info(f"Tool 'get_user_interests' invoked (username: {username})")
    mongo_client = await get_mongo_client()
    user = await mongo_client["RecipeDB"]["Users"].find_one({"username": username})
    if not user:
        return {"error": "User not found"}
    return {
        "username": user.get("username"),
        "likes": user.get("likes", ""),
        "dislikes": user.get("dislikes", ""),
        "allergies": user.get("allergies", ""),
    }


@mcp_app.tool()
async def get_user_meal_plan(username: str):
    """
    Fetch the user's current meal plan.
    """
    from main import get_mongo_client

    logger.info(f"Tool 'get_user_meal_plan' invoked (username: {username})")
    mongo_client = await get_mongo_client()
    user = await mongo_client["RecipeDB"]["Users"].find_one({"username": username})
    if not user:
        return {"error": "User not found"}
    return {
        "username": user.get("username"),
        "mealPlan": user.get("mealPlan", {}),
    }


@mcp_app.tool()
async def update_preferences(username: str, likes: str = "", dislikes: str = "", allergies: str = ""):
    from main import get_mongo_client

    logger.info(
        f"Tool 'update_preferences' invoked (username: {username}, likes: {likes}, dislikes: {dislikes}, allergies: {allergies})"
    )
    mongo_client = await get_mongo_client()
    try:
        update_fields = {"likes": likes, "dislikes": dislikes, "allergies": allergies}
        # Filter out empty strings if we want to avoid overwriting with empty? 
        # The previous behavior was to overwrite. If the user sends nothing, it defaults to empty string.
        # But if the tool call is intended to be a partial update, this is bad.
        # However, the previous signature required them, so it was always a full update (or required values).
        # To fix the "missing field" error, defaults are needed.
        
        await mongo_client["RecipeDB"]["Users"].update_one(
            {"username": username}, {"$set": update_fields}
        )
    except Exception as e:
        logger.info(f"Error in update_preferences tool: {e}", exc_info=True)
        return {"error": "Failed to update preferences"}


@mcp_app.tool()
async def add_like(username: str, like: str):
    from main import get_mongo_client
    mongo_client = await get_mongo_client()
    user = await mongo_client["RecipeDB"]["Users"].find_one({"username": username})
    if not user:
        return {"error": "User not found"}
    
    current_likes = user.get("likes", "")
    if current_likes:
        # Check if already exists to avoid duplicates
        likes_list = [l.strip() for l in current_likes.split(",")]
        if like not in likes_list:
            new_likes = current_likes + ", " + like
        else:
            new_likes = current_likes
    else:
        new_likes = like
        
    await mongo_client["RecipeDB"]["Users"].update_one(
        {"username": username},
        {"$set": {"likes": new_likes}}
    )
    return {"status": "success", "likes": new_likes}


@mcp_app.tool()
async def remove_like(username: str, like: str):
    from main import get_mongo_client
    mongo_client = await get_mongo_client()
    user = await mongo_client["RecipeDB"]["Users"].find_one({"username": username})
    if not user:
        return {"error": "User not found"}
    
    current_likes = user.get("likes", "")
    if not current_likes:
        return {"status": "success", "likes": ""}
        
    likes_list = [l.strip() for l in current_likes.split(",")]
    if like in likes_list:
        likes_list.remove(like)
        
    new_likes = ", ".join(likes_list)
    
    await mongo_client["RecipeDB"]["Users"].update_one(
        {"username": username},
        {"$set": {"likes": new_likes}}
    )
    return {"status": "success", "likes": new_likes}


@mcp_app.tool()
async def add_dislike(username: str, dislike: str):
    from main import get_mongo_client
    mongo_client = await get_mongo_client()
    user = await mongo_client["RecipeDB"]["Users"].find_one({"username": username})
    if not user:
        return {"error": "User not found"}
    
    current_dislikes = user.get("dislikes", "")
    if current_dislikes:
        dislikes_list = [d.strip() for d in current_dislikes.split(",")]
        if dislike not in dislikes_list:
            new_dislikes = current_dislikes + ", " + dislike
        else:
            new_dislikes = current_dislikes
    else:
        new_dislikes = dislike
        
    await mongo_client["RecipeDB"]["Users"].update_one(
        {"username": username},
        {"$set": {"dislikes": new_dislikes}}
    )
    return {"status": "success", "dislikes": new_dislikes}


@mcp_app.tool()
async def remove_dislike(username: str, dislike: str):
    from main import get_mongo_client
    mongo_client = await get_mongo_client()
    user = await mongo_client["RecipeDB"]["Users"].find_one({"username": username})
    if not user:
        return {"error": "User not found"}
    
    current_dislikes = user.get("dislikes", "")
    if not current_dislikes:
        return {"status": "success", "dislikes": ""}
        
    dislikes_list = [d.strip() for d in current_dislikes.split(",")]
    if dislike in dislikes_list:
        dislikes_list.remove(dislike)
        
    new_dislikes = ", ".join(dislikes_list)
    
    await mongo_client["RecipeDB"]["Users"].update_one(
        {"username": username},
        {"$set": {"dislikes": new_dislikes}}
    )
    return {"status": "success", "dislikes": new_dislikes}


@mcp_app.tool()
async def add_allergy(username: str, allergy: str):
    from main import get_mongo_client
    mongo_client = await get_mongo_client()
    user = await mongo_client["RecipeDB"]["Users"].find_one({"username": username})
    if not user:
        return {"error": "User not found"}
    
    current_allergies = user.get("allergies", "")
    if current_allergies:
        allergies_list = [a.strip() for a in current_allergies.split(",")]
        if allergy not in allergies_list:
            new_allergies = current_allergies + ", " + allergy
        else:
            new_allergies = current_allergies
    else:
        new_allergies = allergy
        
    await mongo_client["RecipeDB"]["Users"].update_one(
        {"username": username},
        {"$set": {"allergies": new_allergies}}
    )
    return {"status": "success", "allergies": new_allergies}


@mcp_app.tool()
async def remove_allergy(username: str, allergy: str):
    from main import get_mongo_client
    mongo_client = await get_mongo_client()
    user = await mongo_client["RecipeDB"]["Users"].find_one({"username": username})
    if not user:
        return {"error": "User not found"}
    
    current_allergies = user.get("allergies", "")
    if not current_allergies:
        return {"status": "success", "allergies": ""}
        
    allergies_list = [a.strip() for a in current_allergies.split(",")]
    if allergy in allergies_list:
        allergies_list.remove(allergy)
        
    new_allergies = ", ".join(allergies_list)
    
    await mongo_client["RecipeDB"]["Users"].update_one(
        {"username": username},
        {"$set": {"allergies": new_allergies}}
    )
    return {"status": "success", "allergies": new_allergies}
