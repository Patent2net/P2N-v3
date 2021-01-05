.. _release:

*******
Release
*******

.. warning:: Please help to fix it.  

	1. Entry point in doc/conf.py  
	2. linux functionality? Doen't work on the P2N installation on centOS  
	3. how to push on Read the docs ?
	
Prerequisites
=============
Run once to prepare the sandbox environment for release tasks::

    make setup-release

Cut a new release
=================
This will bump the version in setup.py, tag the repository and push to git origin.

Use from inside repository, with virtualenv activated.
::

    # Possible increments: major, minor, patch, dev
    make release bump=dev

