#!/usr/bin/env python

import os
from liquidluck.writers.contrib import _404Writer
from liquidluck.options import g


class Test404Writer(object):
    def test_start(self):
        writer = _404Writer()
        writer.start()
        f = os.path.join(g.output_directory, '404.html')
        assert os.path.exists(f)
