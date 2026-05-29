import sqlite3
import os
import time

DB_PATH = os.getenv("TAUTULLI_DB", "/config/tautulli.db")

CACHE_TTL = 120

_cache = {}


def query_db():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            section_name,
            section_type,
            count,
            parent_count,
            child_count
        FROM library_sections
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def aggregate_rows(rows):

    movies = 0
    tvshows = 0
    artists = 0
    albums = 0
    tracks = 0

    for name, section_type, count, parent, child in rows:

        section_type = (section_type or "").lower()

        count = int(count or 0)
        parent = int(parent or 0)
        child = int(child or 0)

        if section_type == "movie":
            movies += count

        elif section_type == "show":
            tvshows += count

        elif section_type == "artist":
            artists += count
            albums += parent
            tracks += child

    return {
        "movies": movies,
        "tvshows": tvshows,
        "artists": artists,
        "albums": albums,
        "tracks": tracks
    }


def detailed_rows(rows):

    result = []

    for name, section_type, count, parent, child in rows:

        result.append({
            "name": name,
            "type": section_type,
            "count": int(count or 0),
            "parent_count": int(parent or 0),
            "child_count": int(child or 0)
        })

    return result


def get_stats(aggregate=True):

    cache_key = "aggregate" if aggregate else "detailed"

    now = time.time()

    if cache_key in _cache:

        cached = _cache[cache_key]

        if now - cached["time"] < CACHE_TTL:
            return cached["data"]

    rows = query_db()

    if aggregate:
        data = aggregate_rows(rows)

    else:
        data = detailed_rows(rows)

    _cache[cache_key] = {
        "time": now,
        "data": data
    }

    return data
