import os
from langgraph.graph import StateGraph
from groq import AsyncGroq
from bson import ObjectId
from Agent.prompts import SYSTEM_PROMPT
from Agent.menu_handler import handle_menu
from Agent.models import Conversation, Message


async def chatbot_node(state: Conversation):
    last_msg_text = state.messages[-1].content
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

    menu_reply = handle_menu(last_msg_text, state.messages)
    if menu_reply:
        return {"messages": state.messages + [menu_reply]}

    system_msg = Message(role="system", content=SYSTEM_PROMPT)

    prompt = [
        {"role": system_msg.role, "content": system_msg.content}
    ] + [
        {"role": m.role, "content": m.content}
        for m in state.messages
    ]

    completion = await client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=prompt,
        tools=[
            {
                "type" : "mcp",
                "server_label" : "ReciKit-Tool-Server",
                "server_url" : os.getenv("RECOMMENDATION_SERVICE_URL")
            }
        ]
    )

    output = completion.choices[0].message.content
    reply = Message(role="assistant", content=output)
    return {"messages": state.messages + [reply]}

async def get_likes_dislikes(user_id: str):
    global mongo_client
    db = mongo_client["RecipeDB"]
    db.Users.find_one({"_id": ObjectId(user_id)})

graph = StateGraph(Conversation)
graph.add_node("chatbot", chatbot_node)
graph.set_entry_point("chatbot")
chatbot = graph.compile()