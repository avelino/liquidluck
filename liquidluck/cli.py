#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import os
import argparse
from liquidluck.options import enable_pretty_logging
from liquidluck.options import g, settings
from liquidluck.utils import import_object, walk_dir

from liquidluck.writers.base import load_jinja


def load_settings(path):
    config = {}
    execfile(path, {}, config)

    for key in config:
        settings[key] = config[key]

    load_jinja()


def load_posts(path):
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


def write_posts():
    writers = []
    for writer in settings.writers:
        writers.append(import_object(writer)())

    for writer in writers:
        writer.begin()

    for writer in writers:
        writer.run()


def main():
    parser = argparse.ArgumentParser(prog='liquidluck')

    parser.add_argument('--disable-log', action='store_true',
                        dest='disable_log')

    args = parser.parse_args()
    if args.disable_log:
        enable_pretty_logging('warn')
    else:
        enable_pretty_logging()


if __name__ == '__main__':
    main()
