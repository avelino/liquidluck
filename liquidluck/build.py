# coding: utf-8
"""
    liquidluck.build
    ~~~~~~~~~~~~~~~~

    Liquidluck build program.

    :copyright: (c) 2013 by Hsiaoming Yang
"""

from .cache import Cache


class Builder(object):
    """The builder interface of liquidluck."""

    def __init__(self, argv=None, config=None):
        if argv:
            config = self._parse_command_line(argv)
        if not config:
            raise ValueError('No configuration')

        self._config = config
        self._cache = Cache(config.cachedir)

    def _parse_command_line(self, argv):
        pass

    def load_posts(self):
        pass

    def start_writers(self):
        pass

    def finish_writers(self):
        pass

    def run(self):
        self.load_posts()
        self.start_writers()
        self.finish_writers()
