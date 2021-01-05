***************************
Contribute to documentation
***************************
.. image:: https://readthedocs.org/projects/p2n-v3/badge/?version=latest
:target: https://p2n-v3.readthedocs.io/en/latest/?badge=latest
:alt: Documentation Status

============
Introduction
============
Beautiful static HTML documentation can be easily built using the Sphinx documentation generator.
Sphinx uses `reStructuredText <https://docutils.sourceforge.io/docs/user/rst/quickref.html>`_ as its markup language, and many of its strengths come from the power
and straightforwardness of reStructuredText.

The documentation can be built locally and also will be published to https://docs.ip-tools.org/patent2net/.
It is also pushed to https://readthedocs.org/.

.. _note: it seems that latexmk fails due to svg graphics. (badges included from shield.io or readthedoc...

=====
Usage
=====

On Linux
--------

Build HTML::

    make docs-html

Display::

    open doc/_build/html/index.html

.. warning:: I couldn't achieive this on the centOs docker image. I had to hack the make procedure. See ./update.sh file. Help to fix please.


On Windows
----------

Build HTML::

    cd doc
    make.bat html

Display::

    open _build/html/index.html

Clean start::
	
	make.bat clean