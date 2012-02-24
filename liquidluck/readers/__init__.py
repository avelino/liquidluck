
import os
from datetime import datetime
from liquidluck.utils import import_module
from liquidluck.namespace import ns
from liquidluck import logger


def detect_reader(filepath):
    for reader in ns.readers.values():
        reader = import_module(reader)(filepath)
        if reader.support():
            return reader
    return None


class Reader(object):
    """
    Base Reader, all readers must inherit this module. e.g.:

        ``RstReader(Reader)``

    New reader required:
        - ``support_type``
        - ``parse_post``

    New reader optional:
        - ``start``
    """
    def __init__(self, filepath=None):
        self.filepath = filepath

    def start(self):
        return None

    def get_relative_folder(self):
        postdir = os.path.join(ns.storage.projectdir,
                               ns.site.postdir)
        folder, filename = os.path.split(self.filepath.replace(postdir, ''))
        return folder.lstrip('/')

    def get_resource_basename(self):
        folder, filename = os.path.split(self.filepath)
        basename, ext = os.path.splitext(filename)
        return basename

    def get_resource_destination(self):
        _format = ns.site.format
        post = self.parse_post()
        if hasattr(post, 'ext'):
            filename = self.get_resource_basename() + '.' + post.ext
        else:
            filename = self.get_resource_basename() + '.html'
        year = str(post.date.year)
        month = str(post.date.month)
        day = str(post.date.day)
        if '/' in _format:
            path = ''
            dates = {'year': year, 'month': month, 'day': day}
            for attr in _format.split('/'):
                if attr in dates:
                    path = os.path.join(path, dates[attr])
                elif attr:
                    try:
                        path = os.path.join(path, getattr(post, attr))
                    except AttributeError:
                        logger.warn('Attribute %s Missing: %s'\
                                    % (attr, filename))
                        pass
            return os.path.join(path, filename)
        if _format == 'year':
            return os.path.join(year, filename)
        if _format == 'month':
            return os.path.join(year, month, filename)
        if _format == 'day':
            return os.path.join(year, month, day, filename)
        if hasattr(post, 'folder'):
            return os.path.join(post.folder, filename)
        return os.path.join(self.get_relative_folder(), filename)

    def get_resource_slug(self):
        return self.get_resource_destination().lower()

    def support_type(self):
        return None

    def support(self):
        _type = self.support_type()
        if isinstance(_type, basestring):
            return self.filepath.endswith('.' + _type)
        if isinstance(_type, list) or isinstance(_type, tuple):
            for _t in _type:
                if isinstance(_t, basestring) and \
                   self.filepath.endswith('.' + _t):
                    return True
        return False

    def _parse_datetime(sef, value):
        supported_formats = [
            '%a %b %d %H:%M:%S %Y',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M',
            '%Y-%m-%dT%H:%M',
            '%Y%m%d %H:%M:%S',
            '%Y%m%d %H:%M',
            '%Y-%m-%d',
            '%Y%m%d',
        ]
        for format in supported_formats:
            try:
                return datetime.strptime(value, format)
            except ValueError:
                pass
        logger.error('Unrecognized date/time: %r' % value)
        raise ValueError('Unrecognized date/time: %r' % value)

    def render(self):
        try:
            post = self.parse_post()
        except Exception as e:
            logger.error(e)
            ns.storage.errors.append(self.filepath)
            return None

        if not post or not post.get('date', None):
            ns.storage.errors.append(self.filepath)
            return None

        if not post.get('author', None):
            post.author = ns.context.get('author', 'admin')

        try:
            post.date = self._parse_datetime(post.get('date'))
        except ValueError as e:
            ns.storage.errors.append(self.filepath)
            return None

        for key in post.keys():
            if '_date' in key or '_time' in key:
                try:
                    post[key] = self._parse_datetime(post[key])
                except ValueError as e:
                    ns.storage.errors.append(self.filepath)
                    return None

        if post.get('public', 'true') == 'false':
            post.public = False
        else:
            post.public = True

        post.destination = self.get_resource_destination()
        post.slug = self.get_resource_slug()
        post.filepath = self.filepath
        return post

    def parse_post(self):
        raise NotImplementedError
