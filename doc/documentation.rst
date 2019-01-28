#############
Documentation
#############


************
Introduction
************
Beautiful static HTML documentation can be easily built using the Sphinx documentation generator.
Sphinx uses reStructuredText as its markup language, and many of its strengths come from the power
and straightforwardness of reStructuredText.

The documentation can be built locally and also will be published to https://docs.ip-tools.org/patent2net/.
It could also be pushed to https://readthedocs.org/.


*****
Usage
*****

On Linux
========

Build HTML::

    make docs-html

Display::

    open doc/_build/html/index.html


On Windows
==========

Build HTML::

    cd doc
    make.bat

Display::

    open _build/html/index.html

