"""
IPMI provider for Homepage Helpers.

Requires:
- queries/ipmi_sensors.json
- freeipmi (ipmi-sensors command available in container)

Returns selected sensor values in JSON format for Homepage customapi widgets.
"""

import ipaddress
import json
import logging
import re
import subprocess
from pathlib import Path


logger = logging.getLogger(__name__)


BASE = Path(__file__).parent.parent / "queries"


def load_config():
    with open(BASE / "ipmi_sensors.json") as f:
        return json.load(f)


def validate_host(host):
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def validate_username(username):
    return re.match(r"^[a-zA-Z0-9._\-]+$", username)


def get_sensors(host, username, password):

    if not validate_host(host):
        raise ValueError("Invalid hostname")

    if not validate_username(username):
        raise ValueError("Invalid username")

    config = load_config()

    cmd = [
        "ipmi-sensors",
        "--hostname", host,
        "--username", username,
        "--password", password,
        "--quiet-cache"
    ]

    logger.info(f"Fetching IPMI sensors from {host}")

    try:
        result = subprocess.check_output(
            cmd,
            text=True
        )

    except Exception as e:
        logger.error(f"IPMI command failed: {e}")
        raise

    temperatures = {}
    fans = {}

    wanted_temps = config.get("temperatures", [])
    wanted_fans = config.get("fans", [])

    for line in result.splitlines():

        if "|" not in line:
            continue

        parts = [p.strip() for p in line.split("|")]

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

            key = name.lower()

            fans[key] = value

    return {
        "temperatures": temperatures,
        "fans": fans
    }