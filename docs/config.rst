.. _configuration:


Configuration
==============

Default setting file is ``settings.py`` in your current working directory,
but you can specify another file with::

    $ liquidluck -s another-settings.py


Overview
----------

A demo setting file (settings.py)::

    # -*- coding: utf-8 -*-

    #: site information
    site = {
        'name': 'Just lepture',
        'url': 'http://lepture.com',
    }

    #: posts lay here
    source = 'content'

    #: generate html to ouput
    output = '_site'
    # static_output = '_site/static'

    #: theme, load theme from _themes
    theme = 'default'

    permalink = '{{date.year}}/{{filename}}.html'

    author = 'lepture'
    authors = {
        'lepture': {
            'name': 'Hsiaoming Yang',
            'website': 'http://lepture.com',
            'email': 'lepture@me.com',
        }
    }

    #: active readers
    # readers = {}

    #: active writers
    # writers = {}
    writers_variables = {
        'archive_output': 'archive.html',
    }

    # template_variables = {}

    # template_filters = {}

    theme_variables = {
        'disqus': 'lepture',
        'analytics': 'UA-21475122-1',

        'navigation': [
            ('Blog', '/archive/'),
            ('Life', '/life/'),
            ('Work', '/work/'),
            ('About', '/about/'),
        ],
        'elsewhere': [
            ('GitHub', 'https://github.com/lepture'),
            ('Twitter', 'https://twitter.com/lepture'),
        ],
    }


Permalink
-----------

Default permalink style is::

    {{category}}/{{filename}}.html

    # output example
    tech/intro-of-liquidluck.html

There are other permalink styles you may like:

+ ``{{filename}}.html``
+ ``{{date.year}}/{{filename}}.html``
+ ``{{date.year}}/{{date.month}}/{{filename}}.html``

You can define other keywords in your post, and take them as a part of the permalink::

    # Hello World

    - date: 2012-12-12
    - topic: life

    ----------

    content here

And then you can set your permalink as: ``{{topic}}/{{filename}}.html``.

If you don't like ``.html`` as a part of the permalink, you can set your permalink as::

    {{category}}/{{filename}}

    # or with a slash
    {{category}}/{{filename}}/

In this case, you need to make some config of your server, so that everything will be ok.
A good example of nginx conf for slash style permalink: `nginx.conf`_.

.. _`nginx.conf`: https://github.com/lepture/lepture.com/blob/master/nginx.conf

.. _multi-authors:

Multiple Authors
------------------

If your site has multiple authors, you can add them to your settings::

    author = 'lepture'
    authors = {
        'lepture': {
            'name': 'Hsiaoming Yang',
            'website': 'http://lepture.com',
            'email': 'lepture@me.com',
        },
        'kitty': {
            'name': 'Hello Kitty',
            'website': 'http://hellokitty.com',
        }
    }

And when you write a post, the default author is 'lepture', but you can change it by::

    # Hello World

    - date: 2012-12-12
    - author: kitty
    
    --------

    content here


Access the author information in template as ``{{post.author.name}}`` and
``{{post.author.website}}``.

For more information on template or theme design, head over to :ref:`theme` section.

The default theme doesn't show any information of the author, it is designed for
personal blogging.
