from fastapi import APIRouter, HTTPException, Depends
from dotenv import load_dotenv
from groq import AsyncGroq
from Agent.chatbot import chatbot
from Agent.models import Message
from Routes.auth_routes import current_user
import requests
import os

load_dotenv()
routes = APIRouter()

@routes.post("/chats")
async def chat_endpoint(state: dict, user: str = Depends(current_user)):
    try:
        global mongo_client
        reply = None
        if len(state.get("messages", [])) >= 10:
            groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
            completion = await groq_client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "system", "content": "Summarize the following conversation briefly to reduce context length."}] +
                         [{"role": m["role"], "content": m["content"]} for m in state["messages"]],
            )
            output = completion.choices[0].message.content
            reply = Message(role="assistant", content=output)
        state+={"messages": state.get("messages", []) + ([reply] if reply else [])}
        result = await chatbot.ainvoke(state)
        await mongo_client.RecipeDB.Chats.update_one(
            {"username": user},
            {
            "$push": {"conversation": {"$each": result["messages"]}}
            },
            upsert=True
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@routes.get("/recommendations")
async def get_recommendations(user: str = Depends(current_user)):
    try:
        global mongo_client
        db = mongo_client["RecipeDB"]
        users = db.Users
        u = await users.find_one({"username": user})
        if not u:
            raise HTTPException(status_code=404, detail="User not found")
        likes = u.get("likes", "")
        dislikes = u.get("dislikes", "")
        result = requests.post(
            os.getenv("RECOMMENDATION_SERVICE_URL")+"/api/recommendations",
            json={"likes": likes, "dislikes": dislikes}
        )
        return result.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))