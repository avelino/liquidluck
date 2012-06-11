#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
install_requires = ['docutils', 'Jinja2', 'Pygments', 'misaka']
try:
    import argparse  # python 2.7+ support argparse
except ImportError:
    install_requires.append('argparse')


import liquidluck

setup(
    name='liquidluck',
    version=liquidluck.__version__,
    author=liquidluck.__author__,
    author_email='lepture@me.com',
    url='http://project.lepture.com/liquidluck/',
    packages=['liquidluck', 'liquidluck.writers', 'liquidluck.readers'],
    description='A lightweight static weblog generator',
    license='BSD License',
    entry_points={
        'console_scripts': ['liquidluck= liquidluck.cli:main'],
    },
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Text Processing :: Markup',
    ]
)
