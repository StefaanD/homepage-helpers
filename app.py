from flask import Flask, jsonify, request
from providers import tautulli, unraid, ipmi

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/tautulli/stats")
def tautulli_stats():
    return jsonify(tautulli.get_stats())


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


@app.route("/ipmi/sensors")
def ipmi_sensors():
    return jsonify(ipmi.get_sensors())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8383)