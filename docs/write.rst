Writing
===========


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

Post contains date, page doesn't. Post follows permalink, page doesn't.

A example of page in Markdown::

    # Hello Page

    - tags: page

    ----------------

    Hello Page

    ```python
    def hello():
        print("Hello Page")
    ```

It has no date.
