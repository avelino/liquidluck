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
from liquidluck.namespace import ns


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

    def _get_related_posts_by_tags(self, post):
        if not post.public:
            return
        if not hasattr(post, 'tags'):
            return
        tags = set(post.tags)
        base = len(post.tags)
        for p in ns.storage.posts:
            prior = len(tags - set(p.get('tags', [])))
            if prior < base and p.slug != post.slug and p.public:
                p.related_priority = base - prior
                yield p

    def run(self):
        for post in ns.storage.posts:
            post = self._get_rel_posts(post)
            post.related_posts = self._get_related_posts_by_tags(post)
            self._write_post(post)
