import os
import sys

import django
import pytest


def run_tests(*test_args):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_settings'
    django.setup()
    failures = pytest.main(*test_args)
    sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
