import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.tools import tool

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")
if not api_key:
    raise ValueError("TAVILY_API_KEY is not set in the environment variables.")

tavily_client = TavilyClient(api_key=api_key)

@tool("place_to_visit", description="Find recommended tourist attractions and places to visit in a given location based on the user's travel plans.")
def place_to_visit(location: str, travel_plans: str) -> str:
    query = f"""

    Tourist attractions and places to visit in {location} based on the following travel plans: {travel_plans}.
    """

    response = tavily_client.query(query)
    result = response["result"]

    output = []
    for result in results:
        output.append(
            f"Title: {result['title']}\n"
            f"URL: {result['url']}\n"
            f"Information: {result['content']}\n"
        )

    return "\n".join(output)

