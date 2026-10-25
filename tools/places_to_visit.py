
import os

from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise ValueError("TAVILY_API_KEY is not set in the environment variables.")

tavily_client = TavilyClient(api_key=api_key)

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


@tool(
    "place_to_visit",
    description=(
        "Find actual tourist attractions in a location based on "
        "the user's travel plans. Return a simple list of place names."
    )
)
def place_to_visit(location: str, travel_plans: str) -> str:

    query = (
        f"Actual tourist attractions, landmarks, temples, parks, "
        f"and visitor destinations in {location}. "
        f"Travel plans: {travel_plans}. "
        "Find specific attraction names, not travel articles or websites."
    )

    response = tavily_client.search(
        query,
        max_results=10
    )

    results = response.get("results", [])

    if not results:
        return f"No tourist attractions found for {location}."

    # Collect webpage titles and content for the LLM.
    search_context = "\n\n".join(
        f"Title: {result.get('title', '')}\n"
        f"Content: {result.get('content', '')}"
        for result in results
    )

    prompt = f"""
You are a travel information assistant.

Identify actual tourist attractions mentioned in the search results.

Location: {location}
Travel plans: {travel_plans}

Search results:
{search_context}

Instructions:
- Return only real, specific tourist attraction names.
- Exclude article titles, travel guides, websites, and general activities.
- Prefer attractions located in or near {location}.
- Remove duplicate names.
- Do not invent places that are not supported by the search results.
- Return a maximum of 10 attractions.
- Format the output exactly like this:

Places to visit:
- Attraction name 1
- Attraction name 2
- Attraction name 3

If no actual attractions can be identified, say so.
"""

    result = llm.invoke(prompt)

    return result.content.strip()
