from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.tools import tool

from tools.transport import transport
from tools.bus import bus
from tools.train import train


model = ChatOllama(
    model="llama3.2",
    temperature=0
)


# Create Transport Agent
transport_sub_agent = create_agent(
    model=model,
    tools=[transport, bus, train],
    system_prompt="""
You are a transportation planning assistant.

Your job is to recommend suitable transportation
based on the user's travel requirements.

Available transportation tools:

1. transport
   - Private transportation options.
   - Uses the private transport knowledge base.

2. bus
   - Public bus information.
   - Uses the public bus knowledge base.

3. train
   - Public train information.
   - Uses the train knowledge base.

Choose the appropriate tool based on the user's
transportation requirements.

Do not invent:
- fares
- schedules
- availability
- travel times
- operators

Use only information returned by the available tools.
"""
)


# Wrap Transport Agent as a tool
@tool(
    "transport_agent",
    description=(
        "Get transportation recommendations including "
        "private transport, public buses, and trains "
        "based on the user's travel requirements."
    )
)
def transport_agent(query: str) -> str:
    """
    Send a transportation request to the Transport Agent.
    """

    response = transport_sub_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
    )

    return response["messages"][-1].content