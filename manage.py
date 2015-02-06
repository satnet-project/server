#!/usr/bin/env python

from django.core import management
import os
import sys

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
    management.execute_from_command_line(sys.argv)
