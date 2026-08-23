from langchain_core.tools import tool


@tool(
    "place_to_visit",
    description="Find recommended tourist attractions and places to visit in a given location based on the user's travel plans."
)
def place_to_visit(location: str, travel_plans: str) -> str:

    return f"""
    Recommended places in {location}:

    1. Temple of the Tooth
    2. Kandy Lake
    3. Royal Botanical Gardens
    4. Bahirawakanda Temple

    Travel plan:
    {travel_plans}
    """