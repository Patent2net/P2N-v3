.. _configuration:

*************
Configuration
*************

This part of the documentation covers the configuration of Patent2Net.
The second step to using any software package is getting it properly configured.
Please read this section carefully.

After successfully configuring the software, you might want to
follow up reading about its :ref:`usage`.


OPS credentials
===============
Patent2Net needs your personal credentials for accessing the OPS API.
You have to provide them once as they are stored into the file
``cles-epo.txt`` in the current working directory.

There is a convenience command for initializing Patent2Net with your OPS credentials::

    p2n ops init --key=ScirfedyifJiashwOckNoupNecpainLo --secret=degTefyekDevgew1

.. note:: The Patent2Net scripts expect to find the file ``cles-epo.txt`` in the projects' root folder.


OPS registration
================

Please follow the `Register P2N with OPS`_ documentation to install your
OPS OAuth credentials in the "``cles-epo.txt``" file in the root directory.

.. _Register P2N with OPS: http://patent2netv2.vlab4u.info/dokuwiki/doku.php?id=user_manual:download_install#register_the_use_of_p2n

