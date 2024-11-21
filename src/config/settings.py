import os
from pathlib import Path
import logging.config

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = os.path.join(BASE_DIR, "db/book.json")
TEST_DB_PATH = os.path.join(BASE_DIR, "db/book_test.json")

# LOGGING
log_config = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "[%(levelname)s]: %(asctime)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "streamLogger": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": "no"
        }
    }
}

logging.config.dictConfig(log_config)
