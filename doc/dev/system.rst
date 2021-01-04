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

Web interface
-------------
You can interact with Patent2Net using a HTML5 compliant browser. Best results using Firefox or chrome are acheived. 
The main interface is on port 5000. You can access the home page using the adress: http://localhost:5000

Home page
^^^^^^^^^
* Home page welcomes you and offers a button to update Patent2Net code and keep is always up to date

Get Started 
^^^^^^^^^^^
* Get Started has to be used once to insert your `Open Patent Services API (OPS) keys <https://www.epo.org/searching-for-patents/data/web-services/ops.html>`_. follow their instructions to get one.

Request 
^^^^^^^
 
* Request is a form to build your requests. 
 * Enter a request in CQL format.
 
 .. tip:: You can use the advanced search interface `provided by the EPO <https://worldwide.espacenet.com/patent/search?>`_. Consider using the menu at the left side (the blue     square on the image below) to build you request by selecting the fields of search (Title, abstract, date, names, classification), the binary operators (OR, AND, NOT) between the fields and do the search. The interface fills the research form with the request formulated in CQL format that you can copy and paste to the Patent2Net form (the red circle on the image). You can also check the number of patents in the database (the green ellipse).
 .. image:: images/EPO-CQL.png
 
 .. note:: if your request expects more thant 2000 patent you must consider to split your request in several subrequest. P2N offers a script for this (AutomRequest3.py and AutomRequestSpliterTime.py) but it's not web friendly nor documented yet...
 
 * Enter a data directory to save all files gathered and processed by P2N. 
 
 .. tip:: choise lower case name without accents or space or strange caracter is often a best choice.
 
 * Requests options are binary paremeter to proceed to the several processings steps  
 * The submit button will launch your request and you can see (beta  ugly version) progress bar of the several processing tools.  
 * The left panel is a direct entry to previous requests operated. Its a list of the datadirectories you filed pointing directly to the page of results.  
 
Index 
^^^^^
* This page is where you can find your results. It points out the list of the datadirectories you filed in the request form pointing directly to the page of results

Download Data 
^^^^^^^^^^^^^
* This button allows you to download all the data directory in zip format to you computer file system (out of the docker machine).

.. note:: You can also use an FTP client with the address localhost, user p2n and no pass.

