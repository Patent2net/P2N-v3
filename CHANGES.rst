##################
Patent2Net CHANGES
##################


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
