# Moment Theme for Felix Felicis

This is the latest version of the default theme for Felix Felicis.


## Installation

Requires Felix Felicis 1.10+


### Install with liquidluck

```
$ liquidluck install moment
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

+ Tagcloud support, active tagcloud:

```python
writers = {
    'tagcloud': 'liquidluck.writers.core.TagCloudWriter',
    # disable tag writer
    # 'tag': None,
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

## Allow comment

If you post is not public, this post will not be allowed to comment.
If you want to allow people to comment on your secret post, set

```python
allow_comment_on_secret_post = True
```

## Write a Review

This theme supports [review microdata](http://support.google.com/webmasters/bin/answer.py?hl=en&answer=146645#Individual_reviews).

Write your post:

```
# title

- date: 2012-12-12
- review: movie or book title
- rating: 4

------------

content
```

Rating is optional, the max rating is 5.
