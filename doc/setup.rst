.. _setup:


###########
Quick start
###########

This part of the documentation covers the installation of Patent2Net.
The first step to using any software package is getting it properly installed.
Please read this section carefully.

************
Installation
************
#. Install docker desktop
#. download the docker-install repository (https://github.com/Patent2net/P2N-Docker)
#. Use the Install_P2N.bat and enjoy Patent2Net via docker image
#. See Install.bat in the elatickibana directory for the full architecture (BETA) with elastic search and Kibana
#. Refer to :ref:`docker-install` procedures for details

**************
Configuration
**************
- setup your EPO's API key in the `get_started page: <http://localhost:5000/get_started)>`_
- enjoy the request form (http://localhost:5000/form) to make your requests and see progress (Help need to fix UX and SSE consolidate)
- explore results: http://localhost:5000/index
- please help in user design interface!
- go to the :ref:`docker-config` section for details on the interface
- see :ref:`usage` for details.

***************************
The old way for developpers
***************************

.. tip:: the following on this page concerns developpers and avanced users information. Welcome to new users that should follow first theses pages :ref:`docker-install`, :ref:`usage`.


.. include:: ./historic/install.rst
