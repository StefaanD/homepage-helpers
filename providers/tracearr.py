"""
Tracearr provider for Homepage Helpers.

Endpoints:

/tracearr/resolutions/movies
/tracearr/resolutions/tv
/tracearr/video_codecs
/tracearr/audio_codecs
/tracearr/audio_channels
"""

import json
import os
import logging

from pathlib import Path

import psycopg2
import psycopg2.extras

from flask import Blueprint
from flask import jsonify


logger = logging.getLogger(__name__)


tracearr_bp = Blueprint(
    "tracearr",
    __name__,
    url_prefix="/tracearr"
)

BASE_DIR = Path(__file__).parent.parent

SQL_DIR = BASE_DIR / "queries"
CONFIG_DIR = BASE_DIR / "config"

# sort the items based on the configuration
def sort_items(items):

    sort_order = CONFIG.get(
        "sort_order",
        "count_desc"
    )

    logger.info(
        f"Sorting items using '{sort_order}'"
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
                key=lambda item: item["label"].lower()
            )

        case _:

            logger.warning(
                f"Invalid sort_order '{sort_order}', falling back to count_desc"
            )

            return sorted(
                items,
                key=lambda item: item["count"],
                reverse=True
            )


# apply limits to the items based on the configuration
def apply_limits(items):

    top_n = CONFIG.get(
        "top_n",
        10
    )

    group_other = CONFIG.get(
        "group_other",
        True
    )

    logger.info(
        f"Applying limits: top_n={top_n}, group_other={group_other}"
    )

    if not isinstance(top_n, int):

        logger.warning(
            f"Invalid top_n value '{top_n}', using 10"
        )

        top_n = 10

    if top_n <= 0:

        logger.warning(
            f"Invalid top_n value '{top_n}', using 10"
        )

        top_n = 10

    if len(items) <= top_n:

        logger.info(
            "No limiting required"
        )

        return items

    if not group_other:

        logger.info(
            f"Truncating list to first {top_n} items"
        )

        return items[:top_n]
    
    if group_other and top_n < 2:

        logger.warning(
            f"top_n={top_n} too small when group_other enabled, using 2"
        )

        top_n = 2

    if group_other:

        visible_count = top_n - 1

    else:

        visible_count = top_n

    visible_items = items[:visible_count]

    other_items = items[visible_count:]

    other_count = sum(
        item["count"]
        for item in other_items
    )

    other_count = sum(
        item["count"]
        for item in other_items
    )

    if other_count > 0:

        visible_items.append({
            "label": "Other",
            "count": other_count
        })

        logger.info(
            f"Grouped {len(other_items)} items into Other ({other_count})"
        )

    return visible_items


def load_config():

    config_file = (
        CONFIG_DIR /
        "tracearr_configuration.json"
    )

    with open(config_file, "r") as f:
        return json.load(f)


CONFIG = load_config()


# get a connection to the database using environment variables
def get_connection():

    return psycopg2.connect(
        host=os.getenv(
            "TRACEARR_DB_HOST",
            "tracearr-supervised"
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
            "TRACEARR_DB_PASSWORD",
            "tracearr"
        )
    )


# execute the SQL file and return the results as a list of dictionaries
def execute_sql_file(filename):

    logger.info(
        f"Executing SQL query: {filename}"
    )

    sql_file = SQL_DIR / filename

    with open(sql_file, "r") as f:
        sql = f.read()

    conn = get_connection()

    try:

        with conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        ) as cur:

            cur.execute(sql)

            return cur.fetchall()
        
        logger.info(
            f"Query returned {len(rows)} rows"
        )

    finally:
        conn.close()


# normalize the codec using the mapping in the configuration
def normalize_codec(codec):

    mapping = CONFIG.get(
        "codec_mapping",
        {}
    )

    return mapping.get(codec, codec)


# audio channels are stored as integers, but we want to display them as strings
def normalize_audio_channels(value):

    mapping = CONFIG.get(
        "audio_channel_mapping",
        {}
    )

    return mapping.get(
        str(value),
        str(value)
    )


# transform the rows from the database into a normalized format
def transform_resolution_rows(rows):

    logger.info(
        f"Normalizing {len(rows)} resolution rows"
    )

    include_unknown = CONFIG.get(
        "include_unknown",
        True
    )

    result = []

    total = sum(
        row["count"]
        for row in rows
    )

    for row in rows:

        resolution = row["resolution"]

        if (
            resolution == "unknown"
            and not include_unknown
        ):
            continue

        result.append({
            "resolution": resolution,
            "count": row["count"],
            "percentage": round(
                (
                    row["count"] /
                    total
                ) * 100,
                1
            )
        })

    return result


# transform the codec rows to include normalized codec and percentage
def transform_codec_rows(rows):

    logger.info(
        f"Normalizing {len(rows)} codec rows"
    )

    include_unknown = CONFIG.get(
        "include_unknown",
        True
    )

    result = []

    total = sum(
        row["count"]
        for row in rows
    )

    for row in rows:

        codec = row["codec"]

        if (
            codec == "unknown"
            and not include_unknown
        ):
            continue

        result.append({
            "codec": normalize_codec(codec),
            "count": row["count"],
            "percentage": round(
                (
                    row["count"] /
                    total
                ) * 100,
                1
            )
        })

    logger.info(
        f"Normalized to {len(result)} codec items"
    )

    return result


# transform the audio channel rows to include display value and percentage
def transform_audio_channel_rows(rows):

    logger.info(
        f"Normalizing {len(rows)} audio channel rows"
    )

    include_unknown = CONFIG.get(
        "include_unknown",
        True
    )

    result = []

    total = sum(
        row["count"]
        for row in rows
    )

    for row in rows:

        channels = row["channels"]

        if (
            channels == 0
            and not include_unknown
        ):
            continue

        result.append({
            "channels": channels,
            "display": normalize_audio_channels(
                channels
            ),
            "count": row["count"],
            "percentage": round(
                (
                    row["count"] /
                    total
                ) * 100,
                1
            )
        })

    return result


# normalize the response to include total and count
def build_response(items):

    logger.info(
        f"Building response with {len(items)} items"
    )

    return {
        "total": len(items),
        "count": sum(
            item["count"]
            for item in items
        ),
        "items": items
    }


@tracearr_bp.route(
    "/resolutions/movies"
)
def resolutions_movies():

    logger.info(
        "Fetching resolution statistics for movies"
    )

    rows = execute_sql_file(
        "tracearr_resolutions_movies.sql"
    )

    items = transform_resolution_rows(
        rows
    )

    items = sort_items(
        items
    )

    items = apply_limits(
        items
    )

    logger.info(
        f"Returning {len(items)} resolution items for movies"
    )

    return jsonify(
        build_response(items)
    )


@tracearr_bp.route(
    "/resolutions/tv"
)
def resolutions_tv():

    logger.info(
        "Fetching resolution statistics for TV"
    )

    rows = execute_sql_file(
        "tracearr_resolutions_tv.sql"
    )

    items = transform_resolution_rows(
        rows
    )

    items = sort_items(
        items
    )

    items = apply_limits(
        items
    )

    logger.info(
        f"Returning {len(items)} resolution items for TV"
    )

    return jsonify(
        build_response(items)
    )


@tracearr_bp.route(
    "/video_codecs"
)
def video_codecs():

    logger.info(
        "Fetching video codec statistics"
    )

    rows = execute_sql_file(
        "tracearr_video_codecs.sql"
    )

    items = transform_codec_rows(
        rows
    )

    items = sort_items(
        items
    )

    items = apply_limits(
        items
    )

    logger.info(
        f"Returning {len(items)} video codec statistics"
    )

    return jsonify(
        build_response(items)
    )


@tracearr_bp.route(
    "/audio_codecs"
)
def audio_codecs():

    logger.info(
        "Fetching audio codec statistics"
    )

    rows = execute_sql_file(
        "tracearr_audio_codecs.sql"
    )

    items = transform_codec_rows(
        rows
    )

    items = sort_items(
        items
    )

    items = apply_limits(
        items
    )

    logger.info(
        f"Returning {len(items)} audio codec statistics"
    )

    return jsonify(
        build_response(items)
    )


@tracearr_bp.route(
    "/audio_channels"
)
def audio_channels():

    logger.info(
        "Fetching audio channel statistics"
    )

    rows = execute_sql_file(
        "tracearr_audio_channels.sql"
    )

    items = transform_audio_channel_rows(
        rows
    )

    items = sort_items(
        items
    )

    items = apply_limits(
        items
    )

    logger.info(
        f"Returning {len(items)} audio channel statistics"
    )

    return jsonify(
        build_response(items)
    )


@tracearr_bp.route(
    "/music_codecs"
)
def music_codecs():

    logger.info(
        "Fetching music codec statistics"
    )

    rows = execute_sql_file(
        "tracearr_music_codecs.sql"
    )

    items = transform_codec_rows(
        rows
    )

    items = sort_items(
        items
    )

    items = apply_limits(
        items
    )

    logger.info(
        f"Returning {len(items)} music codec statistics"
    )

    return jsonify(
        build_response(items)
    )