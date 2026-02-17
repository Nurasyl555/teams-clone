#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    # Reads TEAMS_ENV_ID from settings/.env (or environment variable)
    # TEAMS_ENV_ID=local  → settings.env.local
    # TEAMS_ENV_ID=prod   → settings.env.prod
    from decouple import config
    env_id = config("TEAMS_ENV_ID", default="local")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"settings.env.{env_id}")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
