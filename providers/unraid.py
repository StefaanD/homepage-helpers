import requests
import os

REMOVED = os.getenv(
    "REMOVED",
    "REMOVED"
)

API_KEY = os.getenv("REMOVED")
CSRF_TOKEN = os.getenv("REMOVED")

HEADERS = {
    "Content-Type": "application/json",
    "apollo-require-preflight": "true",
    "x-api-key": API_KEY,
    "x-csrf-token": CSRF_TOKEN
}

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


def get_stats():
    try:
        response = requests.post(
            REMOVED,
            json=QUERY,
            headers=HEADERS,
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

        return {
            "count": len(updates),
            "updates": updates,
            "text": " • ".join(updates) if updates else "Alles up-to-date"
        }

    except Exception as e:
        return {
            "count": -1,
            "updates": [],
            "text": f"Error: {str(e)}"
        }