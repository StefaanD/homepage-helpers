import requests
import time

# cache in seconden
CACHE_TTL = 60
_cache = {}


QUERY = {
    "query": """
    query ContainerUpdateStatuses {
      docker {
        containerUpdateStatuses {
          name
          updateStatus
        }
      }
    }
    """
}


def get_stats(unraid_url, api_key, csrf_token):
    cache_key = f"{unraid_url}:{api_key}"

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

    try:
        response = requests.post(
            unraid_url,
            json=QUERY,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        containers = data["data"]["docker"]["containerUpdateStatuses"]

        updates = [
            c["name"]
            for c in containers
            if c["updateStatus"] == "UPDATE_AVAILABLE"
        ]

        result = {
            "count": len(updates),
            "updates": updates,
            "text": " • ".join(updates) if updates else "Alles up-to-date"
        }

        _cache[cache_key] = {
            "time": now,
            "data": result
        }

        return result

    except Exception as e:
        return {
            "count": -1,
            "updates": [],
            "text": f"Error: {str(e)}"
        }