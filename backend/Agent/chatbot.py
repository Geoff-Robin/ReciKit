import os
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langgraph.graph import StateGraph, MessagesState
from langchain_mcp_adapters.client import MultiServerMCPClient
from Agent.menu_handler import handle_menu
    

async def chatbot_node(state: MessagesState):
    last_message = state["messages"][-1].content
    client = MultiServerMCPClient(
        {
            "recommendation_service" : {
                "transport": "streamable_http",
                "url": os.getenv("RECOMMENDATION_SERVICE_URL")
            }
        }
    )
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )
    tools = await client.get_tools()
    agent = create_agent(llm, tools)
    
    menu_reply = handle_menu(last_message, state["messages"])

    if menu_reply:
        return {"messages": state["messages"] + [menu_reply]}
    
    response = await agent.ainvoke(state["messages"])
    return {"messages": state["messages"] + [response]}

graph = StateGraph(MessagesState)
graph.add_node("chatbot", chatbot_node)
graph.set_entry_point("chatbot")
chatbot_app = graph.compile()
