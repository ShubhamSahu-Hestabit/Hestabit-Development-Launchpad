from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import BufferedChatCompletionContext
from config import model_client

answer_agent = AssistantAgent(
    name="AnswerAgent",
    model_client=model_client,
    system_message="""
You are the Answer Agent.

You receive summarized information from another agent.

Using that summary, generate the final response.

Structure the response clearly:

1. Short explanation
2. Key points (bullet list)
3. Final conclusion

Keep the answer clear, simple, and informative.
""",
    model_context=BufferedChatCompletionContext(buffer_size=10),
)