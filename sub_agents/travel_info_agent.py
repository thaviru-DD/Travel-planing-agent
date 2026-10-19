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
    system_prompt="""
    You are a travel information specialist.

    Your job is to help users with:
    - distance between two locations
    - weather information 
    - places to visit 

    Use available tools whenever needed. 

    If the user ask about distance use distance tool.
    If the user ask about weather use weather tool.
    If the user ask about places to visit use place_to_visit tool. 

    You may use more than one tool when the user's request requires
    multiple types of travel information.

    Do not handle transport budget recommendations.
    Do not perform general mathematical calculations.
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
