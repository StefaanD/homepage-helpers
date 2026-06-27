import os
import logging

from pathlib import Path
from logging.handlers import RotatingFileHandler


def configure_logging():

    log_dir = Path(
        os.getenv(
            "LOG_DIR",
            "/config/logs"
        )
    )

    log_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    log_file = (
        log_dir /
        "homepage-helpers.log"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=int(
            os.getenv(
                "LOG_MAX_SIZE",
                "10485760"
            )
        ),
        backupCount=int(
            os.getenv(
                "LOG_BACKUP_COUNT",
                "5"
            )
        )
    )

    file_handler.setFormatter(
        formatter
    )

    stream_handler = logging.StreamHandler()

    stream_handler.setFormatter(
        formatter
    )

    log_level = os.getenv(
        "LOG_LEVEL",
        "INFO"
    ).upper()

    logging.basicConfig(
        level=getattr(
            logging,
            log_level,
            logging.INFO
        ),
        handlers=[
            stream_handler,
            file_handler
        ],
        force=True
    )
