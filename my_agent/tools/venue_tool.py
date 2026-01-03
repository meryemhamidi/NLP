"""Tool to search in the app-level venue catalog."""

from __future__ import annotations

from typing import List, Optional

from my_agent.memory.app_catalog import VENUES, Venue


def find_venues(
    city: Optional[str] = None,
    guests: Optional[int] = None,
    price_band: Optional[str] = None,
    indoor: Optional[bool] = None,
) -> dict:
    """Filter the static catalog with simple criteria."""
    matches: List[Venue] = []
    for v in VENUES:
        if city and v.city.lower() != city.lower():
            continue
        if guests and v.capacity < guests:
            continue
        if price_band and v.price_band != price_band:
            continue
        if indoor is not None and v.indoor != indoor:
            continue
        matches.append(v)

    return {
        "count": len(matches),
        "results": [
            {
                "city": v.city,
                "name": v.name,
                "capacity": v.capacity,
                "price_band": v.price_band,
                "indoor": v.indoor,
                "notes": v.notes,
            }
            for v in matches
        ],
        "hint": "Ajustez price_band (low/mid/high) ou indoor=True/False pour affiner.",
    }
