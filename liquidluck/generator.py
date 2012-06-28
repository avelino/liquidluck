#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from liquidluck.options import g, settings
from liquidluck.utils import import_object, walk_dir

from liquidluck.writers.base import load_jinja


def load_settings(path):
    config = {}
    execfile(path, {}, config)

    for key in config:
        setting = config[key]
        if isinstance(setting, dict):
            settings[key].update(setting)
        else:
            settings[key] = setting

    g.output_directory = os.path.abspath(settings.output)
    g.static_directory = os.path.abspath(settings.static_output)
    logging.info('Load Settings Finished')


def load_posts(path):
    g.source_directory = path
    readers = []
    for name in settings.readers:
        reader = settings.readers[name]
        if reader:
            readers.append(import_object(reader))

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
    for name in settings.writers:
        writer = settings.writers[name]
        if writer:
            writers.append(import_object(writer)())

    load_jinja()

    for writer in writers:
        writer.run()


def build(config='settings.py'):
    load_settings(config)
    load_posts(settings.source)
    write_posts()
