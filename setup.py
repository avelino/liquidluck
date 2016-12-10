#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from setuptools import setup
import liquidluck
from email.utils import parseaddr


kwargs = {}
major, minor = sys.version_info[:2]
if major >= 3:
    kwargs['use_2to3'] = True

install_requires = [
    'Jinja2', 'Pygments', 'hoedown<=0.1.1', 'docopt', 'PyYAML', 'docutils<=0.10'
]

author, author_email = parseaddr(liquidluck.__author__)

setup(
    name='liquidluck',
    version=liquidluck.__version__,
    author=author,
    author_email=author_email,
    url=liquidluck.__homepage__,
    packages=['liquidluck', 'liquidluck.writers', 'liquidluck.readers',
              'liquidluck.tools'],
    description='A lightweight static weblog generator',
    long_description=open('README.rst').read(),
    license='BSD License',
    entry_points={
        'console_scripts': ['liquidluck= liquidluck.cli:main'],
    },
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Text Processing :: Markup',
    ],
    **kwargs
)
