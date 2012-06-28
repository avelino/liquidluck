# Moment Theme for Felix Felicis

This is the latest version of the default theme for Felix Felicis.


## Installation

### Install with liquidluck

```
$ liquidluck install -t moment
```

### Install by yourself

Git clone this repo, and place it in your blog:

```
your_blog/
    settings.py
    content/
    _themes/
        moment/
```

### Install with git submodule

You can use git submodule for convience:

```
$ git submodule add git://github.com/lepture/liquidluck-theme-moment.git _themes/moment
```

## Configuration

Edit your settings.py, change your theme to:

```python
theme = 'moment'
```


## Customize

You can customize your theme with ``theme_variables``.

+ Change Navigation (example)

```python
theme_variables = {
    'navigation': [
        ('Home', '/'),
        ('Life', '/life/'),
        ('Work', '/work/'),
    ],
}
```

+ Google Analytics

```python
theme_variables = {
    'analytics': 'UA-xxxx',
}
```

+ Disqus Comment Support

```python
theme_variables = {
    'disqus': 'your-disqus-shortname',
}
```

+ Show author information, default is False

```python
theme_variables = {
    'show_author': True,
}
```

+ Tagcloud support, active tagcloud:

```python
writers = {
    'tagcloud': 'liquidluck.writers.core.TagCloudWriter',
    # disable tag writer
    # 'tag': None,
}

# change post tags link to tagcloud
theme_variables = {
    'tagcloud': True,  # default is False
}
```

## 404

You can create a file in your source directory (``content``) named ``404.md``.

```
# 404

- template: 404.html

----------------

You content here.
```

Configure your nginx, add:

```
error_page 404 /404.html;
```

You can google for more information.
