"""
Tracearr provider for Homepage Helpers.

Requires:
- queries/tracearr_resolution.json
- queries/tracearr_codecs.json
- queries/tracearr_session_aggregates.json
- connection to the Tracearr API (set TRACEARR_URL and TRACEARR_TOKEN env vars)

Returns resolution and codec stats in JSON format for Homepage customapi widgets.
"""

import json
import os
import time
import logging
import requests

from pathlib import Path

logger = logging.getLogger(__name__)

BASE = Path(__file__).parent.parent / "queries"

CACHE_TTL = int(os.getenv("CACHE_TTL", "120"))

_cache = {}


def load_config(name):
    with open(BASE / name) as f:
        return json.load(f)


def call_tracearr(config_file):

    cache_key = config_file

    now = time.time()

    if cache_key in _cache:

        cached = _cache[cache_key]

        if now - cached["time"] < CACHE_TTL:
            logger.info(f"Tracearr cache hit: {cache_key}")
            return cached["data"]

    config = load_config(config_file)

    url = os.getenv("TRACEARR_URL")
    token = os.getenv("TRACEARR_TOKEN")

    if not url:
        raise ValueError("TRACEARR_URL not configured")

    if not token:
        raise ValueError("TRACEARR_TOKEN not configured")

    logger.info(f"Fetching Tracearr data: {config['endpoint']}")

    response = requests.get(
        f"{url}{config['endpoint']}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        },
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    _cache[cache_key] = {
        "time": now,
        "data": data
    }

    data = response.json()

    data["watchTimeHuman"] = format_duration(
        data["totalWatchTimeMs"]
    )

    return data


def get_resolution():
    return call_tracearr("tracearr_resolution.json")


def get_codecs():
    return call_tracearr("tracearr_codecs.json")


def get_session_aggregates():
    return call_tracearr("tracearr_session_aggregates.json")


# --- BEGIN DURATION CALCULATION ---
def format_duration(ms):
    seconds = ms // 1000

    days = seconds // 86400
    hours = (seconds % 86400) // 3600

    return f"{days}d {hours}h"
# --- END DURATION CALCULATION ---