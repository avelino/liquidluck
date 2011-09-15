
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
        path = os.path.join(a, *args)
        path = '{0}/'.format(path.rstrip('/'))
        if not path.startswith('http://'):
            path = '/{0}'.format(path.lstrip('/'))
        return path

    def register(self):
        self.register_context('content_url', self._content_url)

    def _calc_rel_rsts(self):
        public_rsts = []
        secret_rsts = []
        for rst in self.total_files[0]:
            if rst.get_info('public', 'true') != 'false':
                public_rsts.append(rst)
            else:
                secret_rsts.append(rst)
        public_rsts = self.sort_rsts(public_rsts)
        i = 0
        count = len(public_rsts)
        for rst in public_rsts:
            if i > 0:
                public_rsts[i].prev = public_rsts[i-1]
            if i + 1 < count:
                public_rsts[i].next = public_rsts[i+1]
            i += 1
        rsts = public_rsts
        rsts.extend(secret_rsts)
        return rsts


    def _write_post(self, rst):
        _tpl = rst.get_info('template', 'post.html')
        dest = os.path.join(self.deploydir, rst.destination)
        if os.path.exists(dest) and rst.mtime < os.stat(dest).st_mtime:
            logger.info('Ignore ' + dest)
            return
        self.write({'rst':rst}, _tpl, rst.destination)

    def run(self):
        for rst in self._calc_rel_rsts():
            self._write_post(rst)

class FileWriter(Writer):
    def run(self):
        for source in self.total_files[1]:
            path = source.replace(self.postdir,'').lstrip('/')
            dest = os.path.join(self.deploydir, path)
            self.copy_to(source, dest)

class IndexWriter(Writer, ArchiveMixin, PagerMixin, FeedMixin):
    def run(self):
        rsts = self.sort_rsts(self.calc_archive_rsts())
        self.register_context('title', 'Archive')
        self.register_context('folder', '')
        dest = self.config.get('index', 'archive.html')
        self.write_pager(rsts, dest)
        self.write_feed(rsts, dest='feed.xml')

class YearWriter(Writer, ArchiveMixin, PagerMixin, FeedMixin):
    def calc_year_rsts(self):
        for rst in self.calc_archive_rsts():
            date = rst.get_info('date')
            yield date.year, rst

    def run(self):
        for year, rsts in merge(self.calc_year_rsts()).iteritems():
            rsts = self.sort_rsts(rsts)
            year = str(year)
            self.register_context('title', year)
            dest = os.path.join(year, 'index.html')
            self.write_pager(rsts, dest)

class TagWriter(Writer, ArchiveMixin, PagerMixin):
    def calc_tag_rsts(self):
        for rst in self.calc_archive_rsts():
            tags = rst.get_info('tags')
            for tag in tags:
                yield tag, rst

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
        tagcloud = merge(self.calc_tag_rsts())
        self.write_tagcloud(tagcloud)
        for tag, rsts in tagcloud.iteritems():
            rsts = self.sort_rsts(rsts)
            self.register_context('title', tag)

            dest = os.path.join('tag', tag + '.html')
            self.write_pager(rsts, dest)

class FolderWriter(Writer, ArchiveMixin, PagerMixin, FeedMixin):
    def calc_folder_rsts(self):
        for rst in self.calc_archive_rsts():
            folder = rst.get_info('folder')
            if folder:
                yield folder, rst

    def run(self):
        for folder, rsts in merge(self.calc_folder_rsts()).iteritems():
            rsts = self.sort_rsts(rsts)
            self.register_context('title', folder)
            self.register_context('folder', folder)

            dest = os.path.join(folder, 'index.html')
            self.write_pager(rsts, dest)
            dest = os.path.join(folder, 'feed.xml')
            self.write_feed(rsts, dest)
