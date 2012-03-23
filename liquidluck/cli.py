#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import shutil
import argparse
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

import liquidluck
from liquidluck.namespace import ns
if '--disable-log' in sys.argv:
    ns.disable_log = True
from liquidluck.utils import import_module, walk_dir, UnicodeDict
from liquidluck import logger
from liquidluck.readers import detect_reader

ns.storage.root = os.path.dirname(__file__)


def make_notify():
    logger.warn("Important!!!!!")
    logger.warn("sourcecode in markdown changed to the new mark")
    logger.warn("using ```python instead of [sourcecode:python]")
    logger.warn("using ``` to end the code block instead of [/sourcecode]")


def init_config(filepath):
    config = ConfigParser()
    config.read(filepath)
    for sec in config.sections():
        if sec in ('site', 'context', 'writers', 'readers', 'filters'):
            ns[sec].update(config.items(sec))
        elif '_data' in sec:
            ns.data[sec] = UnicodeDict(config.items(sec))
        else:
            ns.sections[sec] = UnicodeDict(config.items(sec))
    return config


def init_post(projectdir):
    ns.storage.projectdir = projectdir
    postdir = os.path.join(ns.storage.projectdir,
                           ns.site.postdir)
    for f in walk_dir(postdir):
        reader = detect_reader(f)
        if reader:
            post = reader.render()
            if post:
                # ignore invalid post
                ns.storage.posts.append(post)
        else:
            ns.storage.files.append(f)

    ns.storage.posts = sorted(
        ns.storage.posts, key=lambda o: o.date, reverse=True)
    ns.storage.public_posts = filter(
        lambda post: post.public, ns.storage.posts)
    return ns


def generate():
    for reader in ns.readers.values():
        if reader:
            import_module(reader)().start()

    for writer in ns.writers.values():
        if writer:
            import_module(writer)().start()

    for writer in ns.writers.values():
        if writer:
            import_module(writer)().run()


def build(config_file):
    log = logger.Logger()
    begin = time.time()
    if not os.path.exists(config_file):
        answer = raw_input('This is not a Felix Felicis repo, '
                           'would you like to create one?(Y/n) ')
        if answer.lower() == 'n':
            sys.exit(1)
            return
        return create()

    init_config(config_file)
    init_post(os.getcwd())

    generate()

    for error in ns.storage.errors:
        log.error('Invalid Post: %s' % error)

    end = time.time()
    log.info('Total time: %s' % (end - begin))
    make_notify()
    return


def create(config_file='config.ini'):
    shutil.copy(os.path.join(ns.storage.root, 'config.ini'), config_file)
    init_config(config_file)
    cwd = os.getcwd()
    dest = os.path.join(cwd, ns.site.staticdir)
    if not os.path.exists(dest):
        shutil.copytree(os.path.join(ns.storage.root, '_static'), dest)
    dest = os.path.join(cwd, ns.site.template)
    if not os.path.exists(dest):
        os.makedirs(dest)
        for f in ('layout.html', 'archive.html', 'post.html', 'tagcloud.html'):
            shutil.copy(os.path.join(ns.storage.root, '_templates', f),
                        os.path.join(dest, f))
    dest = os.path.join(cwd, ns.site.postdir)
    if not os.path.exists(dest):
        os.makedirs(dest)
    print('Felix Felicis Repo Created')
    return


def main():
    parser = argparse.ArgumentParser(
        prog='liquidluck',
        description=('Felix Felicis, aka liquidluck,'
                     'is a static weblog generator'),
    )
    parser.add_argument('command', nargs='*', type=str, default='build',
                        metavar='command',
                        help='liquidluck commands: create, build etc.'
                       )
    parser.add_argument('-f', '--config', dest='config', default='config.ini',
                        metavar='config.ini')
    parser.add_argument('--disable-log', action='store_true')
    parser.add_argument('-v', '--version', action='store_true', dest='version')
    args = parser.parse_args()

    def run_command(cmd):
        if cmd == 'build':
            return build(args.config)
        if cmd == 'create':
            return create(args.config)
        config = init_config(args.config)
        if not config.has_section('commands'):
            return
        for k, v in config.items('commands'):
            if args.command == k:
                return import_module(v)(args.config)

    if args.version:
        print 'liquidluck (Felix Felicis) %s' % liquidluck.__version__
        return
    if isinstance(args.command, basestring):
        return run_command(args.command)
    if isinstance(args.command, list):
        for cmd in args.command:
            run_command(cmd)


if __name__ == '__main__':
    main()
