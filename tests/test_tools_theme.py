import os
from liquidluck.tools.theme import search, install

ROOT = os.path.abspath('.')


def test_search():
    search()


def test_search_keyword():
    search('moment')
    search('liquidluck')


def test_install():
    install('liquidluck')
    install('moment')
    assert os.path.exists(os.path.join(ROOT, '_themes/moment'))
