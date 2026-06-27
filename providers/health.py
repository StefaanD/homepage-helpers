"""
Health checker for Homepage Helpers.

Requires:

Endpoints:
/health
"""

import logging

from flask import Blueprint # type: ignore
from flask import jsonify # type: ignore


logger = logging.getLogger(__name__)


health_bp = Blueprint(
    "health",
    __name__,
    url_prefix="/health"
)


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

@health_bp.route(
    ""
)
def health():
    """
    General health check endpoint.
    """

    logger.info(
        "Health check requested"
    )

    return jsonify(
        {
            "status": "ok"
        }
    )
