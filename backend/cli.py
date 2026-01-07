import asyncio
import os
from dotenv import load_dotenv
from Agent.chatbot import ChatbotApp
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()


async def main():
    print("Welcome to ReciKit Meal Planning Assistant!")
    print("Type 'exit' or 'quit' to stop.\n")

    # Initialize the chatbot app
    bot = ChatbotApp()
    try:
        await bot.initialize()
    except Exception as e:
        print(f"Error initializing chatbot (is the MCP server running?): {e}")
        # We can still proceed if the bot handles fallback internally

    username = "jeff"
    user_id = "user_123"
    config = {"configurable": {"thread_id": "cli_session_1"}}

    while True:
        try:
            user_input = input(f"{username} > ")
        except EOFError:
            break

        if user_input.lower() in ["exit", "quit"]:
            break

        # Invoke the bot
        inputs = {
            "messages": [HumanMessage(content=user_input)],
            "username": username,
            "user_id": user_id,
        }

        last_msg = None
        async for output in bot.astream(inputs, config=config, stream_mode="values"):
            if "messages" in output and output["messages"]:
                last_msg = output["messages"][-1]

        if isinstance(last_msg, AIMessage):
            print(f"\nAssistant: {last_msg.content}\n")
        elif last_msg:
            print(f"\n[Unexpected message type: {type(last_msg)}]\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
