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

    return result


# transform the audio channel rows to include display value and percentage
def transform_audio_channel_rows(rows):

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

    rows = execute_sql_file(
        "tracearr_resolutions_movies.sql"
    )

    items = transform_resolution_rows(
        rows
    )

    return jsonify(
        build_response(items)
    )


@tracearr_bp.route(
    "/resolutions/tv"
)
def resolutions_tv():

    rows = execute_sql_file(
        "tracearr_resolutions_tv.sql"
    )

    items = transform_resolution_rows(
        rows
    )

    return jsonify(
        build_response(items)
    )


@tracearr_bp.route(
    "/video_codecs"
)
def video_codecs():

    rows = execute_sql_file(
        "tracearr_video_codecs.sql"
    )

    items = transform_codec_rows(
        rows
    )

    return jsonify(
        build_response(items)
    )


@tracearr_bp.route(
    "/audio_codecs"
)
def audio_codecs():

    rows = execute_sql_file(
        "tracearr_audio_codecs.sql"
    )

    items = transform_codec_rows(
        rows
    )

    return jsonify(
        build_response(items)
    )


@tracearr_bp.route(
    "/audio_channels"
)
def audio_channels():

    rows = execute_sql_file(
        "tracearr_audio_channels.sql"
    )

    items = transform_audio_channel_rows(
        rows
    )

    return jsonify(
        build_response(items)
    )


@tracearr_bp.route(
    "/music_codecs"
)
def music_codecs():

    rows = execute_sql_file(
        "tracearr_music_codecs.sql"
    )

    items = transform_codec_rows(
        rows
    )

    return jsonify(
        build_response(items)
    )