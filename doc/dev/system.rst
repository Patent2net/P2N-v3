####################
System configuration
####################

Dealing with docker version
===========================

Generalities
------------
`The docker version <https://github.com/Patent2net/P2N-Docker>`_ installs for you a Docker machine with a fully functionnal system Patent2Net. The machine is built on CentOS 8 and installs all libraries needed for the python 3.6 using Anaconda distribution.
:: Install.bat makes everything you need for Patent2Net once you have `Docker Desktop installed <https://docs.docker.com/get-docker/>`_. It installs the system, creates the user p2n (no rights) and install a vsftpd server.
.. note:: a special volume name p2nData is mounted on p2n homedir

:: Run_P2N.bat is the script that launches Patent2Net, opens necessary ports and a VSFTP server to download or upload file to your P2N container and attachs the volume p2nData

:: Stop_P2N.bat stops the container.

:: In the directory Uninstall you will find all the stuf to unistall properly P2N. You could also use the Docker Desktop interface to stop the container, remove it and remove the image (in that specific order or it will fail). 

:: In the same directory you find a elastickibana directory. Inside you will find another install.bat

.. tip:: Elastic search is only used for providing data to the Carrot2 plugin. Kibana is just here to start to work with it!

Interface
---------
You can interact with Patent2Net using a HTML5 compliant browser. Best results using Firefox or chrome are acheived. 
The main interface is on port 5000. You can access the home page using the adress: http://

