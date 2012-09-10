#!/usr/bin/env python

"""Extends of the core writers
"""

import os
from liquidluck.options import g, settings
from liquidluck.writers.base import BaseWriter
from liquidluck.writers.base import get_post_destination


class PostWriter(BaseWriter):
    """Replace the default post writer, edit settings::

        writers = {
            'post': 'liquidluck.writers.exends.PostWriter',
        }

    Get related posts in template with::

        - {{post.relation.newer}}
        - {{post.relation.older}}
        - {% for item in post.relation.related %}
    """
    writer_name = 'post'

    def __init__(self):
        self._template = self.get('post_template', 'post.html')

    def start(self):
        for index, post in enumerate(g.public_posts):
            template = post.template or self._template

            relation = self._get_relations(post, index)
            post.relation = relation
            self.render({'post': post}, template, self._dest_of(post))

        for post in g.secure_posts:
            post.relation = None
            self.render({'post': post}, template, self._dest_of(post))

    def _dest_of(self, post):
        dest = get_post_destination(post, settings.config['permalink'])
        return os.path.join(g.output_directory, dest)

    def _get_relations(self, post, index):
        total = len(g.public_posts)

        newer = None
        if index > 0:
            newer = g.public_posts[index - 1]

        older = None
        if index < total - 1:
            older = g.public_posts[index + 1]

        def get_related_by_tags():
            tags = set(post.tags)
            base = len(post.tags)

            for p in g.public_posts:
                prior = len(tags - set(p.tags))
                if prior < base and p.title != post.title:
                    p.related_priority = base - prior
                    yield p

        related = sorted(get_related_by_tags(),
                         key=lambda o: o.related_priority,
                         reverse=True)
        relation = {
            'newer': newer,
            'older': older,
            'related': related[:4],
        }
        return relation
