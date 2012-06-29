#!/usr/bin/env python

import os
import mimetypes
from wsgiref.simple_server import make_server

PORT = 8000
ROOT = os.path.abspath('.')
PERMALINK = 'html'


def config(port=None, root=None, permalink=None):
    global PORT
    global ROOT
    global PERMALINK
    if port:
        PORT = int(port)

    if root:
        ROOT = os.path.abspath(root)

    if permalink:
        PERMALINK = permalink


def app(environ, start_response):
    global ROOT
    global PERMALINK
    path = environ['PATH_INFO'].lstrip('/')
    abspath = os.path.join(ROOT, path)
    headers = []
    mime_type, encoding = mimetypes.guess_type(abspath)
    if mime_type:
        headers.append(('Content-type', mime_type))
    else:
        headers.append(('Content-type', 'text/html'))

    filepath = abspath
    if abspath.endswith('/'):
        #: this is index
        filepath = os.path.join(abspath, 'index.html')
        if not os.path.exists(filepath) and PERMALINK == 'slash':
            filepath = abspath.rstrip('/') + '.html'

    elif not os.path.exists(abspath) and PERMALINK == 'clean':
        filepath = abspath + '.html'

    if not os.path.exists(filepath):
        start_response('404 Not Found', headers)
    else:
        start_response('200 OK', headers)

        f = open(filepath)
        for line in f:
            yield line
        f.close()


def start_server():
    global PORT
    print('Start server at 0.0.0.0:%s' % PORT)
    make_server('', PORT, app).serve_forever()


if __name__ == '__main__':
    start_server()
