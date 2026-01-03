"""External tool: fetch weather forecast via Open-Meteo (no key required)."""

from __future__ import annotations

import requests


def get_weather(city: str) -> dict:
    """Return simple weather forecast for the city using Open-Meteo geocoding + forecast.

    Resilient to API errors and missing fields; never raises.
    """
    if not city or not str(city).strip():
        return {"city": city, "status": "invalid_city"}

    try:
        geo_resp = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "fr", "format": "json"},
            timeout=10,
        )
        geo_resp.raise_for_status()
        geo = geo_resp.json()
    except Exception as err:  # network/parse errors
        return {"city": city, "status": "geo_error", "detail": str(err)}

    results = geo.get("results")
    if not isinstance(results, list) or not results:
        return {
            "city": city,
            "status": "not_found",
            "detail": geo.get("reason") or "no geocoding result",
        }

    loc = results[0]
    lat = loc.get("latitude")
    lon = loc.get("longitude")
    if lat is None or lon is None:
        return {"city": city, "status": "invalid_coordinates", "detail": loc}

    try:
        forecast_resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
                "forecast_days": 1,
            },
            timeout=10,
        )
        forecast_resp.raise_for_status()
        forecast = forecast_resp.json()
    except Exception as err:
        return {"city": city, "status": "forecast_error", "detail": str(err)}

    current = forecast.get("current_weather") or {}
    return {
        "city": loc.get("name", city),
        "country": loc.get("country"),
        "temperature_c": current.get("temperature"),
        "windspeed_kmh": current.get("windspeed"),
        "weathercode": current.get("weathercode"),
        "status": "ok" if current else "no_current_weather",
    }
