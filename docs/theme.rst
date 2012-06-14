.. _theme:

Theme
========

Template engine of Felix Felicis (liquidluck) is Jinja. It would be great if
you have a little knowledge on `Jinja Template`_. The basic syntax is simple,
you should know them.

.. _`Jinja Template`: http://jinja.pocoo.org/

Template
----------

Sometimes, you don't need to create a theme.


Structure
----------

::

    your_theme/
        settings.py                <---- theme variables
        static/                    <---- static files
            style.css
            ...
        templates/                 <---- template files
            archive.html
            post.html
            page.html


You don't need to copy a ``feed.xml`` file. Only ``archive.html``, ``post.html``
and ``page.html`` are required. But you can add more.


Variables
----------

If you are creating a theme, you can define some variables for your theme.


Filters
---------
