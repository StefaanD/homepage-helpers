"""
Tracearr provider for Homepage Helpers.

Requires:
- config/tracearr_configuration.json
- Tracearr database information (set
    TRACEARR_DB_HOST
    TRACEARR_DB_PORT
    TRACEARR_DB_NAME
    TRACEARR_DB_USER
    TRACEARR_DB_PASSWORD env vars)

Endpoints:
/tracearr/resolutions/movies
/tracearr/resolutions/tv
/tracearr/video_codecs
/tracearr/audio_codecs
/tracearr/audio_channels
"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import json
import logging
import os
import time

from pathlib import Path

import psycopg2
import psycopg2.extras

from flask import Blueprint
from flask import jsonify

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Blueprint
# -----------------------------------------------------------------------------

tracearr_bp = Blueprint(
    "tracearr",
    __name__,
    url_prefix="/tracearr"
)

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent.parent

SQL_DIR = BASE_DIR / "queries"

CONFIG_PATH = os.getenv(
    "TRACEARR_CONFIG",
    "/config/tracearr_configuration.json"
)

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

def load_config():

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:

        logger.info(
            "Loading Tracearr configuration from %s",
            CONFIG_PATH
        )

        return json.load(f)

# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------

def get_connection():

    return psycopg2.connect(
        host=os.getenv(
            "TRACEARR_DB_HOST",
            "tracearr-db"
        ),
        port=os.getenv(
            "TRACEARR_DB_PORT",
            "5432"
        ),
        dbname=os.getenv(
            "TRACEARR_DB_NAME",
            "tracearr"
        ),
        user=os.getenv(
            "TRACEARR_DB_USER",
            "tracearr"
        ),
        password=os.getenv(
            "TRACEARR_DB_PASSWORD"
        )
    )


def execute_sql_file(filename):

    logger.info(
        "Executing SQL query: %s",
        filename
    )

    sql_file = SQL_DIR / filename

    with open(
        sql_file,
        "r",
        encoding="utf-8"
    ) as f:

        sql = f.read()

    conn = get_connection()

    try:

        with conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        ) as cur:

            start = time.perf_counter()

            cur.execute(sql)

            rows = cur.fetchall()

            duration = round(
                time.perf_counter() - start,
                3
            )

            logger.info(
                "Query returned %d rows in %.3f seconds",
                len(rows),
                duration
            )

            return rows

    finally:

        conn.close()


# -----------------------------------------------------------------------------
# Normalization
# -----------------------------------------------------------------------------

def normalize_codec(codec, config):

    mapping = config.get(
        "codec_mapping",
        {}
    )

    return mapping.get(
        codec,
        codec
    )


def normalize_audio_channels(value, config):

    mapping = config.get(
        "audio_channel_mapping",
        {}
    )

    return mapping.get(
        str(value),
        str(value)
    )


# -----------------------------------------------------------------------------
# Transformation
# -----------------------------------------------------------------------------

def transform_resolution_rows(rows, config):

    include_unknown = config.get(
        "include_unknown",
        True
    )

    total = sum(
        row["count"]
        for row in rows
    )

    items = []

    for row in rows:

        resolution = row["resolution"]

        if (
            resolution == "unknown"
            and not include_unknown
        ):
            continue

        items.append({
            "resolution": resolution,
            "count": row["count"],
            "percentage": round(
                row["count"] / total * 100,
                1
            )
        })

    return items


def transform_codec_rows(rows, config):

    include_unknown = config.get(
        "include_unknown",
        True
    )

    total = sum(
        row["count"]
        for row in rows
    )

    items = []

    for row in rows:

        codec = row["codec"]

        if (
            codec == "unknown"
            and not include_unknown
        ):
            continue

        items.append({
            "codec": normalize_codec(codec, config),
            "count": row["count"],
            "percentage": round(
                row["count"] / total * 100,
                1
            )
        })

    return items


def transform_audio_channel_rows(rows, config):

    include_unknown = config.get(
        "include_unknown",
        True
    )

    total = sum(
        row["count"]
        for row in rows
    )

    items = []

    for row in rows:

        channels = row["channels"]

        if (
            channels == 0
            and not include_unknown
        ):
            continue

        items.append({
            "channels": channels,
            "display": normalize_audio_channels(channels, config),
            "count": row["count"],
            "percentage": round(
                row["count"] / total * 100,
                1
            )
        })

    return items


def transform_stats_rows(rows, config):

    if not rows:
        return []

    row = rows[0]

    return [
        {
            "label": "Total items",
            "value": row["total_items"]
        },
        {
            "label": "Total size",
            "value": format_bytes(
                 row["total_size_bytes"]
            )
        },
        {
            "label": "Movies",
            "value": row["movie_count"]
        },
        {
            "label": "TV episodes",
            "value": row["episode_count"]
        },
        {
            "label": "Music",
            "value": row["music_count"]
        },
        {
            "label": "4K files",
            "value": row["count_4k"]
        },
        {
            "label": "1080p files",
            "value": row["count_1080p"]
        },
        {
            "label": "720p files",
            "value": row["count_720p"]
        },
        {
            "label": "SD files",
            "value": row["count_sd"]
        }
    ]


def transform_history_stats_rows(
    rows,
    _config
):
    """
    Transform history aggregate statistics.
    """

    if not rows:
        return []

    row = rows[0]

    return [
        {
            "label": "Plays",
            "value": row["play_count"]
        },
        {
            "label": "Watch time",
            "value": format_duration(
                row["total_watch_time_ms"]
            ),
            "milliseconds": row["total_watch_time_ms"]
        },
        {
            "label": "Unique users",
            "value": row["unique_users"]
        },
        {
            "label": "Unique titles",
            "value": row["unique_content"]
        }
    ]


def transform_value_rows(
    rows,
    _config,
    field_name
):
    """
    Transform simple value/count rows.
    """

    items = []

    for row in rows:

        items.append({
            field_name: row["value"],
            "count": row["count"]
        })

    return items


def transform_country_rows(
    rows,
    config
):
    """
    Transform country history rows.
    """

    return [
        {
            "country": row["value"],
            "count": row["count"]
        }
        for row in rows
        if row["value"]
    ]


def transform_device_rows(
    rows,
    config
):
    """
    Transform device history rows.
    """

    return [
        {
            "device": row["value"],
            "count": row["count"]
        }
        for row in rows
        if row["value"]
    ]


def transform_platform_rows(
    rows,
    config
):
    """
    Transform platform history rows.
    """

    return [
        {
            "platform": row["value"],
            "count": row["count"]
        }
        for row in rows
        if row["value"]
    ]


def transform_user_rows(
    rows,
    config
):
    """
    Transform user history rows.
    """

    return [
        {
            "username": row["username"],
            "count": row["count"]
        }
        for row in rows
        if row["username"]
    ]




# -----------------------------------------------------------------------------
# Sorting, limiting and duration (ms)
# -----------------------------------------------------------------------------

def get_item_label(item):

    return (
        item.get("codec")
        or item.get("resolution")
        or item.get("display")
        or "Unknown"
    )


def sort_items(items, config):
    """
    Sort items either by count or alphabetical
    and descending or ascending
    """

    sort_order = config.get(
        "sort_order",
        "count_desc"
    )

    logger.info(
        "Sorting items using %s",
        sort_order
    )

    match sort_order:

        case "count_desc":

            return sorted(
                items,
                key=lambda item: item["count"],
                reverse=True
            )

        case "count_asc":

            return sorted(
                items,
                key=lambda item: item["count"]
            )

        case "alphabetical":

            return sorted(
                items,
                key=lambda item: get_item_label(item).lower()
            )

        case _:

            logger.warning(
                "Invalid sort_order '%s', using count_desc",
                sort_order
            )

            return sorted(
                items,
                key=lambda item: item["count"],
                reverse=True
            )


def apply_limits(items, config):
    """
    Apply top_n and group_other configuration
    to a list of items.
    """

    top_n = config.get(
        "top_n",
        10
    )

    group_other = config.get(
        "group_other",
        True
    )

    logger.info(
        "Applying limits to top %s",
        top_n
    )

    logger.info(
        "Applying limits to group others %s",
        group_other
    )

    if len(items) <= top_n:
        return items

    if not group_other:
        return items[:top_n]

    if top_n < 2:
        top_n = 2

    visible_count = top_n - 1

    visible_items = items[:visible_count]

    other_items = items[visible_count:]

    other_count = sum(
        item["count"]
        for item in other_items
    )

    if other_count > 0:

        label_key = None

        for key in (
            "display",
            "codec",
            "resolution",
            "country",
            "device",
            "platform",
            "user"
        ):
            if key in visible_items[0]:
                label_key = key
                break

        if label_key:

            visible_items.append({
                label_key: "Other",
                "count": other_count
            })

    return visible_items


def format_duration(ms):
    """
    Convert milliseconds to a human readable string.
    """

    total_seconds = ms // 1000

    days = total_seconds // 86400

    hours = (
        total_seconds % 86400
    ) // 3600

    minutes = (
        total_seconds % 3600
    ) // 60

    if days > 0:
        return f"{days}d {hours}h"

    if hours > 0:
        return f"{hours}h {minutes}m"

    return f"{minutes}m"


def format_bytes(size_bytes):
    """
    Convert bytes to a human readable string.
    """

    if size_bytes == 0:
        return "0 B"

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB",
        "PB"
    ]

    size = float(size_bytes)

    for unit in units:

        if size < 1024:
            return f"{size:.1f} {unit}"

        size /= 1024

    return f"{size:.1f} PB"


# -----------------------------------------------------------------------------
# Response helpers
# -----------------------------------------------------------------------------

def build_response(items):

    return {
        "total": len(items),
        "count": sum(
            item["count"]
            for item in items
        ),
        "items": items
    }


def run_query(
    sql_file,
    transformer,
    apply_sorting=True,
    apply_limiting=True
):
    """
    Execute a Tracearr SQL query, transform the results,
    apply sorting and limits, and return a JSON response.
    """

    config = load_config()

    rows = execute_sql_file(
        sql_file
    )

    items = transformer(
        rows,
        config
    )

    if apply_sorting:

        items = sort_items(
            items,
            config
        )

    if apply_limiting:

        items = apply_limits(
            items,
            config
        )

    return jsonify(
        build_response(items)
    )


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

@tracearr_bp.route(
    "/resolutions/movies"
)
def resolutions_movies():

    logger.info(
        "Movie resolutions requested"
    )

    return run_query(
        "tracearr_resolutions_movies.sql",
        transform_resolution_rows
    )


@tracearr_bp.route(
    "/resolutions/tv"
)
def resolutions_tv():

    logger.info(
        "TV resolutions requested"
    )

    return run_query(
        "tracearr_resolutions_tv.sql",
        transform_resolution_rows
    )


@tracearr_bp.route(
    "/video_codecs"
)
def video_codecs():

    logger.info(
        "Video codecs requested"
    )

    return run_query(
        "tracearr_video_codecs.sql",
        transform_codec_rows
    )


@tracearr_bp.route(
    "/audio_codecs"
)
def audio_codecs():

    logger.info(
        "Audio codecs requested"
    )

    return run_query(
        "tracearr_audio_codecs.sql",
        transform_codec_rows
    )


@tracearr_bp.route(
    "/music_codecs"
)
def music_codecs():

    logger.info(
        "Music codecs requested"
    )

    return run_query(
        "tracearr_music_codecs.sql",
        transform_codec_rows
)

@tracearr_bp.route(
    "/audio_channels"
)
def audio_channels():

    logger.info(
        "Audio channels requested"
    )

    return run_query(
        "tracearr_audio_channels.sql",
        transform_audio_channel_rows
    )

@tracearr_bp.route(
    "/stats"
)
def stats():

    logger.info(
        "Library statistics requested"
    )

    config = load_config()

    rows = execute_sql_file(
        "tracearr_stats.sql"
    )

    items = transform_stats_rows(
        rows,
        config
    )

    return jsonify(
        {
            "items": items
        }
    )

@tracearr_bp.route(
    "/history/countries"
)
def history_countries():

    logger.info(
        "History countries requested"
    )

    return run_query(
        "tracearr_history_countries.sql",
        transform_country_rows
    )

@tracearr_bp.route(
    "/history/devices"
)
def history_devices():

    logger.info(
        "History devices requested"
    )

    return run_query(
        "tracearr_history_devices.sql",
        transform_device_rows
    )

@tracearr_bp.route(
    "/history/platforms"
)
def history_platforms():

    logger.info(
        "History platforms requested"
    )

    return run_query(
        "tracearr_history_platforms.sql",
        transform_platform_rows
    )

@tracearr_bp.route(
    "/history/users"
)
def history_users():

    logger.info(
        "History users requested"
    )

    return run_query(
        "tracearr_history_users.sql",
        transform_user_rows
    )

@tracearr_bp.route(
    "/history/stats"
)
def history_stats():

    logger.info(
        "History stats requested"
    )

    config = load_config()

    rows = execute_sql_file(
        "tracearr_history_stats.sql"
    )

    items = transform_history_stats_rows(
        rows,
        config
    )

    return jsonify(
        {
            "items": items
        }
    )
