from fastapi import APIRouter, HTTPException, Depends, Request
from dotenv import load_dotenv
from Routes.auth_routes import current_user, get_optional_current_user
from typing import Tuple, Dict, Any, List
from typing import Tuple, Dict, Any, List
from langchain_core.messages import HumanMessage
import requests
import os

load_dotenv()
routes = APIRouter()


@routes.post("/chats")
async def chat_endpoint(request: Request, payload: dict, user: str = Depends(get_optional_current_user)):
    try:
        user_input = payload.get("message")
        
        # If no user logged in, default to "Guest"
        username = user if user else "Guest"
        
        # Priority: Payload thread_id > User ID based > Guest ID default
        thread_id = payload.get("thread_id")
        if not thread_id:
             thread_id = f"user_{username}" if user else "guest_session"

        if not user_input:
             raise HTTPException(status_code=400, detail="Message is required")

        bot = request.app.state.chatbot
        
        config = {"configurable": {"thread_id": thread_id}}
        inputs = {
            "messages": [HumanMessage(content=user_input)],
            "username": username,
            "user_id": username # simple mapping
        }
        
        # We need to get the last message. We can invoke or stream.
        # Simple invoke is safer for basic request/response.
        result = await bot.ainvoke(inputs, config=config)
        last_msg = result["messages"][-1]
        
        return {"response": last_msg.content}
    except Exception as e:
        print(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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
        else:
            likes = u.get("likes", "")
            allergies = u.get("allergies", "")
            inventory_list = u.get("inventory", [])
            if not isinstance(inventory_list, list):
                inventory_list = []
                
            inventory_str = ", ".join(
                f"{item.get('ingredient_name') or item.get('name', 'Unknown')} {item.get('quantity', '')} {item.get('unit') or item.get('metric', '')}"
                for item in inventory_list
                if isinstance(item, dict) and (item.get('ingredient_name') or item.get('name'))
            )
            result = requests.get(
                os.getenv("RECOMMENDATION_SERVICE_URL") + "/api/mealplan/",
                params={
                    "inventory": inventory_str,
                    "likes": likes,
                    "allergies": allergies,
                },
            )
            await users.update_one(
                {"username": user}, {"$set": {"mealPlan": result.json()}}
            )
            return result.json()

    except Exception as e:
        if isinstance(e, requests.exceptions.RequestException):
            raise HTTPException(status_code=result.status_code, detail=result.text)
        raise HTTPException(status_code=500, detail=str(e))
