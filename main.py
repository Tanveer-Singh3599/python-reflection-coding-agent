import subprocess
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from langgraph.types import Command
from models import gemini_model
from schema import response_format, SYSTEM_PROMPT
from tools import web_search, coding_environment
from middlewares import (
    ToolErrorMiddleware
)

# starting docker sandbox
result = subprocess.run(
    [
        "docker",
        "run",
        "--rm",
        "agent-python:3.13",
        "python",
        "-c",
        "print('Hello from Docker')"
    ],
    capture_output=True,
    text=True
)

print(result.stdout)
print(result.stderr)

# core agent
agent = create_agent(
    model=gemini_model,
    system_prompt=SYSTEM_PROMPT,
    tools=[web_search, coding_environment],
    middleware=[
        ToolErrorMiddleware()
    ],
    response_format=response_format,
    checkpointer=InMemorySaver()
)

# agent execution 
def execute_agent():

    # first user input
    print("Hi how can I help you today?")
    user_input = input("-> ")

    # crreating thread config
    config = {
        "configurable": {"thread_id": "curr_thread"}
    }

    # invoking agent
    res = agent.invoke(
        input={"messages": [HumanMessage(content=user_input)]},
        config=config
    )

    # printing result
    print(res["messages"][-1].content[0]["text"])

if __name__ == "__main__":
    execute_agent()