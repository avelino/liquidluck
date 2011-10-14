
import os
from math import log

from liquidluck.writers import Writer, ArchiveMixin, FeedMixin, PagerMixin
from liquidluck.writers import sort_posts, make_folder, copy_to, _walk
from liquidluck.utils import merge
from liquidluck.ns import namespace, NameSpace
from liquidluck import logger

def static_url(name):
    f = os.path.join(namespace.projectdir, namespace.site.get('staticdir','_static'), name)
    stat = int(os.stat(f).st_mtime)
    url = namespace.site.get('static_prefix', '/_static')
    return os.path.join(url, name) + '?t=' + str(stat)

class StaticWriter(Writer):
    @classmethod
    def get_context(self):
        return {'static_url': static_url}

    def run(self):
        for source in _walk(self.staticdir):
            path = source.replace(namespace.projectdir,'').lstrip('/')
            dest = os.path.join(self.deploydir, path)
            copy_to(source, dest)

def content_url(a, *args):
    path = os.path.join(str(a), *args)
    if not path.startswith('http://'):
        path = '/{0}'.format(path.lstrip('/'))
    return path

class PostWriter(Writer):
    @classmethod
    def get_context(self):
        return {'content_url': content_url}

    def _calc_rel_posts(self):
        public_posts = []
        secret_posts = []
        for post in namespace.allposts:
            if post.public:
                public_posts.append(post)
            else:
                secret_posts.append(post)
        public_posts = sort_posts(public_posts)
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
        for source in namespace.allfiles:
            path = source.replace(self.postdir,'').lstrip('/')
            dest = os.path.join(self.deploydir, path)
            copy_to(source, dest)

class IndexWriter(Writer, ArchiveMixin, PagerMixin, FeedMixin):
    def run(self):
        posts = sort_posts(self.calc_archive_posts())
        dest = namespace.site.get('index', 'index.html')
        self.write_pager(posts, dest, title='Archive')
        self.write_feed(posts, dest='feed.xml', folder='')

class YearWriter(Writer, ArchiveMixin, PagerMixin, FeedMixin):
    def calc_year_posts(self):
        for post in self.calc_archive_posts():
            yield post.date.year, post

    def run(self):
        for year, posts in merge(self.calc_year_posts()).iteritems():
            posts = sort_posts(posts)
            year = str(year)
            dest = os.path.join(year, 'index.html')
            self.write_pager(posts, dest, title=year)

class TagWriter(Writer, ArchiveMixin, PagerMixin):
    def calc_tag_posts(self):
        for post in self.calc_archive_posts():
            tags = post.get('tags', [])
            for tag in tags:
                yield tag, post

    def write_tagcloud(self, tagcloud):
        dest = 'tag/index.html'
        tags = []
        for k, v in tagcloud.iteritems():
            tag = NameSpace(
                name = k,
                count = len(v),
                size = 100 + log(len(v) or 1)*20,
            )
            tags.append(tag)
        _tpl = namespace.site.get('tagcloud_template', 'tagcloud.html')
        return self.write({'tags':tags}, _tpl, dest)

    def run(self):
        tagcloud = merge(self.calc_tag_posts())
        self.write_tagcloud(tagcloud)
        for tag, posts in tagcloud.iteritems():
            posts = sort_posts(posts)
            dest = os.path.join('tag', tag + '.html')
            self.write_pager(posts, dest, title=tag)

class FolderWriter(Writer, ArchiveMixin, PagerMixin, FeedMixin):
    def calc_folder_posts(self):
        for post in self.calc_archive_posts():
            folder = post.get('folder', None)
            if folder:
                yield folder, post

    def run(self):
        for folder, posts in merge(self.calc_folder_posts()).iteritems():
            posts = sort_posts(posts)
            dest = os.path.join(folder, 'index.html')
            self.write_pager(posts, dest, title=folder, folder=folder)
            dest = os.path.join(folder, 'feed.xml')
            self.write_feed(posts, dest, title=folder, folder=folder)
