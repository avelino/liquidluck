.. _installation:

Installation
=============

If you are familiar with Python, it is strongly suggested that you install
everything in virtualenv.

If you are a pythoner, and you have no idea about virtualenv, please do search
the internet.

Distribute and Pip
------------------

If you are on Linux or Mac OS X, you are the lucky one::

    $ sudo pip install liquidluck

If no pip available, try easy_install::

    $ sudo easy_install liquidluck


Sorry, I have no knowledge about Windows, but it really works on Windows.
Cygwin and MinGW would make a better life with UNIX software.


Install with GIT
-----------------

If you prefer git, that is great. You can get the very latest code at GitHub::

    $ git clone http://github.com/lepture/liquidluck.git


Mac User Attention
---------------------

We use misaka_ (python wrapper for sundown_) as the Markdown engine. It requires
C compiler, which means you should install Xcode.

Then open Xcode's preference (command + ,), select ``Downloads`` tab, and install
``Command Line Tools``.

I strongly suggest that you install the ``Command Line Tools``, even if you don't
use Felix Felicis. You will need it somewhere else.

.. _misaka: http://misaka.61924.nl
.. _sundown: https://github.com/tanoku/sundown
