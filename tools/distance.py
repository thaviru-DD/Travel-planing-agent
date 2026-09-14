import os
import requests

from langchain_core.tools import tool
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


# Get Google Maps API key
api_key = os.getenv("GOOGLE_MAPS_API_KEY")

if not api_key:
    raise ValueError(
        "GOOGLE_MAPS_API_KEY is not set in the environment variables."
    )


@tool(
    "distance",
    description="Calculate the driving distance and duration between two locations using Google Maps Routes API."
)
def distance(origin: str, destination: str) -> str:
    """
    Calculate the driving distance and duration
    between two locations using Google Maps Routes API.
    """

    # Google Routes API endpoint
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"


    # Request headers
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.distanceMeters,routes.duration"
    }


    # Request body
    body = {
        "origin": {
            "address": origin
        },
        "destination": {
            "address": destination
        },
        "travelMode": "DRIVE",
        "units": "METRIC"
    }


    try:
        # Send POST request to Google
        response = requests.post(
            url,
            headers=headers,
            json=body,
            timeout=10
        )

        # Raise error for 4xx / 5xx responses
        response.raise_for_status()

    except requests.RequestException as error:
        return f"Google Maps API request failed: {error}"


    # Convert response to Python dictionary
    data = response.json()


    # Check whether Google returned a route
    if not data.get("routes"):
        return (
            f"No driving route found between "
            f"{origin} and {destination}."
        )


    # Get first route
    route = data["routes"][0]


    # Get distance in meters
    distance_meters = route["distanceMeters"]


    # Convert meters to kilometers
    distance_km = distance_meters / 1000


    # Google returns duration like "1234s"
    duration = route["duration"]


    return (
        f"Driving distance from {origin} to {destination}: "
        f"{distance_km:.2f} km. "
        f"Estimated duration: {duration}."
    )
