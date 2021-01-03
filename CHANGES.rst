.. _Changes:

*****************************
Patent2Net CHANGES (in short)
*****************************

##################
Patent2Net CHANGES
##################

2021-01-01 4.0.0-dev1
=====================
.. note::
 - Major improvements in the global architecture
 - P2N in now built on centOS v8
 - Added a docker image for Elasticsearch: 7.9.2 with carrot2 plugin (see https://github.com/carrot2/elasticsearch-carrot2). localhost:9200 and 9300 to access the Elasticsearch server
 - Added a docker image for Kibana: 7.9.2 (see https://www.elastic.co/fr/kibana). Also in the standard port 5601.
 - First version of P2N indexer that feed the elastic search indexer
.. warning:: 
 - ElasticSearch and Kibana are just here to start the new ways for P2N. At this time no features are provided at all. Specialists are welcome
 - Secure version of VSFTPD, fixed several security bugs (port 20-21). 

.. warning:: 
 User p2n with no passwd is set in Dockerfile. Mind in changing this if installing P2N on the cloud!


2020-11-30 3.1.0-dev5
=====================
- New processing feature in beta version (thanks Nezha): Trizifyer
- Major improvement in time processing in network production (using new libraries)
- but dynamic network aren't functional yet. Imrpove this

2020-07-20 3.1.0-dev4
=====================
- New features of "progess bar"
.. note::
 Help to fix the ugly page. UX and designer skills welcome!
- SSE system for all data processing scripts

2020-07-20 3.1.0-dev3
=====================
- Introduction of new libraries in various processing steps: pandas, mpld3, scipy
- New processing steps of data consolidation:
 - Applicants and Inventor Names normalisation (integration of a table from EPO with more than a million of entries)
 - Added more thant 2000 lines in previous file thank to URFIST project
 - New filtering process. Patents list collected from a request may contain (or not) equivalents patent. This tend to make biaises in several processing features of P2N. The new process extracts in the dataset the oldest patent in each subfamilies encountered in the set.
- several bug fixes
- added VSFTPD feature to communicate with the docker image

2020-06-20 3.1.0-dev2
=====================
- New branch: docker installation
- P2N works now in a standalone docker Ubuntu machine (Thanks Esteban).
 - Add Flask front end, localhost:5000 is the entry point.
 - Add update feature making p2n version allways uptodate. Static versions are useless from now.
 - Integration of several features (Pivot, Datatable)
 - Others exports (to IramuteQ or Carrot2) have to use the download data pages

2020-01-20 3.1.0-dev1
=====================
- firt publication of the automatic request splitter: a tool to skirt the 2000 limit of the EPO API
- various updates

2019 3.1.0-dev0
=====================

- various attemps in simplication of installation procedure
- many general bug fixes



development
===========
- Use ImageMagick for thumbnail generation in ``FusionImages.py``,
  see also https://github.com/Patent2net/P2N/issues/24
- Use "Pillow" for thumbnail generation, gracefully fall back to ImageMagick's "convert"

2018-03-20 3.0.0-dev6
=====================
- Make ``p2n adhoc dump`` output results either in "OpsExchangeDocument" or "Patent2NetBrevet" format
- Make ``p2n adhoc list`` output arbitrary fields of "OpsExchangeDocument" (projection)
- Improve documentation regarding CQL query language and updated command line parameters
- Introduce ad-hoc mode for generating JSON data suitable for
  feeding into PivotTable.js with Patent2NetBrevet data model
- Fix ``p2n adhoc dump`` with ``--with-register``
- Improve decoding raw JSON data into "OpsExchangeDocument" object instances
- Improve documentation
- Remove custom helper "attr_object_as_dict" in favor of vanilla "attr.asdict"
- Remove redundant "designated_states" field by using dotted name resolver
  for accessing "register.designated_states" when generating worldmap data
- Add support for PivotTable data generation in ad-hoc mode with "OPSExchangeDocument" data model
- Refactor maps.py and tables.py to "p2n.formatter" namespace
- Improve decoding of "OPSRegisterDocument"
- Improve error logging when decoding register information
- Decode historical data from register information
- Allow dotted attribute/field access for ``p2n adhoc list``
- Add advanced example about using ``jq`` to filter and reformat register information with ``p2n adhoc dump``
- Add convenience command ``p2n images`` for image data acquisition
- Properly display OPS error responses to the user, e.g. when
  submitting an invalid expression like ``--expression='foo=bar'``
- Add command ``p2n adhoc search`` for displaying search results only in raw OPS format
- Complete the data model for OPS Exchange Document
- Improve FusionImages.py
    - Add link to general template, fix and add context info for images
    - Image fusion
    - Improve layout/pagination for patent images gallery
    - Fix output thumbs
    - Add page size handler
- Improve gracefulness for Interface2.py and OPSGatherContentsV2-Images.py, see also #23.
- Fix ``p2n --version`` output, addressing #23. Thanks, @smorvan!

2017-12-01 3.0.0-dev5
=====================
- Attempt to add missing NameCountryMap.csv by providing MANIFEST.in file

2017-12-01 3.0.0-dev4
=====================
- Fix setup.py

2017-12-01 3.0.0-dev3
=====================
- Improve logging and error handling for register data acquisition

2017-12-01 3.0.0-dev2
=====================
- Add crawling behavior to new data acquisition subsystem
  to collect all results from OPS published data search
- Start project documentation based on Sphinx
- Improve documentation layout and move towards reStructuredText

2017-11-30 3.0.0-dev1
=====================
- Minor fixes re. argument processing
- Improve robustness re. case-sensitivity at map resource acquisition (countries.json)
- Add setup.py, convenience step runner and documentation
- Refactor scripts "FormateExportAttractivityCartography.py" and "FormateExportCountryCartography.py"
- Use utility function for accessing cles-epo.txt
- Upgrade to python-epo-ops-client==2.3.1, fixing access to OPS API 3.2
- Make p2n.maps.d3plus_data obtain single field attribute
- Memoize outcome of p2n.maps.read_name_country_map
- Introduce ad-hoc mode
- Worldmap generation in ad-hoc mode is now based on OPSExchangeDocument data model
- Enrich OPS bibliographic data by register information
- Add worldmap generation for designated states in ad-hoc mode
- Add automatic release task

2016-11-01 2.0.0
================
- Release Patent2Net 2.0.0

2014-10-30 1.0.0
================
- Future development will add scenaris of analysis (one scenary, one network e.G authors, applicants etc. to avoid the need of Gephi expert's skills)
- revisiting weight nodes on networks
- check abstracts gathering (seems lack of content)
- complete content gathering
- clean unused function and code everywhere ^_^

2014-03-04 0.9.0
================
- OpsGather-PatentList

    - Accept an Espacenet "smart search" query

- PatentsToNet

    - Fully connected graph is provided in Gephi, connecting any relation (intra and Inter field) : filtering can be done in Gephi or hacking in the Python script.
    - International Patent Classification is treated to be "truncated" at level 1,3,4,7. nodes for each level are created
    - Countries from Patent numbers (first deposit?) are considered as nodes
    - Kind codes (status) are separated as nodes
    - URL links as node attribute in gexf

        - for patent number : link to espacenet
        - for International Patent Classification IPC at level 1,3,4 : link to IPC database (French and English)

    - Dynamic graph are available over first available date (column "deb" and "fin" as to be merged as timeline for nodes and edges in data laboratoty in Gephi)
    - Directed graph is build complete in bidirection mode: Inventor-Inventor; IPC-IPC; Applicant-Applicant, and all combinations
    - Weight of nodes are provided as....
    - Weight among time are provided for node as ...
    - Weight of edges are provided as ....

2014-03-15 0.0.0
================
- Start public development
