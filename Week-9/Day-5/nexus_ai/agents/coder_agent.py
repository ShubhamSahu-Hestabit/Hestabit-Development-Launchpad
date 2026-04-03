import os
import logging
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

logger = logging.getLogger(__name__)
WORK_DIR = os.path.abspath(".")

class CoderAgent:
    def __init__(self, model_client):
        self.executor = LocalCommandLineCodeExecutor(work_dir=WORK_DIR)

        self.writer = AssistantAgent(
            name="CoderWriter",
            model_client=model_client,
            system_message=(
                "You are a Python code writer.\n"
                "Write clean Python code to complete the task.\n"
                "RULES:\n"
                "1. Output ONLY a single Python code block\n"
                "2. Always use print() to show results\n"
                "3. Include comments for clarity\n"
                "4. Do NOT explain — just the code block\n"
                "\n"
                "FILE FINDER — always use for ANY file:\n"
                "   import os\n"
                "   def find_file(name):\n"
                "       for path in [name, f'outputs/{name}']:\n"
                "           if os.path.exists(path): return path\n"
                "       raise FileNotFoundError(f'{name} not found')\n"
                "\n"
                "WHEN TASK INVOLVES READING + ANALYZING A CSV:\n"
                "   1. Read file using find_file()\n"
                "   2. Print columns and full data\n"
                "   3. Compute ACTUAL statistics using real column names:\n"
                "      - Total, average, min, max for numeric columns\n"
                "      - Top/bottom performers using groupby\n"
                "      - Trends over time if date column exists\n"
                "   4. Print ALL computed results with actual numbers\n"
                "   IMPORTANT: Use df.columns to see real names first,\n"
                "   then access columns by their EXACT names from the data\n"
                "\n"
                "EXAMPLE for CSV analysis:\n"
                "   import pandas as pd, os\n"
                "   def find_file(name):\n"
                "       for path in [name, f'outputs/{name}']:\n"
                "           if os.path.exists(path): return path\n"
                "       raise FileNotFoundError(f'{name} not found')\n"
                "   df = pd.read_csv(find_file('sales.csv'))\n"
                "   print('Columns:', df.columns.tolist())\n"
                "   print(df.to_string())\n"
                "   # Use actual column names from above\n"
                "   num_cols = df.select_dtypes(include='number').columns\n"
                "   print('\\nStatistics:')\n"
                "   print(df[num_cols].describe())\n"
                "   for col in num_cols:\n"
                "       print(f'Total {col}:', df[col].sum())\n"
                "       print(f'Top by {col}:', df.loc[df[col].idxmax()])\n"
                "\n"
                "WHEN TASK INVOLVES CREATING A CSV:\n"
                "   import pandas as pd\n"
                "   df = pd.DataFrame({...})\n"
                "   df.to_csv('outputs/filename.csv', index=False)\n"
                "   print('Done')\n"
                "   print(df.to_string())\n"
                "\n"
                "WHEN TASK IS PURE LOGIC:\n"
                "   Just write the algorithm directly\n"
            ))

        self.runner = CodeExecutorAgent(
            name="CoderRunner",
            code_executor=self.executor
        )

    async def run(self, content: str) -> str:
        logger.info("Coder running")
        cancellation = CancellationToken()

        write_response = await self.writer.on_messages(
            [TextMessage(content=content, source="user")],
            cancellation
        )
        code_message = write_response.chat_message
        logger.info("Code written, executing...")

        run_response = await self.runner.on_messages(
            [code_message],
            cancellation
        )
        execution_result = run_response.chat_message.content

        logger.info(f"Coder done: {len(execution_result)} chars")
        return (
            f"Code:\n{code_message.content}\n\n"
            f"Output:\n{execution_result}"
        )

    async def start(self):
        await self.executor.start()
        logger.info(f"Code executor started in: {WORK_DIR}")

    async def stop(self):
        await self.executor.stop()
        logger.info("Code executor stopped")