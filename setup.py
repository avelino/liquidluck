#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='liquidluck',
    version='1.0',
    author='Hsiaoming Young',
    author_email = 'sopheryoung@gmail.com',
    url = 'http://github.com/lepture/liquidluck',
    packages=['liquidluck', 'liquidluck.writers', 'liquidluck.readers'],
    description='a static weblog generator',
    long_description='a static weblog generator',
    license='BSD License',
    entry_points = {
        'console_scripts': ['liquidluck= liquidluck.cli:main'],
    },
    install_requires=['docutils', 'Jinja2', 'Pygments'],
    include_package_data = True,
)
