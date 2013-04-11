.. _get-started:

Get Started
============

This section assumes that you already have Felix Felicis (liquidluck) installed.
If you do not, header over to the :ref:`installation` section.


Create a website
------------------

Now that you have Felix Felicis installed, let's create a website::

    $ cd ~
    $ mkdir website
    $ cd website
    $ liquidluck init


You will be asked some questions. If the question has a default value,
we don't change it, just hit Enter.

See what happens::

    $ ls
    content     settings.yml

Create a Post
---------------

Create a post with your favorite editor, for example::

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

That means the website is created, so you can test it now::

    $ liquidluck server

Open your browser: http://127.0.0.1:8000.

For more on the Felix Felicis server, see :ref:`preview-server`.


Write more
------------

You can test more posts yourself.


Learn Commands
----------------

Get all commands::

    $ liquidluck -h


List all themes::

    $ liquidluck search

Install a theme::

    $ liquidlcuk install {{name}}
