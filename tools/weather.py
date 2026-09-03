import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

@tool("weather", description="Get the weather information for given date and location.")
def weather(location: str, date:str) -> str:
    """Get weather information for a specific location and date. Use this tool when the user asks about weather conditions, temperature,
    rain, or forecast for a location."""




