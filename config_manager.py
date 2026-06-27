"""
Configuration file management.
"""

import logging
import shutil

from pathlib import Path


logger = logging.getLogger(__name__)


DEFAULT_CONFIGS = [
    "tracearr_configuration.json",
    "ipmi_sensors.json",
    "unraid_stats.json",
    "unraid_updates.json"
]


def ensure_config_file(filename):
    """
    Copy default config file to appdata
    if it does not exist.
    """

    source = (
        Path("/app/config")
        / filename
    )

    destination = (
        Path("/config")
        / filename
    )

    if destination.exists():

        logger.info(
            "Config already exists: %s",
            filename
        )

        return

    shutil.copy2(
        source,
        destination
    )

    logger.info(
        "Created config file: %s",
        filename
    )


def ensure_config_files():
    """
    Ensure all config files exist.
    """

    for filename in DEFAULT_CONFIGS:

        ensure_config_file(
            filename
        )
