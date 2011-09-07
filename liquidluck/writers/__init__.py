
import os

from liquidluck.writer import Writer
from liquidluck.reader import rstReader
from liquidluck.utils import Temp, Pagination
from liquidluck.utils import merge, xmldatetime

class ArchiveMixin(object):
    def calc_archive_rsts(self):
        for f in self.walk(self.postdir):
            if f.endswith('.rst'):
                rst = rstReader(f)
                if rst.get_info('public', 'true') != 'false':
                    yield rst

class FeedMixin(object):
    def write_feed(self, rsts, dest='feed.xml'):
        count = int(self.config.get('feed_count',10))
        rsts = rsts[:count]
        _tpl = self.config.get('feed_template', 'feed.xml')
        return self.write({'rsts':rsts}, _tpl, dest)

    def register(self):
        self.register_filter('xmldatetime', xmldatetime)

class PagerMixin(object):
    def write_pager(self, rsts, dest='archive.html'):
        perpage = int(self.config.get('perpage', 30))
        paginator = Pagination(rsts, perpage)
        _tpl = self.config.get('archive_template', 'archive.html')

        # first page
        folder, filename = os.path.split(dest)

        pager = paginator.get_current_page(1)
        pager.folder = folder

        self.write({'pager': pager}, _tpl, dest)

        for p in range(paginator.pages):
            dest = os.path.join(folder, 'page', '{0}.html'.format(p+1))
            pager = paginator.get_current_page(p+1)
            pager.folder = folder
            self.write({'pager': pager}, _tpl, dest)


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

    def _write_post(self, rst):
        _tpl = rst.get_info('template', 'post.html')
        self.write({'rst':rst}, _tpl, rst.destination)

    def run(self):
        for f in self.walk(self.postdir):
            if f.endswith('.rst'):
                rst = rstReader(f)
                self._write_post(rst)

class IndexFeedWriter(Writer, ArchiveMixin, FeedMixin):
    def register(self):
        self.register_filter('xmldatetime', xmldatetime)

    def run(self):
        rsts = self.sort_rsts(self.calc_archive_rsts())
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
            dest = os.path.join(year, 'feed.xml')
            self.write_feed(rsts, dest)

class TagWriter(Writer, ArchiveMixin):
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

class FolderWriter(Writer, ArchiveMixin, FeedMixin):
    def calc_folder_rsts(self):
        for rst in self.calc_archive_rsts():
            folder = rst.get_info('folder')
            if folder:
                yield folder, rst

    def run(self):
        for folder, rsts in merge(self.calc_folder_rsts()).iteritems():
            rsts = self.sort_rsts(rsts)
            self.register_context('title', folder)

            dest = os.path.join(folder, 'index.html')
            self.write_pager(rsts, dest)
            dest = os.path.join(k, 'feed.xml')
            self.write_feed(rsts, dest)
