"""
Geospatial Calculations & Routing Utilities
Provides haversine distance, realistic urban road distance calculation, and mapping links.
Uses the exact tiered urban detour logic from the South East Bengaluru Real Estate Radar.
"""

import math
from typing import Tuple, Dict, Any, Optional


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance between two points on the earth in km."""
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return 0.0
    try:
        lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
    except (ValueError, TypeError):
        return 0.0

    R = 6371.0  # Earth radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


def calculate_road_distance_km(lat1: float, lon1: float, lat2: float, lon2: float, city_id: str = "bengaluru") -> float:
    """
    Calculates realistic road network distance in km between two coordinate points
    in urban Indian metros, accounting for street curvature, flyovers, and arterial detours.
    Identical logic and multi-tier formula as South East Bengaluru Real Estate Radar:
    - Short / Local grid (h <= 1.0 km): 1.25x
    - Medium / Arterial / Tech corridor (1.0 < h <= 8.0 km): 1.32x
    - Long / Highway / Bypass (h > 8.0 km): 1.22x
    """
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return 0.0
    try:
        lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
    except (ValueError, TypeError):
        return 0.0

    h = haversine_distance_km(lat1, lon1, lat2, lon2)
    if h <= 0.05:
        return 0.1

    # Tiered urban network detour factors
    factor = 1.25 if h <= 1.0 else (1.32 if h <= 8.0 else 1.22)
    return round(max(0.3, h * factor), 1)


def estimate_urban_road_distance_km(lat1: float, lon1: float, lat2: float, lon2: float, city_id: str = "bengaluru") -> float:
    """Alias for calculate_road_distance_km for backwards compatibility."""
    return calculate_road_distance_km(lat1, lon1, lat2, lon2, city_id=city_id)


def get_google_maps_search_url(query: str) -> str:
    """Returns a direct Google Maps search URL for a named location/query."""
    import urllib.parse
    return f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(query)}"


def get_google_maps_directions_url(origin_lat: float, origin_lng: float, dest_query: str) -> str:
    """Returns a turn-by-turn navigation URL from origin coordinates to destination."""
    import urllib.parse
    return f"https://www.google.com/maps/dir/?api=1&origin={origin_lat},{origin_lng}&destination={urllib.parse.quote(dest_query)}&travelmode=driving"
