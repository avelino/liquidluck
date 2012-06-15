# Felix Felicis

Felix Felicis is a magical potion, also known as liquidluck.
It was first introduced in Harry Porter, and this is where the name comes.


Felix Felicis (aka liquidluck) is a simple lightweight static blog
generator written in Python.

- [Documentation](http://liquidluck.readthedocs.org)


**There are so many static blog generators, why create a new one?**

The main design pattern of Felix Felicis:

1. We don't create any syntax that is only available in Felix Felicis
2. Document should always be valid, it will be pretty even without Felix Felicis


## Post Style Overview

**A post in Markdown**

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

**A post in reStructuredText**

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


Both of these two posts are valid in their markup language, even without Felix Felicis they should be displayed well.

And in this case, your documents will always be yours, not tied to Felix Felicis.


## Compatibility

- Markup:

    - reStructuredText
    - markdown

- Python:

    - 2.6
    - 2.7
    - 3.2
