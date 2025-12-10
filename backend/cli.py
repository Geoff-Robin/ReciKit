from Agent import chatbot
from Agent.models import Message
import asyncio
from dotenv import load_dotenv

load_dotenv()


async def main():
    state = {"messages": []}

    while True:
        user_input = input("> ")
        if user_input.lower() in ["exit", "quit"]:
            break

        state["messages"].append(Message(role="user", content=user_input))
        result = await chatbot.ainvoke(state)

        reply = result["messages"][-1]
        print(reply.content)

        state = result


if __name__ == "__main__":
    asyncio.run(main())
