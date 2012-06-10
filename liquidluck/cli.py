#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from liquidluck.options import enable_pretty_logging
from liquidluck.options import g, settings

#: prepare liquidluck config
g.root_directory = os.path.abspath(os.path.dirname(__file__))


def load_settings(path):
    execfile(path, settings, settings)
    #: TODO config default settings
    config = {
        'slug_format': '{{category}}/{{filename}}.html',
    }

    for key in config:
        if key not in settings:
            settings[key] = config[key]


def main():
    parser = argparse.ArgumentParser(prog='liquidluck')

    parser.add_argument('--disable-log', action='store_true',
                        dest='disable_log')

    args = parser.parse_args()
    if args.disable_log:
        enable_pretty_logging('warn')
    else:
        enable_pretty_logging()
