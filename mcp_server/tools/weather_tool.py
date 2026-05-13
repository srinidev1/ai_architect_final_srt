import json
import os
import httpx
from dotenv import load_dotenv

load_dotenv(override=True)

GEO_URL = os.getenv("GEO_URL", "https://geocoding-api.open-meteo.com/v1/search")
WEATHER_URL = os.getenv("WEATHER_URL", "https://api.open-meteo.com/v1/forecast")


def get_current_weather(location: str) -> str:
    """
    Get the current weather for a given location.

    Args:
        location: City or place name (e.g. 'London', 'New York', 'Tokyo')

    Returns:
        A JSON string with temperature, wind speed, weather description, etc.
    """
    geo = _geocode(location)
    params = {
        "latitude": geo["lat"],
        "longitude": geo["lon"],
        "current": [
            "temperature_2m", "relative_humidity_2m", "apparent_temperature",
            "weather_code", "wind_speed_10m", "wind_direction_10m",
            "precipitation", "cloud_cover",
        ],
        "timezone": "auto",
    }
    resp = httpx.get(WEATHER_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    current = data["current"]
    result = {
        "location": f"{geo['name']}, {geo['country']}",
        "temperature_c": current["temperature_2m"],
        "feels_like_c": current["apparent_temperature"],
        "humidity_pct": current["relative_humidity_2m"],
        "wind_speed_kmh": current["wind_speed_10m"],
        "wind_direction_deg": current["wind_direction_10m"],
        "precipitation_mm": current["precipitation"],
        "cloud_cover_pct": current["cloud_cover"],
        #"condition": WMO_CODES.get(current["weather_code"], "Unknown"),
        "units": {"temperature": "°C", "wind": "km/h", "precipitation": "mm"},
    }
    return json.dumps(result, indent=2)

def get_forecast(location: str, days: int = 5) -> str:
    """
    Get a multi-day weather forecast for a given location.

    Args:
        location: City or place name (e.g. 'Paris', 'Sydney')
        days: Number of forecast days (1-7, default 5)

    Returns:
        A JSON string with daily high/low temperatures and conditions.
    """
    days = max(1, min(days, 7))
    geo = _geocode(location)
    params = {
        "latitude": geo["lat"],
        "longitude": geo["lon"],
        "daily": [
            "temperature_2m_max", "temperature_2m_min",
            "weather_code", "precipitation_sum", "wind_speed_10m_max",
        ],
        "timezone": "auto",
        "forecast_days": days,
    }
    resp = httpx.get(WEATHER_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    daily = data["daily"]
    forecast = []
    for i in range(len(daily["time"])):
        forecast.append({
            "date": daily["time"][i],
            "temp_max_c": daily["temperature_2m_max"][i],
            "temp_min_c": daily["temperature_2m_min"][i],
            #"condition": WMO_CODES.get(daily["weather_code"][i], "Unknown"),
            "precipitation_mm": daily["precipitation_sum"][i],
            "max_wind_kmh": daily["wind_speed_10m_max"][i],
        })
    result = {
        "location": f"{geo['name']}, {geo['country']}",
        "forecast_days": days,
        "daily": forecast,
    }
    return json.dumps(result, indent=2)


def _geocode(location: str) -> dict:
    """Resolve a location name to lat/lon."""
    resp = httpx.get(GEO_URL, params={"name": location, "count": 1, "language": "en", "format": "json"}, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("results"):
        raise ValueError(f"Location '{location}' not found.")
    r = data["results"][0]
    return {"lat": r["latitude"], "lon": r["longitude"], "name": r["name"], "country": r.get("country", "")}
