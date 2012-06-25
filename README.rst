Felix Felicis
==============

.. image:: https://secure.travis-ci.org/lepture/liquidluck.png
    :target: https://secure.travis-ci.org/lepture/liquidluck


Felix Felicis (aka ``liquidluck``) is a simple lightweight static blog generator
written in Python.

**There are so many static blog generators, why create a new one?**

The main design pattern of Felix Felicis:

1. Beautiful is better than ugly.
2. Nothing is better than everything.


`Documentation <http://liquidluck.readthedocs.org>`_ is available on RTD.

Overview
---------

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


Compatibility
--------------

+ Markup:

  - restructedText_
  - markdown_

+ Python:

  - 2.6
  - 2.7
  - 3.1
  - 3.2


.. _restructedText: http://docutils.sourceforge.net/rst.html
.. _markdown: http://daringfireball.net/projects/markdown/
