.. _setup:

#####
Setup
#####

This part of the documentation covers the installation of Patent2Net.
The first step to using any software package is getting it properly installed.
Please read this section carefully.

After successfully installing the software, you might want to
follow up with its :ref:`configuration`.


************
Installation
************
- Install docker desktop
- download the docker-install branch (https://github.com/Patent2net/P2N-v3/tree/docker_install)
- Use the Install_P2N.bat and enjoy P2N via docker image
- See Install.bat in the elatickibana directory for the full architecture (BETA)

*****
Usage
*****
- setup your API key (http://localhost:5000/get_started)
- enjoy the request form (http://localhost:5000/form) to make your requests and see progress (Help need to fix UX and SSE consolidate)
- explore results: http://localhost:5000/index
- please help in user design interface!

************
Old ways
************
Install from source
===================
- Download Anaconda 3 (big installation, https://www.anaconda.com/distribution/) OR Miniconda https://docs.conda.io/en/latest/miniconda.html
- Download P2N latest https://github.com/Patent2net/P2N-v3
- Unzip to a the P2N directory (please choose a safe path: the root of your second hard drive (d:\P2N) for instance is the prefered choice)
- Launch (double click) installP2N.bat (let it work; do not close windows; that process can be quite long depending on you machine and network access)
- Copy or create cles-epo.txt file (be aware must be ANSI encode caracters!). See https://docs.ip-tools.org/patent2net/configure.html
- Formulate the desired *.cql file in ./REQUESTS/ directory. See https://docs.ip-tools.org/patent2net/usage/index.html 
- Double click runP2N.bat and have fun!


Nexr seems broken
- Source releases are available from GitHub: https://github.com/Patent2net/P2N/releases
- Install a specific version::

    pip install 'https://github.com/Patent2net/P2N/archive/3.0.0-dev6.tar.gz' --upgrade

- Install the current development version::

    pip install 'https://github.com/Patent2net/P2N/archive/develop.tar.gz' --upgrade



Install binary package (Old features)
======================
- | Binary releases are available at
  | http://patent2netv2.vlab4u.info/dokuwiki/doku.php?id=user_manual:download_install



********
Appendix
********

Install ImageMagick
===================

On Debian Linux::

        apt install imagemagick

On Windows::

        https://www.imagemagick.org/script/download.php#windows


Install Patent2Net on Linux
===========================
If you're using Ubuntu or Debian distributions, make sure to have these prerequisites installed::

    sudo apt-get install python-pip build-essential python-dev libjpeg-dev libxml2-dev libfreetype6-dev libpng-dev

Install pygraphviz on Mac OS X::

    pip install --install-option="--include-path=/opt/local/include" --install-option="--library-path=/opt/local/lib" "pygraphviz==1.3.1"


Install Patent2Net on Windows
=============================
- Install Graphviz (I used 2.38)
- Anaconda

    - Starting from Anaconda 2.7 installation (32 or 64 bits)
    - To install Anaconda go to https://www.continuum.io/downloads
    - Use Anaconda 4.2.0 or superior version
    - Use Python 2.7 version

- Then::

    pip install --upgrade requests
    pip install --upgrade networkx
    pip install --upgrade setuptools

- Download the epo_ops directory of https://github.com/55minutes/python-epo-ops-client in ...\Anaconda2\Lib\site-packages
- In IPython: import epo_ops
- Download curses http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses followed by
  ``pip install curses-2.2-cp2.7(...).whl``
- Download https://bitbucket.org/taynaud/python-louvain followed by
  ``python setup.py install``
- Install pygraphviz (for 64 bits use: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygraphviz)
- ``pip install --upgrade jinja2``

