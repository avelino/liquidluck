# coding: utf-8
"""
    liquidluck.config
    ~~~~~~~~~~~~~~~~~

    Load and parse config for liquidluck

    :copyright: (c) 2013 by Hsiaoming Yang
"""


# storing global configuration
_cache = {}

# default configuration
_defaults = {
}


def set(key, value):
    _cache[key] = value
    return _cache


def get(key):
    return _cache.get(key, _defaults.get(key))


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
