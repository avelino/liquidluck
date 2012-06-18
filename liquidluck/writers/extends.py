#!/usr/bin/env python

import os
from liquidluck.utils import UnicodeDict
from liquidluck.options import g, settings
from liquidluck.writers.base import BaseWriter, Pagination
from liquidluck.writers.base import get_post_slug, slug_to_destination


class YearWriter(BaseWriter):
    _posts = {}

    def __init__(self):
        self._template = self.get('year_template', 'archive.html')

        for post in g.public_posts:
            if post.date.year not in self._posts:
                self._posts[post.date.year] = [post]
            else:
                self._posts[post.date.year].append(post)

        g.resource['year'] = self._posts

    def start(self):
        for year in self._posts:
            self._write_posts(year)

    def _write_posts(self, year):
        posts = self._posts[year]
        pagination = Pagination(posts, 1, self.perpage)
        pagination.title = year
        pagination.root = str(year)

        dest = os.path.join(g.output_directory, str(year), 'index.html')
        self.render({'pagination': pagination}, self._template, dest)

        if pagination.pages < 2:
            return

        for page in range(1, pagination.pages + 1):
            dest = os.path.join(
                g.output_directory, str(year), 'page/%s.html' % page
            )
            pagination = Pagination(posts, page, self.perpage)
            pagination.title = year
            pagination.root = str(year)
            self.render({'pagination': pagination}, self._template, dest)


class TagWriter(BaseWriter):
    _posts = {}

    def __init__(self):
        self._template = self.get('tag_template', 'archive.html')

        for post in g.public_posts:
            for tag in post.tags:
                if tag not in self._posts:
                    self._posts[tag] = [post]
                else:
                    self._posts[tag].append(post)

        g.resource['tag'] = self._posts

    def start(self):
        for tag in self._posts:
            self._write_posts(tag)

    def _write_posts(self, tag):
        posts = self._posts[tag]
        pagination = Pagination(posts, 1, self.perpage)
        pagination.title = tag
        pagination.root = 'tag/%s' % tag

        dest = os.path.join(g.output_directory, 'tag', tag, 'index.html')
        self.render({'pagination': pagination}, self._template, dest)

        if pagination.pages < 2:
            return

        for page in range(1, pagination.pages + 1):
            dest = os.path.join(
                g.output_directory, 'tag', tag, 'page/%s.html' % page)
            pagination = Pagination(posts, page, self.perpage)
            pagination.title = tag
            pagination.root = 'tag/%s' % tag
            self.render({'pagination': pagination}, self._template, dest)


class CategoryWriter(BaseWriter):
    _posts = {}

    def __init__(self):
        self._template = self.get('category_template', 'archive.html')
        self._title = self.get('category_title', {})

        for post in g.public_posts:
            if post.category:
                if post.category not in self._posts:
                    self._posts[post.category] = [post]
                else:
                    self._posts[post.category].append(post)

        g.resource['category'] = self._posts

    def start(self):
        for category in self._posts:
            self._write_posts(category)

    def _write_posts(self, category):
        posts = self._posts[category]
        pagination = Pagination(posts, 1, self.perpage)
        pagination.title = self._title.get(category, category)
        pagination.root = category

        dest = os.path.join(g.output_directory, category, 'index.html')
        self.render({'pagination': pagination}, self._template, dest)

        if pagination.pages < 2:
            return

        for page in range(1, pagination.pages + 1):
            dest = os.path.join(
                g.output_directory, category, 'page/%s.html' % page)
            pagination = Pagination(posts, page, self.perpage)
            pagination.title = self._title.get(category, category)
            pagination.root = category
            self.render({'pagination': pagination}, self._template, dest)


class CategoryFeedWriter(BaseWriter):
    _posts = {}

    def __init__(self):
        self._template = self.get('category_feed_template', 'feed.xml')
        self._output = self.get('category_feed_output', 'feed.xml')

        if 'category' in g.resource:
            self._posts = g.resource['category']
            return

        for post in g.public_posts:
            if post.category:
                if post.category not in self._posts:
                    self._posts[post.category] = [post]
                else:
                    self._posts[post.category].append(post)

    def start(self):
        for category in self._posts:
            feed = UnicodeDict()
            feed.url = '%s/index.html' % category
            feed.feedurl = '%s/%s' % (category, self._output)
            feed.posts = self._posts[category][:settings.feedcount]
            dest = os.path.join(g.output_directory, category, self._output)
            self.render({'feed': feed}, self._template, dest)


class RelationalPostWriter(BaseWriter):
    def __init__(self):
        self._template = self.get('relational_post_template', 'post.html')

    def start(self):
        for index, post in enumerate(g.public_posts):
            template = post.template or self._template

            relation = self._get_relations(post, index)
            params = {'post': post, 'relation': relation}
            self.render(params, template, self._dest_of(post))

        for post in g.secure_posts:
            self.render({'post': post}, template, self._dest_of(post))

    def _dest_of(self, post):
        slug = get_post_slug(post, settings.permalink)
        return os.path.join(g.output_directory, slug_to_destination(slug))

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
