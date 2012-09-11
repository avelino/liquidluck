#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
PROJDIR = os.path.abspath(os.path.dirname(__file__))
import sys
import logging
from liquidluck.options import g, settings
from liquidluck.utils import import_object, walk_dir

from liquidluck.writers.base import load_jinja


def load_settings(path):
    cwd = os.path.split(os.path.abspath(path))[0]
    sys.path.insert(0, cwd)

    def load_py_settings(path):
        config = {}
        execfile(path, {}, config)

        for key in config:
            setting = config[key]
            if isinstance(setting, dict) and key in settings:
                settings[key].update(setting)
            else:
                settings[key] = setting

    def load_yaml_settings(path):
        pass

    def load_json_settings(path):
        pass

    #: preload default config
    load_py_settings(os.path.join(PROJDIR, 'tools', '_settings.py'))

    if path.endswith('.py'):
        load_py_settings(path)
    elif path.endswith('.json'):
        load_json_settings(path)
    else:
        load_yaml_settings(path)

    g.output_directory = os.path.abspath(settings.config.get('output'))
    g.static_directory = os.path.abspath(settings.config.get('static'))
    logging.info('Load Settings Finished')


def load_posts(path):
    g.source_directory = path
    readers = []
    for name in settings.reader.get('active'):
        readers.append(import_object(name))

    def detect_reader(filepath):
        for Reader in readers:
            reader = Reader(filepath)
            if reader.support():
                return reader.run()
        return None

    for filepath in walk_dir(path):
        post = detect_reader(filepath)
        if not post:
            g.pure_files.append(filepath)
        elif not post.date:
            g.pure_pages.append(post)
        elif post.public:
            g.public_posts.append(post)
        else:
            g.secure_posts.append(post)

    g.public_posts = sorted(g.public_posts, key=lambda o: o.date, reverse=True)
    g.secure_posts = sorted(g.secure_posts, key=lambda o: o.date, reverse=True)

    logging.info('Load Posts Finished')


def write_posts():
    writers = []
    for name in settings.writer.get('active'):
        writers.append(import_object(name)())

    load_jinja()

    for writer in writers:
        writer.run()


def build(config='settings.py'):
    load_settings(config)
    load_posts(settings.config.get('source'))
    write_posts()
