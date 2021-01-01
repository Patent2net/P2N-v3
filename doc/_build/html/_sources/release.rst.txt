.. _release:

#######
Release
#######

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

