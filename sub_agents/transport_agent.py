from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.tools import tool

# import tools
from tools.bus import bus
from tools.train import train          # make sure tools/train.py exists (see notes)
from tools.transport import transport

# Create a model
model = ChatOllama(model="llama3.2", temperature=0)

# Create transport agent
transport_agent = create_agent(
    model=model,
    tools=[bus, train, transport],
    system_prompt="""
                    You are a transport assistant.

                    Your job is to provide transport information requested by the main travel
                    planning agent. You only handle transport.

                    AVAILABLE TOOLS:

                    1. bus
                    - Public bus options: departure times, fare per person, total fare.
                    - Arguments: origin, destination, budget (LKR), passengers.

                    2. train
                    - Public train options: departure times, classes, fare per person, total fare.
                    - Arguments: origin, destination, budget (LKR), passengers.

                    3. transport
                    - PRIVATE transport (car, van, bike, hired bus): cost per km and suitability.
                    - Arguments: origin, destination, budget (LKR), passengers.

                    WHICH TOOL TO USE:
                    - "bus" or "public bus" -> bus
                    - "train" -> train
                    - "public transport" with no vehicle named -> call BOTH bus and train
                    - "private", "car", "van", "bike", "taxi", "hire" -> transport
                    - If the request does not say public or private, call all three tools.

                    RULES:
                    - Use ONLY the information returned by the tools. Never invent routes,
                    fares, times or distances.
                    - Copy numbers (fares, times, distances, totals) exactly as the tools return them.
                    Do not recalculate or round them.
                    - If a tool says information is not available, tell the main agent that.
                    - If origin, destination, budget or passengers is missing from the request,
                    do not guess. Reply only with the names of the missing details.
                    - Do not give travel/places information or accommodation information.
                    """,
)


@tool(
    "transport_agent",
    description=(
        "Get transport options for a route. "
        "For private transport (car, van, bike), it uses the transport tool. "
        "For public transport, it uses the bus and train tools. "
        "The query MUST include origin, destination, number of passengers "
        "and total budget in LKR."
    ),
)
def transport_agent_tool(query: str) -> str:
    """
    query: a full sentence with origin, destination, passengers and budget,
    e.g. "Public transport from Colombo to Kandy for 5 passengers, budget Rs. 30000".
    """
    response = transport_agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    return response["messages"][-1].content