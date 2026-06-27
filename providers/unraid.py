"""
Unraid provider for Homepage Helpers.

Requires:
- queries/unraid_stats.json
- queries/unraid_updates.json
- Unraid API key and CSRF token (set UNRAID_URL, UNRAID_API_KEY, UNRAID_CSRF_TOKEN env vars)

Endpoints:
/unraid/stats
/unraid/updates
"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import json
import os
import time
import logging

from pathlib import Path

import requests

from flask import Blueprint
from flask import jsonify

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Blueprint
# -----------------------------------------------------------------------------

unraid_bp = Blueprint(
    "unraid",
    __name__,
    url_prefix="/unraid"
)


# -----------------------------------------------------------------------------
# Paths and config
# -----------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent.parent / "config"

CACHE_TTL = int(
    os.getenv(
        "CACHE_TTL",
        "120"
    )
)

UNRAID_URL = os.getenv(
    "UNRAID_URL"
)

UNRAID_API_KEY = os.getenv(
    "UNRAID_API_KEY"
)

UNRAID_CSRF_TOKEN = os.getenv(
    "UNRAID_CSRF_TOKEN"
)


required_vars = {
    "UNRAID_URL": UNRAID_URL,
    "UNRAID_API_KEY": UNRAID_API_KEY,
    "UNRAID_CSRF_TOKEN": UNRAID_CSRF_TOKEN
}

missing = [
    key
    for key, value in required_vars.items()
    if not value
]

if missing:

    logger.warning(
        "Missing Unraid environment variables: %s",
        ", ".join(missing)
    )


_cache = {}


# -----------------------------------------------------------------------------
# Query loader
# -----------------------------------------------------------------------------

def load_config(filename):

    with open(BASE_DIR / filename, "r", encoding="utf-8") as f:

        return json.load(f)


# -----------------------------------------------------------------------------
# GraphQL helper
# -----------------------------------------------------------------------------

def graphql_call(query_file):

    cache_key = f"{UNRAID_URL}:{query_file}"

    now = time.time()

    if cache_key in _cache:

        cached = _cache[cache_key]

        if now - cached["time"] < CACHE_TTL:

            logger.info(
                "Unraid cache hit: %s",
                query_file
            )

            return cached["data"]

    headers = {
        "Content-Type": "application/json",
        "apollo-require-preflight": "true",
        "x-api-key": UNRAID_API_KEY,
        "x-csrf-token": UNRAID_CSRF_TOKEN
    }

    logger.info(
        "Fetching Unraid data: %s",
        query_file
    )

    response = requests.post(
        UNRAID_URL,
        json=load_config(query_file),
        headers=headers,
        timeout=10
    )

    try:

        response.raise_for_status()

    except Exception as e:

        logger.error(
            "Unraid GraphQL request failed: %s",
            e
        )

        raise

    data = response.json()

    _cache[cache_key] = {
        "time": now,
        "data": data
    }

    return data


# -----------------------------------------------------------------------------
# Business logic
# -----------------------------------------------------------------------------

def get_updates():

    data = graphql_call(
        "unraid_updates.json"
    )

    containers = (
        data["data"]["docker"]["containerUpdateStatuses"]
    )

    available_updates = [
        c["name"]
        for c in containers
        if c["updateStatus"] == "UPDATE_AVAILABLE"
    ]

    logger.info(
        "Found %d available updates",
        len(available_updates)
    )

    return {
        "count": len(available_updates),
        "updates": available_updates,
        "text": (
            " • ".join(available_updates)
            if available_updates
            else "Alles up-to-date"
        )
    }


def get_stats():

    return graphql_call(
        "unraid_stats.json"
    )


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

@unraid_bp.route(
    "/updates"
)
def updates():

    logger.info(
        "Unraid updates requested"
    )

    return jsonify(
        get_updates()
    )


@unraid_bp.route(
    "/stats"
)
def stats():

    logger.info(
        "Unraid stats requested"
    )

    return jsonify(
        get_stats()
    )
