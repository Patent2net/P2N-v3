###################
Todo list and ideas
###################

Version 4.0.0
=============
******
Agenda
******
.. note:: 
 - ASAP
 - when practioners are decides and can be recruited
 - and when the weather is not so fine
 
Completed
---------
- [x] Avoid the installation procedure by the use of a docker image
- [x] Many bug fixing and data consolidation
- [x] Integrate the full documentation system in the flask interface
- [x] Use of the docker powerfull feature to extend the global architecture to an ElasticSearch server and it's Kibana brother (or sister I don't mind in fact). Opening to new ways of exploration
- [x] Carrot2 plugin integration

Todo
----
- [o] Kibana and elastic search usage
- [o] Some Iramuteq processing steps coulb directly part of P2N
- [o] Mindmaps integration in the full web system
- [o] Network visualisation and exploring tool integration. Actual Gexf-js interface is a poorly downgrade of Gephi features and data integrated by P2N in network representations.
- [o] Write documentation about data model 
- [o] Write documentation about usage
- [o] Write documentation about global architecture

### User UX improvements

* Use flask and templates to re-design the whole interface keeping in mind kibana and Elatic Search new capability
* improve progress bar design page

### Others improvements

> Although Patent2Net is fully operational, works fine and is enough to begin using Patent Information, a lot can be done to improve analysis:
 * Correct the issues (continuous process, of course)
 * Add some more information in the result html page (ModeleContenuIndex.html). Great to add the processing date (thus can be different from the gathering date) and P2N version
 * As information analysis do not always represent the whole _Patent Universe (PU)_ (for instance french abstracts only) metrics should provide the proportion of P.U. concerned by each analysis
 * Treat Designated State(s) information for EP and WO patentes to complete the attractivity maps. Check if register information recently added (thanks amotl)
 * Improve the Mindmap option to get it more efficient for creativity (Celso is still working on?)


New contributions and ideas are always welcome.


*****
Tasks
*****
New capabilities
================
Added some new capabilities to Patent2Net, i.e.:

* Within the Patent Universe, build a drawings gallery with hyperlink to the Espacenet patent 
* Within the Familly Patent Universe, provide all the same analysis as with the Patent Universe 
Todo
* Include the treatment of the Cooperative Patent Classification (CPC) with the proportion of P.U. concerned (http://www.cooperativepatentclassification.org/Archive.html)
* Build a small database to display results of a specific (Familly) Patent Universe. Database could be [PouchDB] (https://pouchdb.com/) or equivalent


New ways for gathering and analysis
===================================
Provide some new ways of gathering and analysis of patent information, i.e.:

* Within the Familly Patent Universe, provide a new range of analysis, considering a familly as a unique entity (invention)
* Limit the Familly Patent Universe to the only Priority patents, and provide a complete analysis
* Using citations of the Familly Patent Universe, provide genealogic analysis, especially descendants to try to detect invention fronts.
* Gather research reports when avalaible and provide analysis chains

Version 3.0.0
=============

Completed
---------
- [x] Introduce and stabilize new data model and ad-hoc mode
- [x] Write about "jq"
- [x] Remove attr_object_as_dict in favor of attr.as_dict
- [x] Resolve doc.designated_states vs. doc.register.designated_states duplication by providing a dotted name resolver for nested objects
- [x] Refactor maps.py and tables.py to ``p2n.formatter`` namespace
- [x] "p2n adhoc dump --format=raw" mode
- [x] Display OPS error message when running invalid queries like "p2n adhoc dump --expression='pa=grohe and py=2015'"

Todo
----

- [o] OPS Register: Always sort event-like data in ascending order?
      Right now, sort order is mixed as of "history items" vs. "actions" vs. "{publication,application}_reference".
- [o] Write documentation about data model
- [o] Complete implementation of ``Patent2NetBrevet.from_ops_exchange_document`` re. citations, equivalents and more
- [o] Complete implementation of ``OPSRegisterDocument``
- [o] Install Webhook on GitHub for automatic documentation building
- [o] Upload pre-release versions to PyPI
- [o] Currently, python-epo-ops-client requires to be online because it always attempts to authenticate.
      Could this be deferred to the actual first remote access to be able to work completely offline with a prewarmed cache?
- [o] Caching improvements
    - [o] Increase dogpile cache duration to one year
    - [o] Provide api/command to clear the cache
    - [o] More fine-grained cache ttl control
- [o] Use pyjq for providing built-in filtering, with raw or even named filters.
      https://pypi.python.org/pypi/pyjq
- [o] Should we compute "register.designated_states - register.countries_lapsed" to determine the actual
      list of countries the patent is still valid in?
