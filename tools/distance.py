import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

Gooogle_map_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
if not Gooogle_map_api_key:
    raise ValueError("No googge map API key found in the environment variables.")

@tool("distance", description="Calculate the distance between two locations")
def calculate_distance(location1: str, location2: str) -> str:
    query = f"""
    Calculate the distance between {location1} and {location2}.
    """