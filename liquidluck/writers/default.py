
import os
import hashlib
from math import log

from liquidluck.writers import Writer, ArchiveMixin, FeedMixin, PagerMixin
from liquidluck.writers import sort_posts, make_folder, copy_to, _walk
from liquidluck.utils import merge, to_unicode
from liquidluck.ns import namespace, NameSpace
from liquidluck import logger

def static_url(name):
    f = os.path.join(namespace.projectdir, namespace.site.get('staticdir','static'), name)
    url = namespace.site.get('static_prefix', '/static')
    if not os.path.exists(f):
        logger.warn('No such static file: %s' % f)
        return os.path.join(url, name)
    f = open(f, 'rb')
    stat = hashlib.md5(f.read()).hexdigest()
    return os.path.join(url, name) + '?v=' + stat[:5]

class StaticWriter(Writer):
    writer_type = 'Static Writer'

    def start(self):
        namespace.functions.update({'static_url': static_url})
        return

    def run(self):
        for source in _walk(self.staticdir):
            path = source.replace(namespace.projectdir,'').lstrip('/')
            dest = os.path.join(self.deploydir, path)
            copy_to(source, dest)

def content_url(a, *args):
    slug = namespace.site.get('slug', 'html')
    
    args = [to_unicode(arg) for arg in args]
    path = os.path.join(to_unicode(a), *args)
    basename, ext = os.path.splitext(path)
    if not ext:
        path = basename + '/'

    if slug == 'clean':
        path = basename
    if slug == 'slash':
        path = basename + '/'

    if not path.startswith('http://'):
        path = '/%s' % path.lstrip('/')
    return path

class PostWriter(Writer):
    writer_type = 'Post Writer'

    def start(self):
        return namespace.functions.update({'content_url': content_url})

    def _calc_rel_posts(self):
        public_posts = []
        secret_posts = []
        for post in namespace.allposts:
            if post.public:
                public_posts.append(post)
            else:
                logger.info('Secrect Post: %s' % post.destination)
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
        self.write({'post':post}, _tpl, post.destination)

    def run(self):
        for post in self._calc_rel_posts():
            self._write_post(post)

class FileWriter(Writer):
    writer_type = 'File Writer'

    def run(self):
        for source in namespace.allfiles:
            path = source.replace(self.postdir,'').lstrip('/')
            dest = os.path.join(self.deploydir, path)
            copy_to(source, dest)

class IndexWriter(Writer, ArchiveMixin, PagerMixin, FeedMixin):
    writer_type = 'Index Writer'

    def start(self):
        namespace.status.posts = sort_posts(self.calc_archive_posts())
        return

    def run(self):
        posts = sort_posts(self.calc_archive_posts())
        dest = namespace.site.get('index', 'index.html')
        _archive_tpl = namespace.site.get('index_archive_template', None)
        _feed_tpl = namespace.site.get('index_feed_template', None)
        params = {'title': 'Archive'}
        if _archive_tpl: params.update({'tpl': _archive_tpl})
        self.write_pager(posts, dest, **params)
        params = {'folder':''}
        if _feed_tpl: params.update({'tpl': _feed_tpl})
        self.write_feed(posts, dest='feed.xml', **params)

class YearWriter(Writer, ArchiveMixin, PagerMixin, FeedMixin):
    writer_type = 'Year Writer'

    def calc_year_posts(self):
        for post in self.calc_archive_posts():
            yield post.date.year, post

    def start(self):
        namespace.status.years = []
        for year, posts in self.calc_year_posts():
            namespace.status.years.append(year)
        namespace.status.years = sorted(set(namespace.status.years))
        return 

    def run(self):
        _tpl = namespace.site.get('year_archive_template', None)
        for year, posts in merge(self.calc_year_posts()).iteritems():
            posts = sort_posts(posts)
            year = str(year)
            dest = os.path.join(year, 'index.html')
            params = {'title': year}
            if _tpl: params.update({'tpl': _tpl})
            self.write_pager(posts, dest, **params)

class TagWriter(Writer, ArchiveMixin, PagerMixin):
    writer_type = 'Tag Writer'

    def calc_tag_posts(self):
        for post in self.calc_archive_posts():
            tags = post.get('tags', [])
            for tag in tags:
                yield tag, post
    
    def calc_tagcloud(self):
        tagcloud = merge(self.calc_tag_posts())
        for k, v in tagcloud.iteritems():
            tag = NameSpace(
                name = k,
                count = len(v),
                size = 100 + log(len(v) or 1)*20,
            )
            yield tag

    def start(self):
        namespace.status.tags = [tag for tag in self.calc_tagcloud()]
        return 

    def write_tagcloud(self):
        dest = 'tag/index.html'
        _tpl = namespace.site.get('tagcloud_template', 'tagcloud.html')
        return self.write({'tags':namespace.status.tags}, _tpl, dest)

    def run(self):
        self.write_tagcloud()

        tagcloud = merge(self.calc_tag_posts())
        _tpl = namespace.site.get('tag_archive_template', None)
        for tag, posts in tagcloud.items():
            posts = sort_posts(posts)
            dest = os.path.join('tag', tag, 'index.html')
            params = {'title': tag}
            if _tpl: params.update({'tpl': _tpl})
            self.write_pager(posts, dest, **params)

class FolderWriter(Writer, ArchiveMixin, PagerMixin, FeedMixin):
    writer_type = 'Folder Writer'

    def calc_folder_posts(self):
        for post in self.calc_archive_posts():
            folder = post.get('folder', None)
            if folder:
                yield folder, post

    def start(self):
        namespace.status.folders = []
        for folder, posts in self.calc_folder_posts():
            namespace.status.folders.append(folder)
        namespace.status.folders = set(namespace.status.folders)
        return 

    def run(self):
        _archive_tpl = namespace.site.get('folder_archive_template', None)
        _feed_tpl = namespace.site.get('folder_feed_template', None)
        for folder, posts in merge(self.calc_folder_posts()).iteritems():
            posts = sort_posts(posts)
            dest = os.path.join(folder, 'index.html')
            params = {'title': folder, 'folder': folder}
            if _archive_tpl: params.update({'tpl': _archive_tpl})
            self.write_pager(posts, dest, **params)

            dest = os.path.join(folder, 'feed.xml')
            params = {'title': folder, 'folder': folder}
            if _feed_tpl: params.update({'tpl': _feed_tpl})
            self.write_feed(posts, dest, **params)

class CategoryWriter(Writer, ArchiveMixin, PagerMixin, FeedMixin):
    writer_type = 'Category Writer'

    def calc_category_posts(self):
        key = namespace.site.get('category', 'category')
        for post in self.calc_archive_posts():
            category = post.get(key, None)
            if category:
                yield category, post

    def start(self):
        namespace.status.categories = []
        for cat, posts in self.calc_category_posts():
            namespace.status.categories.append(cat)
        namespace.status.categories = set(namespace.status.categories)
        return

    def run(self):
        key = namespace.site.get('category', 'category')
        _archive_tpl = namespace.site.get('category_archive_template', None)
        _feed_tpl = namespace.site.get('category_feed_template', None)
        for cat, posts in merge(self.calc_category_posts()).iteritems():
            posts = sort_posts(posts)
            dest = os.path.join(key, cat, 'index.html')
            params = {'title': cat}
            if _archive_tpl: params.update({'tpl': _archive_tpl})
            self.write_pager(posts, dest, **params)
            dest = os.path.join(key, cat, 'feed.xml')
            params = {'title': cat, 'folder':''}
            if _feed_tpl: params.update({'tpl': _feed_tpl})
            self.write_feed(posts, dest, **params)
