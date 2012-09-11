# -*- coding: utf-8 -*-

author = {
    'default': 'lepture',
}

config = {
    'source': 'post',
    'output': 'build/deploy',
    'static': 'build/deploy/static',
}

#: active readers
reader = {
    'active': [
        'liquidluck.readers.markdown.MarkdownReader',
        'liquidluck.readers.restructuredtext.RestructuredTextReader',
    ],
}

#: active writers
writer = {
    'active': [
        'liquidluck.writers.core.PostWriter',
        'liquidluck.writers.core.PageWriter',
        'liquidluck.writers.core.ArchiveWriter',
        'liquidluck.writers.core.ArchiveFeedWriter',
        'liquidluck.writers.core.FileWriter',
        'liquidluck.writers.core.StaticWriter',
        'liquidluck.writers.core.YearWriter',
        'liquidluck.writers.core.CategoryWriter',
        'liquidluck.writers.core.CategoryFeedWriter',
        'liquidluck.writers.core.TagCloudWriter',
    ],
    'vars': {
        'archive_output': 'archive.html',
    }
}
