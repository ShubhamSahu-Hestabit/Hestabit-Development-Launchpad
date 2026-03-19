import logging
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.tools.code_execution import PythonCodeExecutionTool
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from config import model_client

logger = logging.getLogger(__name__)

executor = LocalCommandLineCodeExecutor()
code_execution_tool = PythonCodeExecutionTool(executor=executor)

code_agent = AssistantAgent(
    name="CodeExecutorAgent",
    tools=[code_execution_tool],
    model_client=model_client,
    system_message=(
        "You are a code execution agent.\n"

        "RULES:\n"
        "1. ALWAYS print output using print().\n"
        "2. NEVER save files to disk.\n"
        "3. If generating CSV data, output ONLY valid CSV format.\n"
        "4. DO NOT add explanations or text.\n"
        "5. Use pandas when needed.\n"

        "CONTEXT USAGE:\n"
        "If CSV data is provided, parse it like:\n"
        "import io, pandas as pd\n"
        "df = pd.read_csv(io.StringIO(csv_data))\n"

        "CSV OUTPUT FORMAT:\n"
        "When generating CSV, ALWAYS use:\n"
        "print(df.to_csv(index=False))\n"

        "FINAL OUTPUT MUST BE PRINTED."
    )
)