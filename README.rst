Felix Felicis
==============

.. image:: https://secure.travis-ci.org/lepture/liquidluck.png?branch=develop
    :target: https://secure.travis-ci.org/lepture/liquidluck


Felix Felicis (aka ``liquidluck``) is a simple lightweight static blog generator
written in Python.

**There are so many static blog generators, why create a new one?**

The main design pattern of Felix Felicis:

1. Beautiful is better than ugly.
2. Nothing is better than everything.


`Documentation <http://liquidluck.readthedocs.org>`_ is available on RTD.

Commands
------------

1. Create a site::

   liquidluck init

2. Search for a theme::

   liquidluck search

3. Install a theme::

   liquidluck install moment

4. Build articles::

   liquidluck build

5. Preview server::

   liquidluck server

More information with ``liquidluck help``.


Write a post
----------------------

A post in markdown::

    # Hello World

    - date: 2012-06-11
    - tags: python, javascript

    -------

    Hello World in Python

    ```python
    def hello(name="World"):
        print "Hello %s" % name
    ```

    Hello World in JavaScript

    ```javascript
    function hello(name) {
        alert('Hello ' + name);
    }
    ```

A post in restructuredText::

    Hello World
    ============

    :date: 2012-06-11
    :tags: python, javascript

    Hello World in Python::

        def hello(name="World"):
            print "Hello %s" % name

    Hello World in JavaScript:

    .. sourcecode:: javascript

        function hello(name) {
            alert('Hello ' + name);
        }

Both of these two posts are valid in their markup language, even without Felix Felicis
they should be displayed well.

And in this case, your documents will always be yours, not tied to Felix Felicis.


Features
-----------

- Category, Tag, Post, Page, Feed and everything a blog should have
- Beautiful and valid syntax supports
- Full customizable theme supports
- Global theme gallery, site theme gallery, site template
- No extension system (Is this a feature? YES!)
- GitHub and BitBucket web hook service
- Live preview server


Compatibility
--------------

+ Markup:

  - restructedText_ (you need install docutils by yourself)
  - markdown_

+ Python:

  - 2.6
  - 2.7
  - 3.1
  - 3.2


.. _restructedText: http://docutils.sourceforge.net/rst.html
.. _markdown: http://daringfireball.net/projects/markdown/
