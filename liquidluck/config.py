# coding: utf-8
"""
    liquidluck.config
    ~~~~~~~~~~~~~~~~~

    Load and parse config for liquidluck

    :copyright: (c) 2013 by Hsiaoming Yang
"""

import os


class Option(dict):
    """Dict object class for storing data."""

    _defaults = {
        'source_directory': 'content',
        'output_directory': '_site',
    }

    def __getattr__(self, key):
        if key in self:
            return self[key]
        if key in self._defaults:
            return self._defaults[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError


# liquidluck directory
_directory_ = os.path.abspath(os.path.dirname(__file__))

# default configuration
theme = os.path.join(_directory_, '_themes', 'default')
theme_gallery = os.path.expanduser('~/.liquidluck-themes')


def parse_config_file(filepath):
    """Parse from a config file into object.

    :param filepath: filepath of the config file
    """
    if filepath.endswith('.py'):
        filetype = 'python'
    elif filepath.endswith('.json'):
        filetype = 'json'
    else:
        filetype = 'yaml'

    def parse_python(filepath):
        config = {}
        execfile(filepath, {}, config)
        return config

    def parse_yaml(filepath):
        from yaml import load
        try:
            from yaml import CLoader as Loader
        except ImportError:
            from yaml import Loader

        with open(filepath) as f:
            return load(f, Loader)

    def parse_json(filepath):
        try:
            import json
        except ImportError:
            import simplejson as json

        with open(filepath) as f:
            return json.load(f)

    if filetype == 'python':
        return parse_python(filepath)
    elif filetype == 'json':
        return parse_json(filepath)
    return parse_yaml(filepath)
