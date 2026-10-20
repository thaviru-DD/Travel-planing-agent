from langchain_ollama import ChatOllama
from langchain.agents import create_agent

from tools.distance import distance
from tools.places_to_visit import place_to_visit
from tools.weather import weather


from langchain_core.tools import tool

model = ChatOllama(model="llama3.2", temperature=0)

#Create travel info agent 

travel_info_agent = create_agent(
    model=model,
    tools=[place_to_visit, distance, weather],
   system_prompt = """
                    You are a travel information assistant.

                    Your job is to provide travel information requested by the main
                    travel planning agent.

                    AVAILABLE TOOLS:

                    1. distance
                    - Calculate the distance between two locations.

                    2. weather
                    - Get weather information for a specific location and date.
                    - Use this tool when weather information is requested.

                    3. place_to_visit
                    - Find places to visit at a destination.


                    WEATHER TOOL RULES:

                    When using the weather tool:

                    - The location must be provided.
                    - The date must be provided.
                    - The date MUST be converted to YYYY-MM-DD format.

                    For example:

                    25 October 2026
                    → 2026-10-25

                    October 25, 2026
                    → 2026-10-25

                    25/10/2026
                    → 2026-10-25

                    Do not invent a date.

                    Do not invent weather information.

                    If the required location or date is missing, do not call the
                    weather tool.


                    GENERAL RULES:

                    - Use the appropriate tool to answer the request.
                    - Do not invent information.
                    - Return the tool result to the main travel planning agent.
                    """

)

# Wrap sub agent as a tool

@tool("travel_info",description=(
        "Get travel information about distance, weather, "
        "and places to visit. Use this tool for travel-information requests."
    )
)
def travel_info(query: str) -> str:
    """
    Send a travel-information request to the Travel Info Agent.
    """

    response = travel_info_agent.invoke(
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
