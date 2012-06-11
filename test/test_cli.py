#!/usr/bin/env python

import os.path
from liquidluck.cli import load_settings, load_posts

ROOT = os.path.abspath(os.path.dirname(__file__))


def test_load_settings():
    path = os.path.join(ROOT, 'source/settings.py')
    load_settings(path)

    from liquidluck.options import settings, g
    assert settings.author == 'lepture'
    assert settings.perpage == 30

    assert g.jinja is not None


def test_load_posts():
    path = os.path.join(ROOT, 'source/settings.py')
    load_settings(path)

    load_posts(os.path.join(ROOT, 'source/post'))
    from liquidluck.options import g
    assert len(g.public_posts) > 0
