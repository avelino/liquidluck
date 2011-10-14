
import os
from liquidluck.ns import namespace

class Reader(object):
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

    def get_resource_slug(self):
        slug = namespace.site.get('slug', 'html')
        source = self.get_resource_destination()
        basename, ext = os.path.splitext(source)
        if slug == 'clean':
            return basename
        if slug == 'slash':
            return basename + '/'
        return source

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

    def get_resource_destination(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError
