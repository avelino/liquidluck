import os


DEFAULT_SETTING = """
# permalink settings
# http://liquidluck.readthedocs.org/en/latest/config.html#permalink
#
# Examples:
# {{filename}}.html
# {{date.year}}/{{filename}}.html
# {{date.year}}/{{date.month}}/{{filename}}.html
# {{category}}/{{filename}}.html
permalink = '{{date.year}}/{{filename}}'

# if you want to use relative url, set it to True
use_relative_url = False

# how many posts can be in one page
perpage = 30

# how many posts can be in a feed
feedcount = 20
timezone = "+00:00"

# default author
# you can set the author in your post::
#
# - author: yourname
#
author = 'nickname'  # choose a nickname

# multi author support
# http://liquidluck.readthedocs.org/en/latest/config.html#multiple-authors
# authors = {
#     'nickname': {
#         'name': 'Full Name',
#         'email': 'admin@example.com',
#         'website': 'http://example.com',
#     },
# }


theme = 'default'
# theme variables are defined by theme creator
# find all the theme variables in the theme settings.py file
theme_variables = {}

# http://liquidluck.readthedocs.org/en/latest/config.html#readers
# readers = {
    # if you want to enable reStructuredText, uncomment this line
    # and you need install doctutils by yourself
    # 'rst': 'liquidluck.readers.restructuredtext.RestructuredTextReader',
# }
readers_variables = {}

# http://liquidluck.readthedocs.org/en/latest/config.html#writers
# writers = {
#     # the writers enabled by default
#     # 'post': 'liquidluck.writers.core.PostWriter',
#     # 'page': 'liquidluck.writers.core.PageWriter',
#     # 'archive': 'liquidluck.writers.core.ArchiveWriter',
#     # 'archive_feed': 'liquidluck.writers.core.ArchiveFeedWriter',
#     # 'file': 'liquidluck.writers.core.FileWriter',
#     # 'static': 'liquidluck.writers.core.StaticWriter',
#     # 'year': 'liquidluck.writers.core.YearWriter',
#     # 'tag': 'liquidluck.writers.core.TagWriter',
#     # 'category': 'liquidluck.writers.core.CategoryWriter',
#     # 'category_feed': 'liquidluck.writers.core.CategoryFeedWriter',
#
#     # you can disable a writer with:
#     # 'year': None,
# }
writers_variables = {}

# template_variables = {}
# template_filters = {}
"""


def create(config):
    #: require site information
    site_name = raw_input("Site Name: ")
    site_url = raw_input("Site URL: ")
    code = (
        '#!/usr/bin/env python\n'
        '# -*- coding: utf-8 -*-\n\n'
        "site = {\n"
        '    "name": "%s",\n'
        '    "url": "%s",\n'
        '    # "prefix": "blog",\n'
        '}\n\n'
    ) % (site_name, site_url)

    source = raw_input("What is your directory for posts(content): ")
    source = source or 'content'
    code += "source = '%s'\n" % source
    if not os.path.isdir(source):
        os.makedirs(source)

    output = raw_input("Where is your directory for output(deploy): ")
    output = output or 'deploy'
    code += "output = '%s'\n" % output
    code += "static_output = '%s/static'\n" % output
    code += "static_prefix = '/static/'\n"
    code += DEFAULT_SETTING

    f = open(config, 'w')
    f.write(code)
    f.close()
    print("\nYour site is created.\n\n\n")
    print("Get help: http://liquidluck.readthedocs.org")
