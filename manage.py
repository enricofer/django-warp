#!/usr/bin/env python
import os
import sys
import pathlib
current_dir = pathlib.Path(__file__).parent.absolute()

if __name__ == "__main__":
    #
    print ("current_dir",str(current_dir))
    sys.path.append(str(current_dir))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dw_test.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
