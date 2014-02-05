.. _theme:

Theme
========

The template engine of Felix Felicis (liquidluck) is Jinja_.
The basic syntax is simple; I encourage you to learn it.



You can learn how to design your own theme by demo:

- https://github.com/lepture/liquidluck-theme-moment
- https://github.com/lepture/liquidluck-theme-octopress

Please create your repo at github with ``liquidluck-theme-`` prefix.
Remember to submit your theme at `Theme Gallery`_.

Get all themes::

    $ liquidluck search

Install a theme::

    $ liquidluck install moment

Install a theme to the global theme gallery::

    $ liquidluck install moment -g


Structure
----------

A glance of a theme::

    your_theme/
        theme.py                <---- theme variables
        filters.py                 <---- filters defined by theme
        static/                    <---- static files
            style.css
            ...
        templates/                 <---- template files
            archive.html
            post.html
            page.html


You don't need to copy a ``feed.xml`` file. Only ``archive.html``, ``post.html``
and ``page.html`` are required, but you can add more.

.. _template:

Template
----------

Sometimes, you don't need to create a total new theme, you just want to make
some changes.

For example, you are using the default theme, which means in your settings::

    theme = {
        'name': 'default'
    }


If you want to make some changes on the post page (like adding Readability),
in your blog directory, create a post.html template::

    your_blog/
        settings.py
        content/
        _templates/
            post.html

And edit this post.html:

.. sourcecode:: html+jinja

    {% extends "layout.html" %}

    {% block title %}{{post.title}} - {{site.name}}{% endblock %}

    {% block main %}
    <div class="hentry">
        <h1 class="entry-title">{{post.title}}</h1>
        <time class="updated" datetime="{{post.date|xmldatetime}}">{{post.date.strftime('%Y-%m-%d')}}</time>
        {% if template.readability %}
        <div class="rdbWrapper" data-show-read="1" data-show-send-to-kindle="1"></div>
        <script type="text/javascript" src="http://www.readability.com/embed.js" async></script>
        {% endif %}

        <div class="entry-content">
            {{post.content}}
        </div>
        <div class="entry-tags">
            {% for tag in post.tags %}
            <a href="{{ content_url(site.prefix, 'tag', tag, 'index.html') }}">{{tag}}</a>
            {% endfor %}
        </div>

        {% if theme.disqus %}
        <div id="disqus_thread"></div>
        <script type="text/javascript">
            var disqus_shortname = '{{theme.disqus}}';
            var disqus_title = '{{post.title}}';
            (function() {
                var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
                dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
                (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
            })();
        </script>
        {% endif %}
    </div>
    {% endblock %}


And edit your settings to enable Readability::

    template = {
        'vars': {
            'readability': True,
        }
    }


Variables
----------

There are two levels of variables, global and templatable. Global means that a
variable can be accessed in every template, and templatable means that a variable
can be accessed in specific template.


Global Variables
~~~~~~~~~~~~~~~~~~

- system, this is all about Felix Felicis::

    {
        'name': 'Felix Felicis',
        'version': '....',
        'homepage': '....',
        'time': '....',
    }

  When you create your own theme, you should add copyright of Felix Felicis by::

    Powered by <a href="{{system.homepage}}">{{system.name}}</a> {{system.version}}

  ``{{system.time}}`` means current utc time.

- site, you defined in your settings file::

    site = {
        'name': "Kitty's BLog",
        'url': 'http://www.example.com',
    }

- theme, theme variable is defined by theme creator in the theme settings, and
  users can overwrite theme in blog settings ``theme_variables``.

  For example, in the default theme's settings, we have::

    navigation = [
        {'title': 'Home', 'link': '/'},
        {'title': 'About', 'link': '/about.html'},
    ]

  Users can rewrite it in blog settings::

    theme = {
        'vars': {
            'navigation': [
                {'title': 'Home', 'link': '/'},
                {'title': 'Life', 'link': '/life/'},
                {'title': 'Work', 'link': '/work/'},
            ]
        }
    }

- template, template variable is defined by users in settings with::

    template = {
        'vars': {
            'readability': True,
        }
    }

  And it can be accessed in template by ``{{template.readability}}``.

- writer, this variable tells you which writer is rendering this page now::

    {
        'class': 'ArchiveWriter',
        'name': 'archive',
        'filepath': 'path/to/file.html',
    }


Templatable Variables
~~~~~~~~~~~~~~~~~~~~~~~

Templatable variables are only accessed in specific templates.

- pagination, available in ``archive.html``
- post, available in ``post.html`` and ``page.html``


Resource Variables
-----------------------

This variable is powerful, for example, ``{{resource.posts}}`` contains all
your public posts. It is related to a writer.

- {{resource.posts}}
- {{resource.pages}}
- {{resource.year}}: if you enabled YearWriter
- {{resource.category}}: if you enabled CategoryWriter
- {{resource.tag}}: if you enabled TagWriter


Functions
~~~~~~~~~

- content_url
- static_url


Filters
---------

Filter is an important concept in Jinja_.

Default Filters
~~~~~~~~~~~~~~~~

- xmldatetime
- permalink, ``{{post|permalink}}`` to create the permalink of a post
- tag_url
- year_url
- feed_updated


Theme Filters
~~~~~~~~~~~~~~~


Contributors
-------------

If you have designed a theme, you can submit it to the `Theme Gallery`_


.. _`Theme Gallery`: https://github.com/lepture/liquidluck/wiki/Themes
.. _Jinja: http://jinja.pocoo.org
