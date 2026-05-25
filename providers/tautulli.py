from flask import Flask, jsonify
import sqlite3
import os
import time
import traceback

app = Flask(__name__)

DB_PATH = os.getenv("TAUTULLI_DB", "/config/tautulli.db")

# cache in seconden
CACHE_TTL = 120

_cache = {
    "time": 0,
    "data": None
}

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


def compute_stats(rows):
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

        # alles van type movie optellen
        if section_type == "movie":
            movies += count

        # alles van type show optellen
        elif section_type == "show":
            tvshows += count

        # music library
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

def get_stats():
    now = time.time()

    # cache hit
    if _cache["data"] and now - _cache["time"] < CACHE_TTL:
        return _cache["data"]

    rows = query_db()
    data = compute_stats(rows)

    _cache["data"] = data
    _cache["time"] = now

    return data

@app.route("/")
def root():
    try:
        return jsonify(get_stats())
    except Exception as e:
        return jsonify({
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8383,
        debug=False
    )