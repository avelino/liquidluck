.. _configuration:


Configuration
==============

Felix Felicis configuration file supports **YAML**, **Python** and **JSON**
formats. You can create the config file with::

    $ liquidluck init


Overview
----------

The default **Python** format config file:

.. literalinclude:: ../liquidluck/tools/_settings.py


Permalink
-----------

Default permalink style is::

    {{date.year}}/{{filename}}.html

    # output example
    tech/intro-of-liquidluck.html

There are other permalink styles you may like:

+ ``{{filename}}.html``
+ ``{{folder}}/{{filename}}.html``
+ ``{{category}}/{{filename}}.html``
+ ``{{date.year}}/{{filename}}.html``
+ ``{{date.year}}/{{date.month}}/{{filename}}.html``

You can define other keywords in your post, and take them as a part of the permalink::

    # Hello World

    - date: 2012-12-12
    - topic: life

    ----------

    content here

And then you can set your permalink as: ``{{topic}}/{{filename}}.html``. Learn
more about :ref:`meta`.

If you don't like ``.html`` as a part of the permalink, you can set your permalink as::

    {{category}}/{{filename}}

    # or with a slash
    {{category}}/{{filename}}/

    # slash without server helper
    {{category}}/{{filename}}/index.html

In this case, you need to make some config of your server, so that everything will be ok.
A good example of nginx conf for slash style permalink: `nginx.conf`_.

Issues about permalink:

- https://github.com/lepture/liquidluck/issues/21

.. _`nginx.conf`: https://github.com/lepture/lepture.com/blob/master/nginx.conf

.. _multi-authors:


Multiple Authors
------------------

If your site has multiple authors, you can add them to your settings::

    author = {
        'default': 'lepture',

        'vars': {
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


Readers
-------

There are two readers in Felix Felicis, one is Markdown, and the other is reStructuredText.


Customize Reader
````````````````

Issues that contain information on readers:

- https://github.com/lepture/liquidluck/issues/26


Reader Variables
````````````````

Issues that contain information on readers variables:

- https://github.com/lepture/liquidluck/issues/25


Writers
-------

There are many writers in Felix Felicis, and you can add more. If you want to add your
own writer to Felix Felics, head over to :ref:`development`.


Writers Variables
`````````````````

Every writer can define its own variable, for example the archive write, if you set::

    writer = {
        'vars': {
            'archive_output': 'archive.html',
        }
    }

The archive page will be write to **archive.html** instead of **index.html**.

Available writers variables (but you won't need to change them):

- post_template (post.html)
- page_template (page.html)
- archive_template (archive.html)
- **archive_output** (index.html)
- archive_feed_template (feed.xml)
- year_template (archive.html)
- tag_template (archive.html)
- category_template (archive.html)
- category_feed_template (feed.xml)


Useful Issues
---------------

- https://github.com/lepture/liquidluck/issues/25
- https://github.com/lepture/liquidluck/issues/26
- https://github.com/lepture/liquidluck/issues/30
- https://github.com/lepture/liquidluck/issues/32
- https://github.com/lepture/liquidluck/issues/34
