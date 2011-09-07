#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from liquidluck.config import Config

default_writers = [
    'liquidluck.writers.StaticWriter',
    'liquidluck.writers.PostWriter',
]
def apply_writer(writer_name):
    writers = writer_name.split('.')
    if len(writers) == 1:
        return __import__(writer_name)

    package = __import__('.'.join(writers[:-1]))
    for module in writers[1:]:
        package = getattr(package, module)
    return package

def main():
    begin = time.time()
    cwd = os.getcwd()
    config = Config(os.path.join(cwd, '.config'))
    writers = [name for name in config.writers.itervalues()]
    writers.extend(default_writers)
    for writer in writers:
        writer = apply_writer(writer)
        writer(config, cwd).register()
    for writer in writers:
        writer = apply_writer(writer)
        writer(config, cwd).run()
    end = time.time()

    print end - begin

if '__main__' == __name__:
    main()
