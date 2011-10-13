#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import shutil
import argparse
from liquidluck.config import Config
from liquidluck.utils import import_module
from liquidluck import logger

ROOT = os.path.dirname(__file__)

default_config = """[site]
postdir = content
deploydir = deploy
template = _templates
staticdir = _static
static_prefix = /_static
perpage = 20

[context]
author = lepture
sitename = Just lepture
siteurl = http://lepture.com
feed = http://feeds.lepture.com/lepture
gcse = 017842580319746762888:cqrgmcc2vg0

[writers]
static = liquidluck.writers.default.StaticWriter
post = liquidluck.writers.default.PostWriter
archive = liquidluck.writers.default.IndexWriter
year = liquidluck.writers.default.YearWriter
tag = liquidluck.writers.default.TagWriter
folder = liquidluck.writers.default.FolderWriter
"""

def apply_writer(writer_name):
    logger.info('Apply writer: ' + writer_name)
    return import_module(writer_name)

def build(config):
    cwd = os.getcwd()
    config_file = os.path.join(cwd, config)
    if  not os.path.exists(config_file):
        answer = raw_input('This is not a Felix Felicis repo, would you like to create one?(Y/n) ')
        if 'n' == answer.lower():
            sys.exit(1)
            return
        return create()

    config = Config(config_file)
    begin = time.time()
    writers = [apply_writer(writer) for writer in config.writers.itervalues()]
    for writer in writers:
        writer(config, cwd).register()

    for writer in writers:
        writer(config, cwd).run()
    end = time.time()

    print end - begin

def create(config='config.ini'):
    cwd = os.getcwd()
    config_file = os.path.join(cwd, config)
    f = open(config_file, 'w')
    f.write(default_config)
    f.close()
    config = Config(config_file)
    shutil.copytree(os.path.join(ROOT, '_static'), os.path.join(cwd, config.get('staticdir')))
    shutil.copytree(os.path.join(ROOT, '_templates'), os.path.join(cwd, config.get('template')))
    os.makedirs(os.path.join(cwd, config.get('postdir')))
    print 'Felix Felicis Repo Created'
    return

def main():
    parser = argparse.ArgumentParser(
        prog='liquidluck',
        description='Felix Felicis, aka liquidluck, is a static weblog generator',
    )
    parser.add_argument('-f', '--config', dest='config', default='config.ini', metavar='config.ini')
    parser.add_argument('-c', '--command', dest='command', default='build', metavar='build')
    args = parser.parse_args()

    if 'build' == args.command:
        build(args.config)
    elif 'create' == args.command: 
        create(args.config)

if '__main__' == __name__:
    main()
