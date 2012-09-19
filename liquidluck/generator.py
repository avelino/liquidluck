#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
PROJDIR = os.path.abspath(os.path.dirname(__file__))
import sys
import logging
from liquidluck.options import g, settings
from liquidluck.utils import import_object, walk_dir, parse_settings
from liquidluck.writers.base import load_jinja, find_theme


def create_settings(filepath):
    if not filepath:
        filetype = raw_input(
            'Select a config format ([yaml], python, json):  '
        ) or 'yaml'

        if filetype not in ['yaml', 'python', 'json']:
            print('format not supported')
            return

        suffix = {'yaml': '.yml', 'python': '.py', 'json': '.json'}
        filepath = 'settings%s' % suffix[filetype]

    content = raw_input('posts folder (content): ') or 'content'
    output = raw_input('output folder (deploy): ') or 'deploy'
    if filepath.endswith('.py'):
        f = open(os.path.join(PROJDIR, 'tools', '_settings.py'))
        text = f.read()
        f.close()
    elif filepath.endswith('.json'):
        f = open(os.path.join(PROJDIR, 'tools', '_settings.json'))
        text = f.read()
        f.close()
    else:
        f = open(os.path.join(PROJDIR, 'tools', '_settings.yml'))
        text = f.read()
        f.close()

    text = text.replace('content', content)
    if content and not content.startswith('.') and not os.path.exists(content):
        os.makedirs(content)
    text = text.replace('deploy', output)
    f = open(filepath, 'w')
    f.write(text)
    f.close()


def find_settings(directory=None):
    if not directory:
        directory = os.getcwd()

    config = [
        'settings.yml', 'settings.json', 'settings.yaml', 'settings.py',
    ]

    for f in config:
        path = os.path.join(directory, f)
        if os.path.exists(path):
            return path

    return None


def load_settings(path=None):
    if not path:
        path = find_settings()

    def update_settings(arg):
        if isinstance(arg, dict):
            config = arg
        else:
            config = parse_settings(arg)
        for key in config:
            setting = config[key]
            if isinstance(setting, dict) and key in settings:
                settings[key].update(setting)
            else:
                settings[key] = setting

    #: preload default config
    update_settings(os.path.join(PROJDIR, 'tools', '_settings.py'))
    update_settings(path)

    g.output_directory = os.path.abspath(settings.config.get('output'))
    g.static_directory = os.path.abspath(settings.config.get('static'))
    logging.info('Load Settings Finished')

    sys.path.insert(0, find_theme())
    cwd = os.path.split(os.path.abspath(path))[0]
    sys.path.insert(0, cwd)


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
