import asyncio
import os
import sys
import traceback

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import model_client
from memory_agent import MemoryAgent


async def main():
    try:
        os.makedirs("db", exist_ok=True)

        print("\nInitializing memory agent...")
        agent = MemoryAgent(model_client=model_client)

        print("\nDay-4 Memory Agent")
        print("Commands: debug | search <query> | clear | quit\n")

        while True:
            try:
                user_input = input("You: ").strip()
            except EOFError:
                break

            if not user_input:
                continue

            if user_input == "quit":
                await agent.close()
                print("Goodbye!")
                break

            if user_input == "debug":
                await agent.debug()
                continue

            if user_input.startswith("search "):
                await agent.search(user_input[7:])
                continue

            if user_input == "clear":
                await agent.clear()
                continue

            response = await agent.run(user_input)
            print(f"\nAgent: {response}\n")

    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())