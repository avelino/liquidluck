
import os
from liquidluck.ns import namespace

class Reader(object):
    """
    Base Reader, all readers must inherit this module. e.g.:

        ``RstReader(Reader)``

    New reader required:
        - ``support_type``
        - ``parse_post``

    New reader optional:
        - ``get_filters``
        - ``get_context``
    """
    def __init__(self, filepath=None):
        self.filepath = filepath

    @classmethod
    def get_filters(self):
        return {}

    @classmethod
    def get_context(self):
        return {}

    def get_resource_path(self):
        return self.filepath

    def get_resource_mtime(self):
        return os.stat(self.filepath).st_mtime

    def get_resource_basename(self):
        folder, filename = os.path.split(self.filepath)
        basename, ext = os.path.splitext(filename)
        return basename

    def get_resource_destination(self):
        _format = namespace.site.get('format', 'year')
        post = self.parse_post()
        filename = self.get_resource_basename() + '.html'
        year = str(post.date.year)
        month = str(post.date.month)
        day = str(post.date.day)
        if _format == 'year':
            return os.path.join(year, filename)
        if _format == 'month':
            return os.path.join(year, month, filename)
        if _format == 'day':
            return os.path.join(year, month, day, filename)
        if hasattr(post, 'folder'):
            return os.path.join(post.folder, filename)
        return filename

    def get_resource_slug(self):
        return self.get_resource_destination()

    def support_type(self):
        return None

    def support(self):
        _type = self.support_type()
        if isinstance(_type, basestring):
            return self.filepath.endswith('.' + _type)
        if isinstance(_type, list) or isinstance(_type, tuple):
            for _t in _type:
                if isinstance(_t, basestring) and self.filepath.endswith('.' + _t):
                    return True
        return False


    def render(self):
        post = self.parse_post()

        post.mtime = self.get_resource_mtime()
        post.destination = self.get_resource_destination()
        post.slug = self.get_resource_slug()
        if not post.get('author', None):
            post.author = namespace.context.get('author', 'admin')
        return post

    def parse_post(self):
        raise NotImplementedError
