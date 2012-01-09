#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is an example writer, which explains to you how to contribute to this
project. You can not rewrite the default.py file, instead, you can write
another writer to disable it.

You can add your author information like I did below.
"""

__author__ = 'lepture <lepture@me.com>'

from liquidluck.writers.default import PostWriter
from liquidluck.writers import sort_posts
from liquidluck.namespace import ns
from liquidluck import logger

class TagRelatedPostWriter(PostWriter):
    """
    How to use this:

        [writers]
        post = liquidluck.writers.related_writer.TagRelatedPostWriter

    This will disable the default post writer and active this writer.

    Edit your post template, get related posts with:

        {% for related in post.related_posts %}
            <h4>{{related.title}}</h4>
        {% endfor %}

    Attension: there is one more parameter in ``related``, which is
    ``related.related_priority``. You may only want to show related
    posts which has a higher priority.

        {% for related in post.related_posts %}
            {% if related.related_priority > 1 %}
            <h4>{{related.title}}</h4>
            {% endif %}
        {% endfor %}
    """
    writer_type = 'Tag Related Post Writer'

    def _calc_rel_posts(self):
        public_posts = []
        secret_posts = []
        for post in ns.storage.posts:
            if post.public:
                public_posts.append(post)
            else:
                logger.warn('Non-indexed Post: %s' % post.filepath)
                secret_posts.append(post)
        public_posts = sort_posts(public_posts)
        i = 0
        count = len(public_posts)
        for post in public_posts:
            if i > 0:
                public_posts[i].prev = public_posts[i - 1]
            if i + 1 < count:
                public_posts[i].next = public_posts[i + 1]
            i += 1
        posts = public_posts
        posts.extend(secret_posts)
        self.public_posts = public_posts
        return posts

    def _get_related_posts_by_tags(self, post):
        if not hasattr(self, 'public_posts'):
            return
        if not hasattr(post, 'tags'):
            return
        tags = set(post.tags)
        base = len(post.tags)
        for p in self.public_posts:
            prior = len(tags - set(p.get('tags',[])))
            if prior < base and p.slug != post.slug:
                p.related_priority = base - prior
                yield p

    def run(self):
        for post in self._calc_rel_posts():
            post.related_posts = self._get_related_posts_by_tags(post)
            self._write_post(post)
