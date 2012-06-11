#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import os
import argparse
from liquidluck.options import enable_pretty_logging
from liquidluck.options import g, settings
from liquidluck.utils import import_object, walk_dir


def load_settings(path):
    config = {}
    execfile(path, {}, config)

    for key in config:
        settings[key] = config[key]


def load_posts(path):
    g.post_directory = path
    readers = []
    for reader in settings.readers:
        readers.append(import_object(reader))

    def detect_reader(filepath):
        for Reader in readers:
            reader = Reader(filepath)
            if reader.support():
                return reader.render()
        return None

    for filepath in walk_dir(path):
        post = detect_reader(filepath)
        if not post:
            g.pure_files.append(filepath)
        elif post.public:
            g.public_posts.append(post)
        else:
            g.secure_posts.append(post)


def main():
    parser = argparse.ArgumentParser(prog='liquidluck')

    parser.add_argument('--disable-log', action='store_true',
                        dest='disable_log')

    args = parser.parse_args()
    if args.disable_log:
        enable_pretty_logging('warn')
    else:
        enable_pretty_logging()
