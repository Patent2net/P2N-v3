********************
System configuration
********************

.. _docker-config:
.. _docker-install:

Dealing with docker version
===========================

Generalities
------------
`The docker version <https://github.com/Patent2net/P2N-Docker>`_ installs for you a Docker machine with a fully functionnal system Patent2Net. The machine is built on CentOS 8 and installs all libraries needed for the python 3.6 using Anaconda distribution.

*Install.bat* makes everything you need for Patent2Net once you have `Docker Desktop installed <https://docs.docker.com/get-docker/>`_. It installs the system, creates the user p2n (no rights) and install a vsftpd server.

.. note:: a special volume name p2nData is mounted on p2n homedir

.. tip:: *Run_P2N.bat* is the script that launches Patent2Net, opens necessary ports and a VSFTP server to download or upload file to your P2N container and attachs the volume p2nData

.. tip:: *Stop_P2N.bat* stops the container.

In the directory _Uninstall_ you will find all the stuff to unistall properly P2N. You could also use the Docker Desktop interface to stop the container, remove it and remove the image (in that specific order or it will fail). 

In the same directory you find a elastickibana directory. Inside you will find another *install.bat*. this one is dedicated to a install two servers: the first is an Elastic Search server. The second server is a Kibana instance. Configuration is done to listen the *P2N-Indexer* tool.

.. tip:: *Elastic search* is only used for providing data to the Carrot2 plugin. Kibana is also just here to start to work with it!

Dealing out of docker version
=============================
If you prefer you can install patent2Net in an anaconda environment. We guess that you know what you do. Refer then to the :ref:`historicdevmod` section.
