"""
IPMI provider for Homepage Helpers.

Requires:
- queries/ipmi_sensors.json
- freeipmi (ipmi-sensors command available in container)

Endpoints:
/ipmi/sensors
"""

import ipaddress
import json
import logging
import os
import re
import subprocess

from pathlib import Path

from flask import Blueprint
from flask import jsonify


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Blueprint
# -----------------------------------------------------------------------------

ipmi_bp = Blueprint(
    "ipmi",
    __name__,
    url_prefix="/ipmi"
)


# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent.parent / "config"

IPMI_SENSOR_HOST = os.getenv(
    "IPMI_SENSOR_HOST"
)

IPMI_SENSOR_USERNAME = os.getenv(
    "IPMI_SENSOR_USERNAME"
)

IPMI_SENSOR_PASSWORD = os.getenv(
    "IPMI_SENSOR_PASSWORD"
)


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

def load_config():

    with open(
        BASE_DIR / "ipmi_sensors.json", "r", encoding="utf-8") as f:

        return json.load(f)


# -----------------------------------------------------------------------------
# Validation
# -----------------------------------------------------------------------------

def validate_host(host):

    try:
        ipaddress.ip_address(host)
        return True

    except ValueError:
        return False


def validate_username(username):

    return re.match(
        r"^[a-zA-Z0-9._\-]+$",
        username
    )


# -----------------------------------------------------------------------------
# Business logic
# -----------------------------------------------------------------------------

def get_sensors():

    host = IPMI_SENSOR_HOST
    username = IPMI_SENSOR_USERNAME
    password = IPMI_SENSOR_PASSWORD

    # -------------------------------------------------------------------------
    # Configuration validation
    # -------------------------------------------------------------------------

    if not host:
        raise ValueError(
            "IPMI_SENSOR_HOST not configured"
        )

    if not username:
        raise ValueError(
            "IPMI_SENSOR_USERNAME not configured"
        )

    if not password:
        raise ValueError(
            "IPMI_SENSOR_PASSWORD not configured"
        )

    if not validate_host(host):
        raise ValueError(
            f"Invalid IPMI host: {host}"
        )

    if not validate_username(username):
        raise ValueError(
            f"Invalid IPMI username: {username}"
        )

    # -------------------------------------------------------------------------
    # Load sensor configuration
    # -------------------------------------------------------------------------

    config = load_config()

    wanted_temps = config.get(
        "temperatures",
        []
    )

    wanted_fans = config.get(
        "fans",
        []
    )

    # -------------------------------------------------------------------------
    # Build IPMI command
    # -------------------------------------------------------------------------

    cmd = [
        "ipmi-sensors",
        "--hostname", host,
        "--username", username,
        "--password", password,
        "--quiet-cache"
    ]

    logger.info(
        "Fetching IPMI sensors from %s",
        host
    )

    # -------------------------------------------------------------------------
    # Execute command
    # -------------------------------------------------------------------------

    try:

        result = subprocess.check_output(
            cmd,
            text=True
        )

    except Exception as e:

        logger.error(
            "IPMI sensor retrieval failed for host %s: %s",
            host,
            e
        )

        raise

    # -------------------------------------------------------------------------
    # Parse output
    # -------------------------------------------------------------------------

    temperatures = {}
    fans = {}

    for line in result.splitlines():

        if "|" not in line:
            continue

        parts = [
            p.strip()
            for p in line.split("|")
        ]

        if len(parts) < 5:
            continue

        name = parts[1]
        reading = parts[3]

        if reading in ["N/A", ""]:
            continue

        try:
            value = float(reading)

        except ValueError:
            continue

        if name in wanted_temps:

            key = (
                name.lower()
                .replace(" temp", "")
                .replace(" ", "_")
            )

            temperatures[key] = value

        elif name in wanted_fans:

            key = (
                name.lower()
                .replace(" ", "_")
            )

            fans[key] = value

    logger.info(
        "Collected %d temperature sensors and %d fan sensors from %s",
        len(temperatures),
        len(fans),
        host
    )

    # -------------------------------------------------------------------------
    # Return response
    # -------------------------------------------------------------------------

    return {
        "temperatures": temperatures,
        "fans": fans
    }



# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

@ipmi_bp.route(
    "/sensors"
)
def sensors():

    logger.info(
        "IPMI sensors requested"
    )

    return jsonify(
        get_sensors()
    )
