#!/usr/bin/env python

"""Writers from contributors
"""

import os
from liquidluck.options import g
from liquidluck.writers.base import BaseWriter


class _404Writer(BaseWriter):
    writer_name = '_404'

    def __init__(self):
        self._template = self.get('404_template', '404.html')

    def start(self):
        dest = os.path.join(g.output_directory, '404.html')
        self.render({}, self._template, dest)
