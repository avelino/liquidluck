.. _design-pattern:

Design Pattern
================


The design pattern of Felix Felicis contains one significant principle:

    Don't create anything.

That means we didn't (and will not) add any invalid markup like Jekyll
and others do. Everything should be valid in its markup language.

And hence there will be no plugin or extension like::

    {% gist id %}


The only things we do:

    Parse your posts correctly.

    Organize your posts correctly.


Readers should parse your posts correctly. And, Writers should organize your posts
correctly.

And we won't do any more.
