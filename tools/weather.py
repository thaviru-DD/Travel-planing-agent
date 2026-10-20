import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


@tool("weather", description="Get weather information for a given date and location.")
def weather(location: str, date: str) -> str:
    """
    Get weather information for a specific location and date.

    Args:
        location: City or location name.
        date: Date in YYYY-MM-DD format.
    """

    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        forecasts = [
            item
            for item in data["list"]
            if item["dt_txt"].startswith(date)
        ]

        if not forecasts:
            return f"No weather forecast available for {location} on {date}."

        temperatures = [
            item["main"]["temp"]
            for item in forecasts
        ]

        descriptions = [
            item["weather"][0]["description"]
            for item in forecasts
        ]

        rain_probability = max(
            item.get("pop", 0) * 100
            for item in forecasts
        )

        return (
            f"Weather forecast for {location} on {date}:\n"
            f"Conditions: {', '.join(set(descriptions))}\n"
            f"Temperature: {min(temperatures):.1f}°C - "
            f"{max(temperatures):.1f}°C\n"
            f"Rain probability: {rain_probability:.0f}%"
        )

    except requests.exceptions.RequestException as e:
        return f"Unable to retrieve weather data: {e}"