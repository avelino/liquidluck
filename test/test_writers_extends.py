#!/usr/bin/env python

import os
from liquidluck.writers.extends import YearWriter
from liquidluck.options import settings

ROOT = os.path.abspath(os.path.dirname(__file__))


class TestArchiveWriter(object):
    def test_run(self):
        writer = YearWriter()
        writer.run()
        f = os.path.join(os.getcwd(), settings.deploydir, '2012/index.html')
        assert os.path.exists(f)
