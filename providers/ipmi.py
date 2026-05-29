import json
import subprocess
from pathlib import Path


BASE = Path(__file__).parent.parent / "queries"


def load_config():
    with open(BASE / "ipmi_sensors.json") as f:
        return json.load(f)


def get_sensors(host, username, password):

    config = load_config()

    cmd = [
        "ipmi-sensors",
        "--hostname", host,
        "--username", username,
        "--password", password,
        "--quiet-cache"
    ]

    result = subprocess.check_output(
        cmd,
        text=True
    )

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