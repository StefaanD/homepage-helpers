"""
Endpoints provider for Homepage Helpers.

Endpoints:
/endpoints
"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import logging

from flask import Blueprint
from flask import current_app
from flask import jsonify

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Blueprint
# -----------------------------------------------------------------------------

endpoints_bp = Blueprint(
    "endpoints",
    __name__
)

# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

@endpoints_bp.route(
    "/endpoints"
)
def endpoints():
    """
    List all available endpoints.
    """

    logger.info(
        "Endpoints listing requested"
    )

    routes = []

    for rule in sorted(
        current_app.url_map.iter_rules(),
        key=lambda r: r.rule
    ):

        if rule.endpoint == "static":
            continue

        methods = sorted(
            method
            for method in rule.methods
            if method not in (
                "HEAD",
                "OPTIONS"
            )
        )

        routes.append({
            "path": rule.rule,
            "methods": methods
        })

    return jsonify(
        {
            "application": current_app.config["APP_NAME"],
            "version": current_app.config["APP_VERSION"],
            "total": len(routes),
            "endpoints": routes
        }
    )
