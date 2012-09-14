#!/usr/bin/env python

import os
import mimetypes
import logging
from wsgiref.simple_server import make_server
from liquidluck.options import g, settings
from liquidluck.utils import to_unicode, UnicodeDict
from liquidluck.generator import load_posts, write_posts
try:
    import tornado.web
    import tornado.escape
    import tornado.websocket
    RequestHandler = tornado.web.RequestHandler
    WebSocketHandler = tornado.websocket.WebSocketHandler
    escape = tornado.escape
except ImportError:
    print('Enable Livereload Server by installing tornado')
    escape = None
    RequestHandler = object
    WebSocketHandler = object


HOST = '127.0.0.1'
PORT = 8000
ROOT = os.path.abspath('.')
PERMALINK = 'html'
LIVERELOAD = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'livereload.js'
)


def config(port=None, root=None, permalink=None):
    global PORT
    global ROOT
    global PERMALINK

    if port and ':' in port:
        HOST, PORT = port.split(':')
    elif port:
        PORT = port

    if root:
        ROOT = os.path.abspath(root)

    if permalink:
        PERMALINK = permalink


def _autoindex(abspath):
    if not os.path.exists(abspath):
        return None
    html = '<ul>'
    files = os.listdir(abspath)
    for f in files:
        path = os.path.join(abspath, f)
        html += '<li>'
        if os.path.isdir(path):
            html += '<a href="%s/">%s</a>' % (f, f)
        else:
            html += '<a href="%s">%s</a>' % (f, f)

        html += '</li>'

    html += '</ul>'
    return html


def _read(abspath):
    filepath = abspath
    if abspath.endswith('/'):
        #: this is index
        filepath = os.path.join(abspath, 'index.html')
        if not os.path.exists(filepath) and PERMALINK == 'slash':
            filepath = abspath.rstrip('/') + '.html'
        elif not os.path.exists(filepath):
            return _autoindex(abspath)

    elif not os.path.exists(abspath):
        filepath = abspath + '.html'

    if not os.path.exists(filepath):
        return None

    f = open(filepath)
    content = f.read()
    f.close()
    return content


def wsgi_app(environ, start_response):
    path = environ['PATH_INFO'].lstrip('/')
    abspath = os.path.join(ROOT, path)
    headers = []
    mime_type, encoding = mimetypes.guess_type(abspath)
    if mime_type:
        headers.append(('Content-type', mime_type))
    else:
        headers.append(('Content-type', 'text/html'))

    body = _read(abspath)

    if body is None:
        start_response('404 Not Found', headers)
    else:
        start_response('200 OK', headers)
        yield body


class LiveReloadJSHandler(RequestHandler):
    def get(self):
        f = open(LIVERELOAD)
        content = to_unicode(f.read())
        content = content.replace('{{port}}', str(PORT))
        f.close()

        self.set_header('Content-Type', 'application/javascript')
        self.write(content)


class LiveReloadHandler(WebSocketHandler):
    waiters = set()
    _modified_times = {}
    _watch_running = False

    def allow_draft76(self):
        return True

    def on_close(self):
        if self in LiveReloadHandler.waiters:
            LiveReloadHandler.waiters.remove(self)

    def send_message(self, message):
        if isinstance(message, dict):
            message = escape.json_encode(message)

        try:
            self.write_message(message)
        except:
            logging.error('Error sending message', exc_info=True)

    def on_message(self, message):
        """Handshake with livereload.js

        1. client send 'hello'
        2. server reply 'hello'
        3. client send 'info'

        http://help.livereload.com/kb/ecosystem/livereload-protocol
        """
        message = UnicodeDict(escape.json_decode(message))
        if message.command == 'hello':
            handshake = {}
            handshake['command'] = 'hello'
            protocols = message.protocols
            protocols.append(
                'http://livereload.com/protocols/2.x-remote-control'
            )
            handshake['protocols'] = protocols
            handshake['serverName'] = 'livereload-tornado'
            self.send_message(handshake)

        if message.command == 'info' and 'url' in message:
            logging.info('Browser Connected: %s' % message.url)
            LiveReloadHandler.waiters.add(self)
            if not LiveReloadHandler._watch_running:
                LiveReloadHandler._watch_running = True
                logging.info('Start watching changes')
                tornado.ioloop.PeriodicCallback(self.watch_tasks, 500).start()

    def watch_tasks(self):
        if g.output_directory != ROOT:
            # not a liquidluck project
            if self._is_changed(ROOT):
                self.reload_browser()
            return

        if self._is_changed(g.source_directory, 4):
            # clean posts
            g.public_posts = []
            g.secure_posts = []
            g.pure_files = []
            g.pure_pages = []

            load_posts(settings.config['source'])
            write_posts()
            self.reload_browser()

        if self._is_changed(g.theme_directory):
            write_posts()
            self.reload_browser()

    def reload_browser(self):
        logging.info('Reload')
        msg = {
            'command': 'reload',
            'path': '*',
            'liveCSS': True
        }
        for waiter in LiveReloadHandler.waiters:
            try:
                waiter.write_message(msg)
            except:
                logging.error('Error sending message', exc_info=True)
                LiveReloadHandler.waiters.remove(waiter)

    def _is_changed(self, path, flags=0):
        def is_file_changed(path):
            if not os.path.isfile(path):
                return False

            _, ext = os.path.splitext(path)
            theme = settings.theme.get('vars') or {}

            ignores = theme.get('reload_ignore') or []
            ignores.extend(['.pyc', '.pyo', '.swp'])
            if flags > 0 and ext in ignores:
                return False

            matches = theme.get('reload_match') or []
            if flags > 1 and ext not in matches:
                return False

            modified = int(os.stat(path).st_mtime)

            if path not in self._modified_times:
                self._modified_times[path] = modified
                return False

            if path in self._modified_times and \
               self._modified_times[path] == modified:
                return False

            self._modified_times[path] = modified
            logging.info('file changed: %s' % path)
            return True

        for root, dirs, files in os.walk(path):
            if '.git' in dirs:
                dirs.remove('.git')
            if '.hg' in dirs:
                dirs.remove('.hg')
            if '.svn' in dirs:
                dirs.remove('.svn')

            for f in files:
                path = os.path.join(root, f)
                if is_file_changed(path):
                    return True

        return False


class IndexHandler(RequestHandler):
    def get(self, path='/'):
        abspath = os.path.join(os.path.abspath(ROOT), path.lstrip('/'))
        mime_type, encoding = mimetypes.guess_type(abspath)
        if not mime_type:
            mime_type = 'text/html'

        self.set_header('Content-Type', mime_type)

        body = _read(abspath)

        if body is None:
            self.send_error(404)
            return
        ua = self.request.headers.get("User-Agent", 'bot').lower()
        if 'msie' not in ua:
            body = body.replace(
                '</head>', '<script src="/livereload.js"></script></head>'
            )
        # disable google analytics
        body = body.replace('google-analytics.com/ga.js', '')
        self.write(body)


class ThemeStaticHandler(RequestHandler):
    def get(self, filepath):
        abspath = os.path.join(g.theme_directory, 'static', filepath)
        mime_type, encoding = mimetypes.guess_type(abspath)
        if not mime_type:
            mime_type = 'text/html'

        self.set_header('Content-Type', mime_type)
        if not os.path.exists(abspath):
            self.send_error(404)
            return

        f = open(abspath)
        for line in f:
            self.write(line)
        f.close()


def start_server():
    if RequestHandler is object:
        logging.info('Start server at %s:%s' % (HOST, PORT))
        make_server(HOST, int(PORT), wsgi_app).serve_forever()
    else:
        import tornado.web
        if g.output_directory == ROOT:
            #: if this is a liquidluck project, build the site
            load_posts(settings.config['source'])
            write_posts()
            logging.info('Theme directory: %s' % g.theme_directory)
        handlers = [
            (r'/livereload', LiveReloadHandler),
            (r'/livereload.js', LiveReloadJSHandler),
            (r'/theme/(.*)', ThemeStaticHandler),
            (r'(.*)', IndexHandler),
        ]
        app = tornado.web.Application(handlers=handlers, default_host=HOST)
        app.listen(int(PORT))
        logging.info('Start server at %s:%s' % (HOST, PORT))
        tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    start_server()
