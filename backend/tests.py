from Agent import ChatbotApp
import pytest
from unittest.mock import AsyncMock, patch
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()


@pytest.mark.asyncio
async def test_chatbot_initialization():
    bot = ChatbotApp()
    with patch("Agent.chatbot.MultiServerMCPClient") as mc:
        mc.return_value.get_tools = AsyncMock(return_value=[])
        await bot.initialize()
        assert bot.graph is not None


@pytest.mark.asyncio
async def test_chatbot_response():
    bot = ChatbotApp()
    with (
        patch("Agent.chatbot.MultiServerMCPClient") as mc,
        patch("langchain_groq.ChatGroq.ainvoke") as mock_invoke,
    ):
        mc.return_value.get_tools = AsyncMock(return_value=[])
        mock_invoke.return_value = AIMessage(content="Hello! How can I help you?")

        await bot.initialize()
        config = {"configurable": {"thread_id": "test"}}
        state = {
            "messages": [HumanMessage(content="hi")],
            "username": "Jeff",
            "user_id": "1",
        }
        result = await bot.ainvoke(state, config=config)

        assert "messages" in result
        assert result["messages"][-1].content == "Hello! How can I help you?"
