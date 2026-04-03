import asyncio
from orchestrator_tool import run_orchestration, summarize_results

async def main():
    print("\nDay-3 Multi-Agent System (File + DB + Code)\n")
    while True:
        try:
            query = input("Enter your query (or type 'exit'): ").strip()
            if query.lower() in ["exit", "quit"]:
                print("Exiting...")
                break
            context = await run_orchestration(query)
            print("\nSummary:\n")
            summary = await summarize_results(context)
            print(summary)
            print("\n" + "=" * 60 + "\n")
        except Exception as e:
            print(f"ERROR: {str(e)}\n")

if __name__ == "__main__":
    asyncio.run(main())