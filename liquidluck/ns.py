
__all__ = ['NameSpace', 'namespace']

class NameSpace(dict):
    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError

namespace = NameSpace.instance()


#defaults 
namespace.context = NameSpace()
namespace.status = NameSpace()
namespace.functions = NameSpace()
namespace.site = NameSpace({
    'postdir': 'content',
    'deploydir': 'deploy',
    'staticdir': 'static',
    'static_prefix': '/static',
    'template': '_templates',
    'format': 'year',
    'dateformat': '%Y-%m-%d',
    'timeformat': '%Y-%m-%d %H:%M:%S',
    'slug': 'html',
    'syntax': 'class',
    'autoescape': 'false',
    'feed_count': 10,
    'perpage': 30,
    'index': 'index.html',
    'feed_template': 'feed.xml',
    'archive_template': 'archive.html',
    'tagcloud_template': 'tagcloud.html',
})
namespace.readers = NameSpace({
    'mkd': 'liquidluck.readers.mkd.MarkdownReader',
    'rst': 'liquidluck.readers.rst.RstReader',
})
namespace.writers = NameSpace({
    'static': 'liquidluck.writers.default.StaticWriter',
    'post': 'liquidluck.writers.default.PostWriter',
    'file': 'liquidluck.writers.default.FileWriter',
    'archive': 'liquidluck.writers.default.IndexWriter',
    'year': 'liquidluck.writers.default.YearWriter',
    'tag': 'liquidluck.writers.default.TagWriter',
})
namespace.filters = NameSpace({
    'restructuredtext': 'liquidluck.readers.rst.restructuredtext',
    'markdown': 'liquidluck.readers.mkd.markdown',
    'xmldatetime': 'liquidluck.filters.xmldatetime',
    'embed': 'liquidluck.filters.embed',
})
