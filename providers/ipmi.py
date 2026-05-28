import subprocess


WANTED_SENSORS = {
    "CPU Temp": "cpu",
    "System Temp": "system",
    "Peripheral Temp": "peripheral",
    "FAN2": "fan2",
    "FAN3": "fan3",
    "FAN4": "fan4",
    "FAN5": "fan5",
    "FANB": "fanb"
}


def get_sensors():
    result = subprocess.check_output(
        ["/usr/sbin/ipmi-sensors"],
        text=True
    )

    temperatures = {}
    fans = {}

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

        if name not in WANTED_SENSORS:
            continue

        key = WANTED_SENSORS[name]

        try:
            value = float(reading)

            if "Temp" in name:
                temperatures[key] = value

            elif "FAN" in name:
                fans[key] = value

        except ValueError:
            continue

    return {
        "temperatures": temperatures,
        "fans": fans
    }