.. _goodies:


Goodies
==========

Gifts that makes Felix Felicis easy to use.


Oh My Zsh Plugin
------------------

If you are using `oh-my-zsh <https://github.com/robbyrussell/oh-my-zsh>`_,
there is a plugin for you.

https://github.com/lepture/liquidluck/tree/master/oh-my-zsh-plugins

Copy ``liquidluck`` to ``~/.oh-my-zsh/plugins``::

    $ cp -r oh-my-zsh-plugins/liquidluck ~/.oh-my-zsh/plugins/

Then edit your zshrc file::

    plugins=(git ... liquidluck)

Now you can tab complete every Felix Felicis command::

    $ liquidluck b(tab)
    $ liquidluck build (tab)


Webhook
----------

Felix Felicis supports webhook since v1.6. When you push to GitHub or BitBucket,
your blog can generate itself.

First, you need to install Felix Felicis on your server::

    $ pip install liquidluck

Second, your blog repo on your server::

    $ git clone git://path/to/your/repo blog

Then, start webhook daemon in your blog::

    $ cd blog
    $ liquidluck webhook start -p 9876


Configure webhook on GitHub or BitBucket. We take GitHub as an example.

Head over to your blog source repo admin, select **Service Hooks**

.. image:: http://i.imgur.com/dE4rX.jpg
    :alt: github service hook

If you prefer BitBucket, you should select the POST service:

.. image:: http://i.imgur.com/K4HfA.jpg
    :alt: bitbucket service hook

If your server ip is 88.88.88.88, you can add a URL::

    http://88.88.88.88:9876/webhook

And when you push to GitHub, your server will update the repo and generate the whole site.
