Changelog
===========

All history since the new Felix Felicis are listed here:

Version 3.6
------------

Released on Nov 2nd, 2012

+ ``clean_folder`` is replaced by ``folder``
+ ``clean_filepath`` is replaced by ``relative_filepath``
+ delete ``Post.embed_author``
+ livereload server work again
+ add ``resource.files`` params


Version 3.5
------------

Released on Oct 31th, 2012

+ fix ``liquidluck search`` unicode bug #57
+ add theme.debug vars for preview server


Version 3.4
------------

Released on Sep 20th, 2012

+ **ATTENTION**: settings.py in themes should be named as theme.py now
+ install and update theme
+ logging improvement


Version 3.3
-------------

Released on Sep 17th, 2012

+ support for [[]]
+ updates on default theme


Version 3.2
--------------

Released on Sep 13rd, 2012

+ bugfix for relative url
+ support for `````


Version 3.1
-------------

Released on Sep 12nd, 2012

+ bugfix
+ change server host to 127.0.0.1


Version 3.0
-------------

Released on Sep 12nd, 2012

+ new config format: yaml, python, json
+ redesigned


Version 2.0
------------

Released on Sep 7th, 2012

+ support for relative url
+ support for inject html, css, javascript
+ bugfix for server
+ code structure changed
+ github search api changed


Version 1.14
------------

Released on Oct 23th, 2012

+ add render params: writer
+ API changed. ``liquidluck.readers.base.Post``, delete ``filedir``, add ``clean_filepath``
+ force search theme from internet


Version 1.13
-------------

Released on Jul 16th, 2012

+ fix markdown meta parser
+ webhook deamon enhancement


Version 1.12
-------------

Released on Jul 9th, 2012

+ LiveReload Server
+ GitHub Search API fix
+ docutils is optional


Version 1.11
--------------

Released on Jun 20th, 2012

+ fix permalink filter, support {{filename}}/index.html now. #41
+ update default theme
+ improve command line interface. #43


Version 1.10
-------------

Released on Jul 17th, 2012

+ improve on feed render #40
+ config feed output tags
+ server bugfix
+ built in filters of tag_url and year_url


Version 1.9
------------

Released on Jul 4th, 2012

+ improve server, can be used as a standalone app with autoindex support
+ default permalink changed to {{date.year}}/{{filename}}
+ timezone fix
+ update theme


Version 1.8
------------

Released on Jul 1st, 2012

+ search theme from github
+ timezone support


Version 1.7
------------

Released on Jun 29th, 2012

+ webhook supports submodule
+ webhook supports hg
+ preview server #35


Version 1.6
------------

Released on Jun 29th, 2012

+ webhook support #33
+ add clean_title #32
+ table support in markdown


Version 1.5
------------

Released on Jun 28th, 2012.

+ bugfix for ``static_url`` encoding error
+ command line interface changed #31
+ update the default theme


Version 1.4
------------

Released on Jun 25th, 2012.

+ add TagCloudWriter
+ bugfix #24 #29


Version 1.3
-------------

Released on Jun 21th 2012.

+ customize markdown link transform
+ customize post class
+ add filedir property for post


Version 1.2
-------------

Released on Jun 19th 2012.

+ site['prefix'] configuration


Version 1.1
-------------

Released on Jun 19th 2012.

+ search and install theme available
+ bugfix issue#20

Version 1.0
-------------

Released on Jun 16th 2012. The new Felix Felicis.
