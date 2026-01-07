from fastapi import APIRouter, HTTPException, Depends
from dotenv import load_dotenv
# from groq import AsyncGroq
# from Agent.chatbot import chatbot
# from Agent.models import Message
from Routes.auth_routes import current_user
from typing import Tuple, Dict, Any
import requests
import os

load_dotenv()
routes = APIRouter()

async def meal_plan_exists(username: str) -> Tuple[bool, Dict[str, Any]]:
    try:
        from main import get_mongo_client
        mongo_client = await get_mongo_client()
        users = mongo_client["RecipeDB"]["Users"]

        user = await users.find_one({
            "username": username,
            "mealPlan": {"$exists": True}
        })

        if not user or "mealPlan" not in user:
            return False, {"message": "none"}

        return True, user["mealPlan"]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))         

@routes.post("/chats")
async def chat_endpoint(state: dict, user: str = Depends(current_user)):
    pass

@routes.get("/recommendations")
async def get_recommendations(user: str = Depends(current_user)):
    try:
        from main import get_mongo_client
        mongo_client = await get_mongo_client()
        db = mongo_client["RecipeDB"]
        users = db.Users
        u = await users.find_one({"username": user})
        if not u:
            raise HTTPException(status_code=404, detail="User not found")
        check, meal_plan = await meal_plan_exists(username=user) 
        if check:
            return meal_plan
        else: 
            likes = u.get("likes", "")
            allergies = u.get("allergies", "")
            inventory_list = u.get("inventory", "")
            inventory_str = ", ".join(
                f"{item['ingredient_name']} {item['quantity']} {item['unit']}"
                for item in inventory_list
            )
            result = requests.get(
                os.getenv("RECOMMENDATION_SERVICE_URL")+"/api/mealplan/",params={
                    "inventory": inventory_str,
                    "likes": likes,
                    "allergies": allergies
                }
            )
            await users.update_one(
                {"username": user},
                {"$set":{"mealPlan": result.json()}}
            )
            return result.json()

    except Exception as e:
        if isinstance(e, requests.exceptions.RequestException):
            raise HTTPException(status_code=result.status_code, detail= result.text)
        raise HTTPException(status_code=500, detail=str(e))