import json
import requests
from pathlib import Path
import time

BASE = Path(__file__).parent.parent / "queries"

CACHE_TTL = 60
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
            return cached["data"]

    headers = {
        "Content-Type": "application/json",
        "apollo-require-preflight": "true",
        "x-api-key": api_key,
        "x-csrf-token": csrf_token
    }

    response = requests.post(
        url,
        json=load_query(query_file),
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

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