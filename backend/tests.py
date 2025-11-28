import pytest
from unittest.mock import AsyncMock, patch
from langchain.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
load_dotenv()

from Agent import chatbot_app


@pytest.mark.asyncio
async def test_menu_option_1():
    state = {"messages": [HumanMessage(content="1")]}
    with patch("Agent.chatbot.MultiServerMCPClient") as mc, \
         patch("Agent.chatbot.create_agent"):
        mc.return_value.get_tools = AsyncMock(return_value=[])
        result = await chatbot_app.ainvoke(state)

    msg = result["messages"][-1]
    assert isinstance(msg, AIMessage)
    assert "record your inventory" in msg.content


@pytest.mark.asyncio
async def test_menu_option_2():
    state = {"messages": [HumanMessage(content="2")]}
    with patch("Agent.chatbot.MultiServerMCPClient") as mc, \
         patch("Agent.chatbot.create_agent"):
        mc.return_value.get_tools = AsyncMock(return_value=[])
        result = await chatbot_app.ainvoke(state)

    msg = result["messages"][-1]
    assert "provide a recipe" in msg.content


@pytest.mark.asyncio
async def test_menu_option_3():
    state = {"messages": [HumanMessage(content="3")]}
    with patch("Agent.chatbot.MultiServerMCPClient") as mc, \
         patch("Agent.chatbot.create_agent"):
        mc.return_value.get_tools = AsyncMock(return_value=[])
        result = await chatbot_app.ainvoke(state)

    msg = result["messages"][-1]
    assert "preferences" in msg.content


@pytest.mark.asyncio
async def test_menu_option_4():
    state = {"messages": [HumanMessage(content="4")]}
    with patch("Agent.chatbot.MultiServerMCPClient") as mc, \
         patch("Agent.chatbot.create_agent"):
        mc.return_value.get_tools = AsyncMock(return_value=[])
        result = await chatbot_app.ainvoke(state)

    msg = result["messages"][-1]
    assert "manage your profile" in msg.content


@pytest.mark.asyncio
async def test_initial_greeting():
    state = {"messages": [HumanMessage(content="hi")]}
    with patch("Agent.chatbot.MultiServerMCPClient") as mc, \
         patch("Agent.chatbot.create_agent"):
        mc.return_value.get_tools = AsyncMock(return_value=[])
        result = await chatbot_app.ainvoke(state)

    msg = result["messages"][-1]
    assert "What do you want to do today" in msg.content


@pytest.mark.asyncio
async def test_agent_invocation():
    state = {
        "messages": [
            HumanMessage(content="hello"),
            HumanMessage(content="test")
        ]
    }

    mock_agent = AsyncMock()
    mock_agent.ainvoke = AsyncMock(return_value=AIMessage(content="agent output"))

    with patch("Agent.chatbot.MultiServerMCPClient") as mc, \
         patch("Agent.chatbot.create_agent", return_value=mock_agent):
        mc.return_value.get_tools = AsyncMock(return_value=[])
        result = await chatbot_app.ainvoke(state)

    msg = result["messages"][-1]
    assert msg.content == "agent output"
    mock_agent.ainvoke.assert_called_once_with(state["messages"])


@pytest.mark.asyncio
async def test_menu_blocks_agent():
    state = {"messages": [HumanMessage(content="3")]}

    mock_agent = AsyncMock()
    mock_agent.ainvoke = AsyncMock()

    with patch("Agent.chatbot.MultiServerMCPClient") as mc, \
         patch("Agent.chatbot.create_agent", return_value=mock_agent):
        mc.return_value.get_tools = AsyncMock(return_value=[])
        result = await chatbot_app.ainvoke(state)

    msg = result["messages"][-1]
    assert "preferences" in msg.content
    mock_agent.ainvoke.assert_not_called()
