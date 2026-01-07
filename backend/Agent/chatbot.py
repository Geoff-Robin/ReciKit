import os
import asyncio
from typing import Annotated, TypedDict, List
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

from Agent.prompts import SYSTEM_PROMPT
from Agent.models import ChatState

load_dotenv()


class ChatbotApp:
    def __init__(self):
        self.mcp_settings = {
            "recommendation_service": {
                "transport": "http",
                "url": os.getenv("RECOMMENDATION_SERVICE_URL", "http://localhost:3000") + "/mcp",
            }
        }
        self.client = MultiServerMCPClient(self.mcp_settings)
        self.memory = MemorySaver()
        self.graph = None

    async def initialize(self):
        """
        Async initialization to fetch tools and compile the graph.
        """
        try:
            mcp_tools = await self.client.get_tools()
        except Exception as e:
            # Fallback or log error
            print(f"Warning: Could not connect to MCP servers: {e}")
            mcp_tools = []

        model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)

        # Bind tools to the model
        if mcp_tools:
            self.model_with_tools = model.bind_tools(mcp_tools)
        else:
            self.model_with_tools = model

        # Define the assistant node
        async def assistant(state: ChatState):
            system_msg = SystemMessage(
                content=SYSTEM_PROMPT.format(username=state.get("username", "User"))
            )

            # Sanitize messages for Groq compatibility
            processed_messages = []
            for m in state["messages"]:
                if isinstance(m, ToolMessage):
                    content = m.content
                    if not content:
                        content = "Tool executed successfully (no output)."
                    elif not isinstance(content, str):
                        import json

                        try:
                            content = json.dumps(content)
                        except Exception:
                            content = str(content)

                    # Create a new ToolMessage to avoid mutating state directly if possible
                    # but here we are in a node, so modifying a local list is fine.
                    processed_messages.append(
                        ToolMessage(
                            content=content,
                            tool_call_id=m.tool_call_id,
                            status=m.status,
                            name=m.name,
                        )
                    )
                else:
                    processed_messages.append(m)

            messages = [system_msg] + processed_messages
            try:
                response = await self.model_with_tools.ainvoke(messages)
            except Exception as e:
                error_str = str(e).lower()
                if "413" in error_str or "token" in error_str or "rate_limit" in error_str:
                     return {"messages": [AIMessage(content="🚫 **Token Limit Exceeded**\n\nI can't process this request because our conversation history is too long. Please refresh the page to start a new chat.")]}
                raise e
            
            return {"messages": [response]}

        # Define the graph
        builder = StateGraph(ChatState)
        builder.add_node("assistant", assistant)

        if mcp_tools:
            builder.add_node("tools", ToolNode(mcp_tools))
            builder.add_edge(START, "assistant")

            def route_after_assistant(state: ChatState):
                last_message = state["messages"][-1]
                if last_message.tool_calls:
                    return "tools"
                return END

            builder.add_conditional_edges("assistant", route_after_assistant)
            builder.add_edge("tools", "assistant")
        else:
            builder.add_edge(START, "assistant")
            builder.add_edge("assistant", END)

        self.graph = builder.compile(checkpointer=self.memory)

    async def ainvoke(self, state: dict, config: dict = None):
        if self.graph is None:
            await self.initialize()
        return await self.graph.ainvoke(state, config=config)

    async def astream(
        self, state: dict, config: dict = None, stream_mode: str = "values"
    ):
        if self.graph is None:
            await self.initialize()
        async for output in self.graph.astream(
            state, config=config, stream_mode=stream_mode
        ):
            yield output


if __name__ == "__main__":

    async def test():
        bot = ChatbotApp()
        await bot.initialize()
        config = {"configurable": {"thread_id": "test_thread"}}
        inputs = {
            "messages": [HumanMessage(content="Hi!")],
            "username": "Jeff",
            "user_id": "123",
        }
        async for output in bot.astream(inputs, config=config):
            last_msg = output["messages"][-1]
        print(f"Assistant: {last_msg.content}")

    asyncio.run(test())
