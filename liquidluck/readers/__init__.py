import os

class Reader(object):
    def __init__(self, filepath,config):
        self.filepath = filepath
        self.config = config

    def get_resource_path(self):
        return self.filepath

    def get_resource_mtime(self):
        return os.stat(self.filepath).st_mtime

    def get_resource_basename(self):
        folder, filename = os.path.split(self.filepath)
        basename, ext = os.path.splitext(filename)
        return basename

    def get_resource_slug(self):
        slug = self.config.get('slug', 'html')
        source = self.get_resource_destination()
        basename, ext = os.path.splitext(source)
        if slug == 'clean':
            return basename
        if slug == 'slash':
            return basename + '/'
        return source

    def support(self):
        raise NotImplementedError

    def get_resource_destination(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError
