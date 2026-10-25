from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.tools import tool

# import tools
from tools.hotel_search import hotel_search

# Create a model
model = ChatOllama(model="llama3.2", temperature=0)

# Create accommodation agent
accommodation_agent = create_agent(
    model=model,
    tools=[hotel_search],
    system_prompt="""
                    You are an accommodation assistant.

                    Your job is to find hotels requested by the main travel
                    planning agent. You only handle accommodation.

                    AVAILABLE TOOLS:

                    1. hotel_search
                    - Searches the web for hotels in a location.
                    - Arguments: location, guests, nights, budget_per_night (LKR).

                    REQUIRED DETAILS:
                    - location (the destination city)
                    - guests (number of travellers)
                    - nights (number of nights)

                    OPTIONAL DETAIL:
                    - budget_per_night in LKR. If it is not given, use 0.

                    RULES:
                    - If location, guests or nights is missing from the request,
                    do not call the tool and do not guess. Reply only with the
                    names of the missing details.
                    - Use ONLY the information returned by the hotel_search tool.
                    Never invent hotel names, prices, ratings, availability or
                    booking confirmations.
                    - Only state a price if the tool result contains it. Copy it
                    exactly. If no price is listed, say "price not listed".
                    - If the tool says nothing was found or the search failed,
                    tell the main agent that.
                    - Return up to 3 hotels. For each: name, short description,
                    price if listed, and the URL.
                    - Do not give transport, weather, distance or places-to-visit
                    information.
                    - Do not book anything.
                    """,
)


# Wrap sub agent as a tool
@tool(
    "accommodation",
    description=(
        "Find hotels for a destination. "
        "The query MUST include the location, number of guests and number of "
        "nights, and may include a nightly budget in LKR. "
        "Use only for trips of more than one day."
    ),
)
def accommodation(query: str) -> str:
    """
    query: a full sentence, e.g.
    "Find hotels in Kandy for 4 guests for 2 nights, budget Rs. 15000 per night."
    """
    response = accommodation_agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    return response["messages"][-1].content
