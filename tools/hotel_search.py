import os

from dotenv import load_dotenv
from langchain_core.tools import tool

# Load variables from the .env file in the project root
load_dotenv()

MAX_RESULTS = 5          # how many web results to return to the agent
MAX_SNIPPET_CHARS = 400  # keep each snippet short so the small LLM is not overloaded


def _get_client():
    """Create the Tavily client when the tool is used (not at import time),
    so the rest of the app still starts if the key is missing."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError("TAVILY_API_KEY is not set in the .env file.")

    from tavily import TavilyClient

    return TavilyClient(api_key=api_key)


def build_query(location: str, guests: int, budget_per_night: float) -> str:
    """Build the web-search query for the hotel search."""
    place = location.strip()
    if "sri lanka" not in place.lower():
        place = f"{place}, Sri Lanka"

    query = (
        f"Best hotels to stay in {place} for {guests} guest(s), "
        "price per night in LKR, location and rating"
    )
    if budget_per_night and budget_per_night > 0:
        query += f", around Rs. {budget_per_night:,.0f} per night or less"
    return query


def format_results(results: list, location: str, nights: int, guests: int,
                   budget_per_night: float) -> str:
    """Turn raw Tavily results into plain text for the agent."""
    budget_text = (
        f"Rs. {budget_per_night:,.0f} per night"
        if budget_per_night and budget_per_night > 0
        else "not specified"
    )
    lines = [
        f"Hotel search results for {location} "
        f"({nights} night(s), {guests} guest(s), budget: {budget_text}):",
        "",
    ]

    for i, result in enumerate(results[:MAX_RESULTS], start=1):
        snippet = (result.get("content") or "").strip().replace("\n", " ")
        if len(snippet) > MAX_SNIPPET_CHARS:
            snippet = snippet[:MAX_SNIPPET_CHARS].rstrip() + "..."
        lines.append(
            f"{i}. {result.get('title', 'Untitled')}\n"
            f"   URL: {result.get('url', 'n/a')}\n"
            f"   Information: {snippet}\n"
        )

    lines.append(
        "NOTE: These are web search results. Prices and availability are NOT "
        "verified. Only state a price if it appears in the information above; "
        "otherwise say the price is not listed. Never invent hotel names, "
        "prices, availability or booking confirmations."
    )
    return "\n".join(lines)


@tool(
    "hotel_search",
    description=(
        "Search the web for suitable hotels in a location. Returns hotel names, "
        "links and short descriptions (prices only if listed). "
        "Arguments: location, guests, nights, budget_per_night (LKR, 0 if unknown)."
    ),
)
def hotel_search(
    location: str,
    guests: int = 1,
    nights: int = 1,
    budget_per_night: float = 0,
) -> str:
    """
    location: city or area, e.g. "Kandy".
    guests: number of travellers.
    nights: number of nights to stay.
    budget_per_night: hotel budget per night in LKR (0 if the user has none).
    """
    try:
        client = _get_client()
        response = client.search(
            build_query(location, guests, budget_per_night),
            max_results=MAX_RESULTS,
        )
    except Exception as error:  # missing key, network error, API error ...
        return (
            f"Hotel search failed: {error}. "
            "Tell the user hotel information is not available right now. "
            "Do not invent hotels or prices."
        )

    results = response.get("results", [])
    if not results:
        return (
            f"No hotel results found for {location}. "
            "Tell the user nothing was found. Do not invent hotels."
        )

    return format_results(results, location, nights, guests, budget_per_night)