#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from writer import Walker, Writer
from config import Config


def write():
    cwd = os.getcwd()
    config = Config(os.path.join(cwd, '.config'))
    writer = Writer(config, cwd) 
    writer.run()

if '__main__' == __name__:
    write()
