.. _get-started:

Get Started
============

This section assumes that you already have Felix Felicis (liquidluck) installed.
If you do not, header over to the :ref:`installation` section.


Create a website
------------------

Now, you have Felix Felicis installed. Let's create a website::

    $ cd ~
    $ mkdir website
    $ cd website
    $ liquidluck create


You will be asked some questions. If the question has a default value,
we don't change it, just hit Enter.

See what happens::

    $ ls
    content     settings.py

Create a Post
---------------

Create a post::

    $ touch content/hello-world.md

Write with you favorite editor, for example vim::

    $ vim content/hello-world.md

::

    # Hello World

    - date: 2012-12-12
    - category: life
    - tags: python, code

    ----------------

    Hello World. This is a DEMO post.


Build the website
------------------

Now that you have written a post, let's create the website::

    $ cd ~/website
    $ liquidluck build -v
    $ ls
    content     deploy      settings.py

The website is created, you can test your website::

    $ cd deploy
    $ python -m SimpleHTTPServer

Open your browser: ``http://127.0.0.1:8000``


Write more
------------

You can test more posts yourself.


.. _markup:

Markup
---------

Felix Felicis (liquidluck) supports markup of Markdown and reStructuredText.
It is suggested that you write in Markdown, it's easier.

There are three parts in each post:

+ title -- ``Hello World`` in the example
+ meta -- ``date``, ``category``, ``tags`` in the example
+ content -- everything below the first ``-------``

Metadata that Felix Felicis supports natively:

+ date
+ public  -- default is ``true``, if set to ``false``, this post won't be included in archive
+ tags -- tags are seprated by comma
+ category
+ summary
+ author  -- see :ref:`multi-authors` for detail
+ template  -- see :ref:`template` for detail

which means you can access them in template with a shortcut, for example: ``{{post.tags}}``.


Post, Page and File
----------------------

Page is the post without date.
