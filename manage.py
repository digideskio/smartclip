#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "smartclip.settings.vagrant")

    from django.core.management import execute_from_command_line

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'smartclip.settings.testing'
        
    execute_from_command_line(sys.argv)
