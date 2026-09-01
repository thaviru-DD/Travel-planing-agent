import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

api_key = os.getenv("GOOGLE_MAPS_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_MAPS_API_KEY is not set in the environment variables.")

@tool("distance", description="Calculate the distance between two locations using Google Map API.")
def distance(origin:str , destination:str) -> str:
    """Calculate the distance between two locations using Google Map API."""

    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.distanceMeters,routes.duration"
    }

    data = {
        "origin": {
            "address": origin
        },
        "destination": {
            "address": destination
        },
        "travelMode": "DRIVE"
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        return f"Google Maps API error: {response.text}"

    result = response.json()

    route = result["routes"][0]

    distance_meters = route["distanceMeters"]
    duration = route["duration"]

    distance_km = distance_meters / 1000

    return f"Distance: {distance_km:.2f} km, Duration: {duration}"
