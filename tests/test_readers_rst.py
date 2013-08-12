# coding: utf-8

import os
from liquidluck.readers.rst import RstReader


def test_rst_reader():
    root = os.path.abspath(os.path.dirname(__file__))
    mr = RstReader(root)
    post = mr.read(os.path.join(root, 'cases', 'readers-rst.rst'))
    assert post.title == 'rst'
    assert post.tags == ['python', 'rst']
    assert post.relative_filepath == 'cases/readers-rst.rst'
