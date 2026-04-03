import asyncio
import time
import itertools
import sys

from agents.research_agent import research_agent
from agents.summarizer_agent import summarizer_agent
from agents.answer_agent import answer_agent
def section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
async def spinner(text):
    """Simple animated spinner while agent is working"""
    for char in itertools.cycle(["|", "/", "-", "\\"]):
        sys.stdout.write(f"\r{text} {char}")
        sys.stdout.flush()
        await asyncio.sleep(0.1)
async def run_pipeline(user_query):
    """Run full Research → Summarizer → Answer pipeline for a single query"""
    total_start = time.time()

    section("User Query")
    print(user_query)
    print("\nResearch Agent working...")
    start = time.time()
    spin = asyncio.create_task(spinner("Researching..."))

    research_result = await research_agent.run(task=user_query)

    spin.cancel()
    research_time = time.time() - start
    research_output = research_result.messages[-1].content

    section("Research Output")
    print(research_output)
    print("\nSummarizer Agent working...")
    start = time.time()
    spin = asyncio.create_task(spinner("Summarizing..."))

    summary_result = await summarizer_agent.run(task=research_output)

    spin.cancel()
    summary_time = time.time() - start
    summary_output = summary_result.messages[-1].content

    section("Summary")
    print(summary_output)
    print("\nAnswer Agent working...")
    start = time.time()
    spin = asyncio.create_task(spinner("Generating Answer..."))

    answer_result = await answer_agent.run(task=summary_output)

    spin.cancel()
    answer_time = time.time() - start
    final_answer = answer_result.messages[-1].content
    section("Final Answer")
    print(final_answer)
    total_time = time.time() - total_start
    section("Performance Metrics")
    print(f"Research Agent latency: {research_time:.2f} seconds")
    print(f"Summarizer Agent latency: {summary_time:.2f} seconds")
    print(f"Answer Agent latency: {answer_time:.2f} seconds")
    print(f"Total pipeline latency: {total_time:.2f} seconds")
async def main():
    print("\nMulti-Agent System Ready")
    print("Type a question or type 'exit' to stop\n")
    while True:
        query = input("\nUser: ")
        if query.lower() == "exit":
            print("\nStopping agent system...")
            break
        await run_pipeline(query)
if __name__ == "__main__":
    asyncio.run(main())