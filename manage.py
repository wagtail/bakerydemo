#!/usr/bin/env python
import os
import sys

import dotenv


if __name__ == "__main__":
    dotenv.read_dotenv()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bakerydemo.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
