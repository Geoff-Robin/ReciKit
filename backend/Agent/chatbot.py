import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState
from menu_handler import handle_menu

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

def chatbot_node(state: MessagesState):
    last_message = state["messages"][-1].content
    menu_reply = handle_menu(last_message, state["messages"])

    if menu_reply:
        return {"messages": state["messages"] + [menu_reply]}
    
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

graph = StateGraph(MessagesState)
graph.add_node("chatbot", chatbot_node)
graph.set_entry_point("chatbot")
chatbot_app = graph.compile()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    messages: List[Message]

@app.post("/chat")
async def chat_endpoint(conversation: Conversation):
    # Convert incoming messages to HumanMessage objects for the agent
    state = {"messages": [HumanMessage(content=msg.content) for msg in conversation.messages]}
    # Invoke the chatbot
    new_state = chatbot_app.invoke(state)
    # Return only the latest bot reply
    return {"reply": new_state["messages"][-1].content}
