from pydantic import BaseModel
from typing import List
from langgraph.graph import MessagesState


class Message(BaseModel):
    role: str
    content: str


class Conversation(BaseModel):
    messages: List[Message]


class ChatState(MessagesState):
    user_id: str
    username: str
