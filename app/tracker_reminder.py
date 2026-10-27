"""Send a random tracker-update reminder to a Google Chat incoming webhook."""
from __future__ import annotations

import logging
import os
import random
import sys

import requests

LOGGER = logging.getLogger("tracker_reminder")

MESSAGES = [
    'Kindly update the tracker with your notes.',
    'Please update the tracker with your notes.',
    'Could you please update the tracker with your notes?',
    'Kindly add your notes to the tracker.',
    'Please include your notes in the tracker.',
    'Could you kindly record your notes in the tracker?',
    'Please enter your observations in the tracker.',
    'Kindly document your comments in the tracker.',
    'Could you please capture your notes in the tracker?',
    'Kindly ensure the tracker is updated with your notes.',
    'Please ensure your notes are reflected in the tracker.',
    'Please ensure all your comments are documented in the tracker.',
    'Please add any relevant comments to the tracker.',
    'Please update the tracker with your inputs.',
    'Kindly add your comments to the tracker.',
    'Please add your Notes to the tracker.',
    'Please capture your inputs in the tracker.',
    'Add your notes to the tracker, please.',
    'Please update the tracker with your notes at your earliest convenience.',
    'Kindly complete the tracker update with your comments.',
    'Please make sure your notes are added to the tracker.',
    'Please ensure the tracker reflects your latest comments.',
    'Kindly ensure your Notes is captured in the tracker.',
]

# Emoji appearance and colors vary by operating system and chat client.
STAR_EMOJIS = ["⭐", "🌟", "✨", "💫", "🔯", "🌠"]


def configure_logging() -> None:
    """Write logs to stdout so Docker captures them with `docker logs`."""
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, None)
    if not isinstance(level, int):
        level = logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
        stream=sys.stdout,
        force=True,
    )


def send_random_tracker_reminder() -> None:
    """Select and send one reminder. Raises on configuration/network failures."""
    LOGGER.info("Tracker reminder program started.")
    webhook_url = os.getenv("CHAT_WEBHOOK_URL", "").strip()
    if not webhook_url:
        LOGGER.error(
            "Required environment variable CHAT_WEBHOOK_URL is missing or empty. "
            "Set it in the environment or in the .env file before running."
        )
        raise RuntimeError("CHAT_WEBHOOK_URL is missing or empty.")

    timeout_raw = os.getenv("CHAT_REQUEST_TIMEOUT_SECONDS", "30")
    try:
        timeout = int(timeout_raw)
        if timeout <= 0:
            raise ValueError
    except ValueError:
        LOGGER.error(
            "CHAT_REQUEST_TIMEOUT_SECONDS=%r is invalid; use a positive integer.",
            timeout_raw,
        )
        raise ValueError("CHAT_REQUEST_TIMEOUT_SECONDS must be a positive integer.")

    message = random.choice(MESSAGES)
    star = random.choice(STAR_EMOJIS)
    chat_message = f"{star} {message}"
    LOGGER.info("Selected one of %d available reminder messages.", len(MESSAGES))
    LOGGER.info("Sending reminder to Google Chat.")

    try:
        response = requests.post(
            webhook_url, json={"text": chat_message}, timeout=timeout
        )
        response.raise_for_status()
    except requests.RequestException:
        LOGGER.exception("Google Chat notification failed.")
        raise

    LOGGER.info(
        "Google Chat notification delivered successfully (HTTP %s).",
        response.status_code,
    )
    LOGGER.info("Sent message: %s", chat_message)


def main() -> int:
    configure_logging()
    try:
        send_random_tracker_reminder()
    except (RuntimeError, ValueError, requests.RequestException):
        LOGGER.error("Tracker reminder run failed.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
