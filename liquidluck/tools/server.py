#!/usr/bin/env python

import os
import mimetypes
from liquidluck.options import g
from liquidluck.generator import load_settings
#from wsgiref.simple_server import make_server


def app(environ, start_response):
    path = environ['PATH_INFO']
    abspath = os.path.join(g.output_directory, path)
    headers = []
    mime_type, encoding = mimetypes.guess_type(abspath)
    if mime_type:
        headers.append(('Content-type', mime_type))
    else:
        headers.append(('Content-type', 'text/html'))

    start_response('200 OK', headers)


def detect(path):
    load_settings(path)
