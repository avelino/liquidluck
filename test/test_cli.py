#!/usr/bin/env python

import os.path
from liquidluck.cli import load_settings

ROOT = os.path.abspath(os.path.dirname(__file__))


def test_load_settings():
    path = os.path.join(ROOT, 'source/settings.py')
    load_settings(path)

    from liquidluck.options import settings
    assert settings.author == 'lepture'
