import asyncio
import itertools
import sys
import time
from agents.research_agent import research_agent
from agents.summarizer_agent import summarizer_agent
from agents.answer_agent import answer_agent
from config import ACTIVE_MODEL
from logger_config import setup_logger

logger = setup_logger()
def section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

async def spinner(text):
    """Simple animated spinner while agent is working."""
    try:
        for char in itertools.cycle(["|", "/", "-", "\\"]):
            sys.stdout.write(f"\r{text} {char}")
            sys.stdout.flush()
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        sys.stdout.write("\r" + " " * (len(text) + 4) + "\r")
        sys.stdout.flush()
        raise
def get_last_message_content(result):
    try:
        if not result or not getattr(result, "messages", None):
            return "No response returned."
        return result.messages[-1].content
    except Exception:
        return "Could not parse agent response."
    
async def run_single_agent(agent, task, agent_name, spinner_text):
    logger.info(f"{agent_name} started")
    start = time.time()
    spin = asyncio.create_task(spinner(spinner_text))
    try:
        result = await agent.run(task=task)
        output = get_last_message_content(result)
        elapsed = time.time() - start
        logger.info(f"{agent_name} completed in {elapsed:.2f} seconds")
        return output, elapsed
    except Exception as e:
        elapsed = time.time() - start
        logger.exception(f"{agent_name} failed: {e}")
        return f"ERROR: {str(e)}", elapsed
    finally:
        spin.cancel()
        try:
            await spin
        except asyncio.CancelledError:
            pass

async def run_pipeline(user_query):
    """Run full Research -> Summarizer -> Answer pipeline for a single query."""
    total_start = time.time()
    logger.info(f"New query received: {user_query}")
    section("User Query")
    print(user_query)
    print("\nResearch Agent working...")
    research_output, research_time = await run_single_agent(
        research_agent,
        user_query,
        "Research Agent",
        "Researching..."
    )
    section("Research Output")
    print(research_output)
    if research_output.startswith("ERROR:"):
        print("\nPipeline stopped at Research Agent.")
        logger.error("Pipeline stopped at Research Agent")
        return
    print("\nSummarizer Agent working...")
    summary_output, summary_time = await run_single_agent(
        summarizer_agent,
        research_output,
        "Summarizer Agent",
        "Summarizing..."
    )
    section("Summary")
    print(summary_output)
    if summary_output.startswith("ERROR:"):
        print("\nPipeline stopped at Summarizer Agent.")
        logger.error("Pipeline stopped at Summarizer Agent")
        return
    print("\nAnswer Agent working...")
    final_answer, answer_time = await run_single_agent(
        answer_agent,
        summary_output,
        "Answer Agent",
        "Generating Answer..."
    )
    section("Final Answer")
    print(final_answer)
    total_time = time.time() - total_start
    section("Performance Metrics")
    print(f"Research Agent latency: {research_time:.2f} seconds")
    print(f"Summarizer Agent latency: {summary_time:.2f} seconds")
    print(f"Answer Agent latency: {answer_time:.2f} seconds")
    print(f"Total pipeline latency: {total_time:.2f} seconds")
    logger.info(
        f"Pipeline finished | research={research_time:.2f}s | "
        f"summary={summary_time:.2f}s | answer={answer_time:.2f}s | "
        f"total={total_time:.2f}s"
    )
    
async def main():
    logger.info("Day-1 system started")
    print("\nMulti-Agent System Ready")
    print(f"Active Model: {ACTIVE_MODEL}")
    print("Type a question or type 'exit' to stop\n")
    while True:
        query = input("\nUser: ").strip()
        if not query:
            print("Please enter a valid query.")
            continue
        if query.lower() == "exit":
            print("\nStopping agent system...")
            logger.info("System stopped by user")
            break
        await run_pipeline(query)
if __name__ == "__main__":
    asyncio.run(main())