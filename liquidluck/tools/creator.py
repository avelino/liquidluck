import os


DEFAULT_SETTING = """
permalink = '{{category}}/{{filename}}.html'
perpage = 30
feedcount = 20

author = 'admin'  # choose a nickname
authors = {
    'admin': {
        'name': 'Full Name',
        'email': 'admin@example.com',
        'website': 'http://example.com',
    },
}


theme = 'default'
# theme variables are defined by theme creator
theme_variables = {}

# readers = {}
# readers_variables = {}
# writers = {}
# writers_variables = {}

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
