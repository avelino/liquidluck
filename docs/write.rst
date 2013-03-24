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


An example in markdown::

    # Felix Felicis                 <-------- this is title

    - date: 2012-12-12 12:12        <-------- this is meta
    - tags: python, blog, web

    Here is the description.

    --------------------------      <-------- this seprate meta and content

    Hello World! Welcome to the     <-------- this is content
    Felix Felicis World.

    ```                             <-------- this is normal code
    a {
        color: black;
    }
    ```

    ````css                         <-------- if code wrapped with 4 `, the code
    a {                                       will be injected to this page
        color: black;
    }
    ````


An example in reStructuredText (you need to install docutils by yourself)::

    Felix Felicis
    ================

    :date: 2012-12-12 12:12
    :tags: python, blog, web


    Hello World! Welcome to the Felix Felicis World.

    ::
    
        /* normal code */
        a {
            color: black;
        }


    .. sourcecode:: css

        /* hightlight code */

        a {
            color: black;
        }


.. _meta:

Meta
-------

Metadata that Felix Felicis supports natively:

+ date
+ public  -- default is ``true``, if set to ``false``, this post won't be included in archive
+ tags -- tags are seprated by comma
+ category
+ summary
+ folder  -- relative filepath, for example ``/home/user/blog/content/a/a.md``, folder will be ``a``
+ author  -- see :ref:`multi-authors` for detail
+ template  -- see :ref:`template` for detail

which means you can access them in template with a shortcut, for example: ``{{post.tags}}``.

Metadata that Felix Felicis created itself:

+ filepath
+ clean_filepath
+ filename
+ clean_title  -- https://github.com/lepture/liquidluck/issues/32
+ updated


Page
------

Page is the same as post, except that post contains date, page doesn't,
post follows permalink, page doesn't.

A example of page in Markdown::

    # Hello Page

    - tags: python, web         <----------- page has no date

    ----------------

    Hello Page

    ```python
    def hello():
        print("Hello Page")
    ```

Page doesn't have a ``date``, but it may contain some metadata.

Where will the page be rendered? For example, the path of the page::

    content/                 <-------- source directory
        page1.md
        a_folder/
            page2.md

and it will be rendered to::

    deploy/                  <-------- output directory
        page1.html
        a_folder/
            page2.html

It will ignore the ``site.prefix``, and therefore, if your settings::

    site = {
        'name': '...',
        ...
        'prefix': 'blog',
    }

and you want to you pages to be rendered to ``blog`` folder, you have to::

    content/
        blog/               <--------- place your pages under the prefix folder
            page1.md


File
-----

Any file without a valid markup suffix (e.g. ``.md``, ``.rst``, ``.mkd`` ...) is
a **File**. It will be copied to the same path::

    content/
        robots.txt          <--------- this is a file
        media/
            a_pic.jpg       <--------- this is a file

And the output will be::

    deploy/
        robots.txt
        media/
            a_pic.jpg

Hence, I suggest that you have a folder named ``media``, and you can leave your
picture resources there::

    ![alt](/media/a_pic.jpg "title")
