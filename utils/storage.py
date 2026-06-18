"""
utils/storage.py
File I/O helpers — load and save the JSON database.
"""

import json
import os
import logging

DATA_FILE = os.path.join("data", "database.json")

logger = logging.getLogger(__name__)


def load_data() -> list[dict]:
    """
    Load user data from the JSON file.

    Returns an empty list if the file doesn't exist or is corrupted.
    """
    if not os.path.exists(DATA_FILE):
        logger.debug("Data file not found — returning empty list.")
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError as e:
        logger.warning("Malformed JSON in %s: %s — returning empty list.", DATA_FILE, e)
        return []
    except OSError as e:
        logger.error("Could not read %s: %s", DATA_FILE, e)
        return []


def save_data(data: list[dict]) -> bool:
    """
    Persist user data to the JSON file.

    Creates the data/ directory if it doesn't exist.
    Returns True on success, False on failure.
    """
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logger.debug("Saved %d user(s) to %s.", len(data), DATA_FILE)
        return True
    except OSError as e:
        logger.error("Could not write to %s: %s", DATA_FILE, e)
        return False
