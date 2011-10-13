
import os
from math import log

from liquidluck.writers import Writer, ArchiveMixin, FeedMixin, PagerMixin
from liquidluck.utils import Temp
from liquidluck.utils import merge
from liquidluck import logger

class StaticWriter(Writer):
    def _static_url(self, name):
        f = os.path.join(self.staticdir, name)
        url = self.config.get('static_prefix', '/_static')
        stat = int(os.stat(f).st_mtime)
        return os.path.join(url, name) + '?t=' + str(stat)

    def register(self):
        self.register_context('static_url', self._static_url)

    def run(self):
        for source in self.walk(self.staticdir):
            path = source.replace(self.projectdir,'').lstrip('/')
            dest = os.path.join(self.deploydir, path)
            self.copy_to(source, dest)

class PostWriter(Writer):
    def _content_url(self, a, *args):
        path = os.path.join(str(a), *args)
        if not path.startswith('http://'):
            path = '/{0}'.format(path.lstrip('/'))
        return path

    def register(self):
        self.register_context('content_url', self._content_url)

    def _calc_rel_posts(self):
        public_posts = []
        secret_posts = []
        for post in self.total_files[0]:
            if post.get('public', 'true') != 'false':
                public_posts.append(post)
            else:
                secret_posts.append(post)
        public_posts = self.sort_posts(public_posts)
        i = 0
        count = len(public_posts)
        for post in public_posts:
            if i > 0:
                public_posts[i].prev = public_posts[i-1]
            if i + 1 < count:
                public_posts[i].next = public_posts[i+1]
            i += 1
        posts = public_posts
        posts.extend(secret_posts)
        return posts


    def _write_post(self, post):
        _tpl = post.get('template', 'post.html')
        dest = os.path.join(self.deploydir, post.destination)
        if os.path.exists(dest) and post.mtime < os.stat(dest).st_mtime:
            logger.info('Ignore ' + dest)
            return
        self.write({'post':post}, _tpl, post.destination)

    def run(self):
        for post in self._calc_rel_posts():
            self._write_post(post)

class FileWriter(Writer):
    def run(self):
        for source in self.total_files[1]:
            path = source.replace(self.postdir,'').lstrip('/')
            dest = os.path.join(self.deploydir, path)
            self.copy_to(source, dest)

class IndexWriter(Writer, ArchiveMixin, PagerMixin, FeedMixin):
    def run(self):
        posts = self.sort_posts(self.calc_archive_posts())
        self.register_context('title', 'Archive')
        self.register_context('folder', '')
        dest = self.config.get('index', 'index.html')
        self.write_pager(posts, dest)
        self.write_feed(posts, dest='feed.xml')

class YearWriter(Writer, ArchiveMixin, PagerMixin, FeedMixin):
    def calc_year_posts(self):
        for post in self.calc_archive_posts():
            yield post.date.year, post

    def run(self):
        for year, posts in merge(self.calc_year_posts()).iteritems():
            posts = self.sort_posts(posts)
            year = str(year)
            self.register_context('title', year)
            dest = os.path.join(year, 'index.html')
            self.write_pager(posts, dest)

class TagWriter(Writer, ArchiveMixin, PagerMixin):
    def calc_tag_posts(self):
        for post in self.calc_archive_posts():
            tags = post.get('tags')
            for tag in tags:
                yield tag, post

    def write_tagcloud(self, tagcloud):
        dest = 'tag/index.html'
        tags = []
        for k, v in tagcloud.iteritems():
            tag = Temp()
            tag.name = k
            tag.count = len(v)
            tag.size = 100 + log(tag.count or 1)*20
            tags.append(tag)
        _tpl = self.config.get('tagcloud_template', 'tagcloud.html')
        return self.write({'tags':tags}, _tpl, dest)

    def run(self):
        tagcloud = merge(self.calc_tag_posts())
        self.write_tagcloud(tagcloud)
        for tag, posts in tagcloud.iteritems():
            posts = self.sort_posts(posts)
            self.register_context('title', tag)

            dest = os.path.join('tag', tag + '.html')
            self.write_pager(posts, dest)

class FolderWriter(Writer, ArchiveMixin, PagerMixin, FeedMixin):
    def calc_folder_posts(self):
        for post in self.calc_archive_posts():
            folder = post.get('folder', None)
            if folder:
                yield folder, post

    def run(self):
        for folder, posts in merge(self.calc_folder_posts()).iteritems():
            posts = self.sort_posts(posts)
            self.register_context('title', folder)
            self.register_context('folder', folder)

            dest = os.path.join(folder, 'index.html')
            self.write_pager(posts, dest)
            dest = os.path.join(folder, 'feed.xml')
            self.write_feed(posts, dest)
