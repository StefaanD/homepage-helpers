from flask import Flask, jsonify, request
from providers import health, tautulli, unraid, ipmi, tracearr
import os
import logging

app = Flask(__name__)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)


PORT = int(os.getenv("PORT", "8383"))

# --- BEGIN HEALTH ENDPOINT ---
@app.route("/health")
def health_check():
    return jsonify(
        health.get_health()
    )
# --- END HEALTH ENDPOINT ---


# --- BEGIN TAUTULLI ENDPOINTS ---
@app.route("/tautulli/stats")
def tautulli_stats():
    aggregate = request.args.get("aggregate", "on").lower()

    return jsonify(
        tautulli.get_stats(
            aggregate=(aggregate != "off")
        )
    )
# --- END TAUTULLI ENDPOINTS ---


# --- UNRAID ENDPOINTS ---
@app.route("/unraid/updates")
def unraid_updates():
    url = request.args.get("url")
    api_key = request.args.get("apikey")
    csrf_token = request.args.get("csrftoken")

    if not all([url, api_key, csrf_token]):
        return jsonify({
            "error": "missing url, apikey or csrftoken"
        }), 400

    return jsonify(
        unraid.get_updates(url, api_key, csrf_token)
    )


@app.route("/unraid/stats")
def unraid_stats():
    url = request.args.get("url")
    api_key = request.args.get("apikey")
    csrf_token = request.args.get("csrftoken")

    return jsonify(
        unraid.get_stats(url, api_key, csrf_token)
    )
# --- END UNRAID ENDPOINTS ---


# --- BEGIN IPMI ENDPOINTS ---
@app.route("/ipmi/sensors")
def ipmi_sensors():

    host = request.args.get("host")
    username = request.args.get("username")
    password = request.args.get("password")

    if not all([host, username, password]):
        return jsonify({
            "error": "missing host, username or password"
        }), 400

    return jsonify(
        ipmi.get_sensors(
            host,
            username,
            password
        )
    )
# --- END IPMI ENDPOINTS ---


# --- BEGIN TRACEARR ENDPOINTS ---
@app.route("/tracearr/resolution")
def tracearr_resolution():
    return jsonify(tracearr.get_resolution())


@app.route("/tracearr/codecs")
def tracearr_codecs():
    return jsonify(tracearr.get_codecs())


@app.route("/tracearr/session_aggregates")
def tracearr_session_aggregates():
    return jsonify(tracearr.get_session_aggregates ())
# --- END TRACEARR ENDPOINTS --- 


if __name__ == "__main__":

    logger.info(
        f"Starting Homepage Helpers on port {PORT}"
    )

    app.run(
        host="0.0.0.0",
        port=PORT
    )
