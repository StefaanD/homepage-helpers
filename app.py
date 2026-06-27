"""
Main script for Homepage Helpers.

Requires:

Endpoints:
"""

import os
import logging

from flask import Flask
from flask import jsonify

from logging_config import configure_logging
from config_manager import ensure_config_files

from providers.endpoints import endpoints_bp
from providers.health import health_bp
from providers.ipmi import ipmi_bp
from providers.tautulli import tautulli_bp
from providers.tracearr import tracearr_bp
from providers.unraid import unraid_bp


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

configure_logging()


logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Flask
# -----------------------------------------------------------------------------

ensure_config_files()


# -----------------------------------------------------------------------------
# Flask
# -----------------------------------------------------------------------------

app = Flask(__name__)

app.json.sort_keys = False


# -----------------------------------------------------------------------------
# Set app name and version, also used by endpoint.py
# -----------------------------------------------------------------------------

app.config["APP_NAME"] = "Homepage Helpers"
app.config["APP_VERSION"] = "0.2.0"

app.register_blueprint(
    endpoints_bp
)

app.register_blueprint(
    health_bp
)

app.register_blueprint(
    ipmi_bp
)

app.register_blueprint(
    tautulli_bp
)

app.register_blueprint(
    tracearr_bp
)

app.register_blueprint(
    unraid_bp
)

PORT = int(
    os.getenv(
        "PORT",
        "8383"
    )
)

logger.info(
    "Homepage Helpers started on port %s",
    PORT
)


@app.route("/")
def root():

    logger.info(
        "Root endpoint requested"
    )

    return jsonify(
        {
            "application": "Homepage Helpers",
            "version": "0.2.0",
            "providers": [
                "health",
                "tracearr",
                "unraid",
                "ipmi",
                "endpoints"
            ],
            "status": "running"
        }
    )


if __name__ == "__main__":

    logger.info(
        "Starting Homepage Helpers on port %s",
        PORT
    )

    logger.info(
        "JSON sort keys: %s",
        app.json.sort_keys
    )

    app.run(
        host="0.0.0.0",
        port=PORT
    )
