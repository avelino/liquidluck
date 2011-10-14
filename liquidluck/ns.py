
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
namespace.site = NameSpace()
namespace.context = NameSpace()
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
    'xmldatetime': 'liquidluck.utils.xmldatetime',
})
