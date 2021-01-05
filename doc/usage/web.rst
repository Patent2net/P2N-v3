.. contents::
   :local:
   :depth: 1

=============
Web interface
=============
You can interact with Patent2Net using a HTML5 compliant browser. Best results using Firefox or chrome are acheived. 
The main interface is on port 5000. You can access the home page using the adress: http://localhost:5000

Home page
---------
The Home page welcomes you and offers a button to update Patent2Net code and keep is always up to date

Get Started 
-----------
Get Started has to be used once to insert your `Open Patent Services API (OPS) keys <https://www.epo.org/searching-for-patents/data/web-services/ops.html>`_. follow their instructions to get one.

Request 
-------
 
Request is a form to build your requests. 
* Enter a request in CQL format. See the EPO's `pocket guide <http://documents.epo.org/projects/babylon/eponet.nsf/0/8C12F50E07515DBEC12581B00050BFDA/$File/espacenet-pocket-guide_en.pdf>`_.
 
 .. tip:: You can use the advanced search interface `provided by the EPO <https://worldwide.espacenet.com/patent/search?>`_. Consider using the menu at the left side (the blue     square on the image below) to build you request by selecting the fields of search (Title, abstract, date, names, classification), the binary operators (OR, AND, NOT) between the fields and do the search. The interface fills the research form with the request formulated in CQL format that you can copy and paste to the Patent2Net form (the red circle on the image). You can also check the number of patents in the database (the green ellipse).
 .. image:: ../dev/images/EPO-CQL.png
 
 .. note:: if your request expects more than 2000 patents you must consider to split your request in several subrequests. P2N offers two scripts for this (AutomRequest3.py and AutomRequestSpliterTime.py) but it's not web friendly nor documented yet and you have to use them in :ref:`bash mode`.
 
* Enter a data directory to save all files gathered and processed by P2N. 
 
 .. tip:: choise lower case name without accents or space or strange caracter is often a best choice.
 
* Requests options are binary paremeter to proceed to the several processings steps  
* The submit button will launch your request and you can see (beta  ugly version) progress bar of the several processing tools.  
* The left panel is a direct entry to previous requests operated. Its a list of the datadirectories you filed pointing directly to the page of results.  
 
Index 
-----
* This page is where you can find your results. It points out the list of the datadirectories you filed in the request form pointing directly to the page of results

Download Data 
-------------
* This button allows you to download all the data directory in zip format to you computer file system (out of the docker machine).

.. note:: You can also use an FTP client with the address localhost, user p2n and no pass.

