from flask import Flask, jsonify
from providers import tautulli, unraid

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/tautulli/stats")
def tautulli_stats():
    return jsonify(tautulli.get_stats())


@app.route("/unraid/updates")
def unraid_updates():
    return jsonify(unraid.get_stats())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8383)