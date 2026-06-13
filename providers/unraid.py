"""
Unraid provider for Homepage Helpers.

Requires:
- queries/unraid_stats.json
- queries/unraid_updates.json
- Unraid API key and CSRF token (set UNRAID_URL, UNRAID_API_KEY, UNRAID_CSRF_TOKEN env vars)

Returns system stats and available updates in JSON format for Homepage customapi widgets.
"""

import json
import requests
from pathlib import Path
import time
import logging


logger = logging.getLogger(__name__)


BASE = Path(__file__).parent.parent / "queries"

CACHE_TTL = int(
    os.getenv("CACHE_TTL", "120")
)

_cache = {}


def load_query(filename):
    with open(BASE / filename) as f:
        return json.load(f)


def graphql_call(url, api_key, csrf_token, query_file):
    cache_key = f"{url}:{query_file}"
    now = time.time()

    if cache_key in _cache:
        cached = _cache[cache_key]
        if now - cached["time"] < CACHE_TTL:
            logger.info("Unraid cache hit")
            return cached["data"]

    headers = {
        "Content-Type": "application/json",
        "apollo-require-preflight": "true",
        "x-api-key": api_key,
        "x-csrf-token": csrf_token
    }

    logger.info(f"Fetching Unraid data using {query_file}")

    response = requests.post(
        url,
        json=load_query(query_file),
        headers=headers,
        timeout=10
    )

    try:
        response.raise_for_status()

    except Exception as e:
        logger.error(f"Unraid request failed: {e}")
        raise

    data = response.json()

    _cache[cache_key] = {
        "time": now,
        "data": data
    }

    return data


def get_updates(url, api_key, csrf_token):
    data = graphql_call(
        url,
        api_key,
        csrf_token,
        "unraid_updates.json"
    )

    containers = data["data"]["docker"]["containerUpdateStatuses"]

    updates = [
        c["name"]
        for c in containers
        if c["updateStatus"] == "UPDATE_AVAILABLE"
    ]

    return {
        "count": len(updates),
        "updates": updates,
        "text": " • ".join(updates) if updates else "Alles up-to-date"
    }


def get_stats(url, api_key, csrf_token):
    return graphql_call(
        url,
        api_key,
        csrf_token,
        "unraid_stats.json"
    )