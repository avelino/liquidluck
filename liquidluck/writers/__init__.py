#!/usr/bin/env python

alias = {
    'post': 'liquidluck.writers.core.PostWriter',
    'page': 'liquidluck.writers.core.PageWriter',
    'archive': 'liquidluck.writers.core.ArchiveWriter',
    'archive_feed': 'liquidluck.writers.core.ArchiveFeedWriter',
    'file': 'liquidluck.writers.core.FileWriter',
    'static': 'liquidluck.writers.core.StaticWriter',

    'year': 'liquidluck.writers.extends.YearWriter',
    'tag': 'liquidluck.writers.extends.TagWriter',
    'category': 'liquidluck.writers.extends.CategoryWriter',
    'category_feed': 'liquidluck.writers.extends.CategoryFeedWriter',
}
