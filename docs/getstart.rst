.. _getstart:

Get Start
==========

This section assumes you already have Felix Felicis (liquidlukc) installed.
If you do not, header over to the :ref:`installation` section.


Create a website
------------------

Now, you have Felix Felicis installed. Let's create a website::

    $ cd ~
    $ mkdir website
    $ cd website
    $ liquidluck create


You will be asked some questions, if the question has a default value,
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

You have written a post, let's create the website::

    $ cd ~/website
    $ liquidluck build -v
    $ ls
    content     deploy      settings.py

The website is created, test your website::

    $ cd deploy
    $ python -m SimpleHTTPServer

Open your browser: ``http://127.0.0.1:8000``


Write more
------------

Write more posts to test for yourself.


Markup
---------

Felix Felicis (liquidluck) supports markup of Markdown and reStructuredText.
It is suggested that you write in Markdown, it's easier.
