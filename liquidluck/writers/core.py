#!/usr/bin/env python

import os
from liquidluck.options import g, settings
from liquidluck.utils import UnicodeDict, walk_dir, copy_to
from liquidluck.writers.base import BaseWriter, Pagination
from liquidluck.writers.base import get_post_slug, slug_to_destination


class PostWriter(BaseWriter):
    def __init__(self):
        self._template = self.get('post_template', 'post.html')

    def start(self):
        for post in g.public_posts:
            template = post.template or self._template
            self.render({'post': post}, template, self._dest_of(post))

        for post in g.secure_posts:
            self.render({'post': post}, template, self._dest_of(post))

    def _dest_of(self, post):
        slug = get_post_slug(post, settings.permalink)
        return os.path.join(g.output_directory, slug_to_destination(slug))


class PageWriter(BaseWriter):
    def __init__(self):
        self._template = self.get('page_template', 'page.html')

    def start(self):
        l = len(g.source_directory) + 1
        for post in g.pure_pages:
            template = post.template or self._template
            filename = os.path.splitext(post.filepath[l:])[0] + '.html'
            dest = os.path.join(g.output_directory, filename)
            self.render({'post': post}, template, dest)


class ArchiveWriter(BaseWriter):
    def __init__(self):
        self._template = self.get('archive_template', 'archive.html')
        self._output = self.get(
            'archive_output', self.prefix_dest('index.html'))
        self._title = self.get('archive_title', 'Archive')

    def start(self):
        pagination = Pagination(g.public_posts, 1, self.perpage)
        pagination.title = self._title
        pagination.root = self.prefix_dest('')

        dest = os.path.join(g.output_directory, self._output)
        self.render({'pagination': pagination}, self._template, dest)

        if pagination.pages < 2:
            return

        for page in range(1, pagination.pages + 1):
            pagination = Pagination(g.public_posts, page, self.perpage)
            pagination.title = self._title
            pagination.root = self.prefix_dest('')
            dest = os.path.join(g.output_directory, 'page/%s.html' % page)
            if pagination.root:
                dest = os.path.join(
                    g.output_directory,
                    pagination.root,
                    'page/%s.html' % page
                )
            self.render({'pagination': pagination}, self._template, dest)

    def prefix_dest(self, dest):
        prefix = settings.site.get('prefix').rstrip('/')
        if not dest:
            return prefix
        if prefix:
            return '%s/%s' % (prefix, dest)
        if isinstance(dest, int):
            dest = str(dest)
        return dest


class ArchiveFeedWriter(ArchiveWriter):
    def __init__(self):
        self._template = self.get('archive_feed_template', 'feed.xml')
        self._output = self.get(
            'archive_feed_output', self.prefix_dest('feed.xml')
        )

    def start(self):
        feed = UnicodeDict()
        feed.url = self.prefix_dest('index.html')
        feed.feedurl = self._output
        feed.posts = g.public_posts[:settings.feedcount]

        dest = os.path.join(g.output_directory, self._output)
        self.render({'feed': feed}, self._template, dest)


class FileWriter(BaseWriter):
    def start(self):
        l = len(g.source_directory) + 1
        for f in g.pure_files:
            path = f[l:]
            dest = os.path.join(g.output_directory, path)
            copy_to(f, dest)


class StaticWriter(BaseWriter):
    def start(self):
        static_path = os.path.join(g.theme_directory, 'static')
        l = len(static_path) + 1
        for f in walk_dir(static_path):
            path = f[l:]
            dest = os.path.join(g.static_directory, path)
            copy_to(f, dest)


class YearWriter(ArchiveWriter):
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
        pagination.root = self.prefix_dest(year)

        dest = os.path.join(g.output_directory, pagination.root, 'index.html')
        self.render({'pagination': pagination}, self._template, dest)

        if pagination.pages < 2:
            return

        for page in range(1, pagination.pages + 1):
            pagination = Pagination(posts, page, self.perpage)
            pagination.title = year
            pagination.root = self.prefix_dest(year)

            dest = os.path.join(
                g.output_directory,
                pagination.root,
                'page/%s.html' % page
            )
            self.render({'pagination': pagination}, self._template, dest)


class TagWriter(ArchiveWriter):
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
        pagination.root = self.prefix_dest('tag/%s' % tag)

        dest = os.path.join(g.output_directory, pagination.root, 'index.html')
        self.render({'pagination': pagination}, self._template, dest)

        if pagination.pages < 2:
            return

        for page in range(1, pagination.pages + 1):
            pagination = Pagination(posts, page, self.perpage)
            pagination.title = tag
            pagination.root = self.prefix_dest('tag/%s' % tag)

            dest = os.path.join(
                g.output_directory, pagination.root, 'page/%s.html' % page
            )
            self.render({'pagination': pagination}, self._template, dest)


class TagCloudWriter(ArchiveWriter):
    _posts = {}

    def __init__(self):
        self._template = self.get('tagcloud_template', 'tagcloud.html')
        if 'tag' in g.resource:
            self._posts = g.resource['tag']
            return

        for post in g.public_posts:
            for tag in post.tags:
                if tag not in self._posts:
                    self._posts[tag] = [post]
                else:
                    self._posts[tag].append(post)

        g.resource['tag'] = self._posts

    def start(self):
        dest = os.path.join(
            g.output_directory, self.prefix_dest('tag/index.html')
        )
        self.render({'tags': self._posts}, self._template, dest)


class CategoryWriter(ArchiveWriter):
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
        pagination.root = self.prefix_dest(category)

        dest = os.path.join(g.output_directory, pagination.root, 'index.html')
        self.render({'pagination': pagination}, self._template, dest)

        if pagination.pages < 2:
            return

        for page in range(1, pagination.pages + 1):
            pagination = Pagination(posts, page, self.perpage)
            pagination.title = self._title.get(category, category)
            pagination.root = self.prefix_dest(category)

            dest = os.path.join(
                g.output_directory, pagination.root, 'page/%s.html' % page
            )
            self.render({'pagination': pagination}, self._template, dest)


class CategoryFeedWriter(ArchiveWriter):
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
            feed.url = self.prefix_dest('%s/index.html' % category)
            feed.feedurl = self.prefix_dest('%s/%s' % (category, self._output))
            feed.posts = self._posts[category][:settings.feedcount]
            dest = os.path.join(g.output_directory, feed.feedurl)
            self.render({'feed': feed}, self._template, dest)
