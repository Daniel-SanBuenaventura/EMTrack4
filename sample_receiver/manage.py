#!/usr/bin/env python
import logging
import os
import signal
import sys

logger = logging.getLogger(__name__)


def sighandler(signum, frame):
    logger.error(f"Graceful shutdown. Signal number: {signum}")
    sys.exit(1)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "external_receiver.settings")
    signal.signal(signal.SIGTERM, sighandler)
    signal.signal(signal.SIGINT, sighandler)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
