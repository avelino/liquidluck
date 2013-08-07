# coding: utf-8

import os
from liquidluck.readers.markdown import MarkdownReader


def test_markdown_reader():
    root = os.path.abspath(os.path.dirname(__file__))
    mr = MarkdownReader(root)
    post = mr.read(os.path.join(root, 'cases', 'readers-markdown.md'))
    assert post.title == 'Markdown'
    assert post.tags == ['python', 'markdown']
    assert post.relative_filepath == 'cases/readers-markdown.md'
    assert 'description' in post.meta
