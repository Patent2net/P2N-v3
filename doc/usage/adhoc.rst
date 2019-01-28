###########
Ad-hoc mode
###########

The ad-hoc mode allows to specify the query expression on the command line.
This gives Patent2Net a more interactive mode of operation.

.. contents::
   :local:
   :depth: 1


----


************
Data dumpers
************
These actions run the query against OPS and display decoded/polished information in JSON format.

You might want to have a look at the :ref:`jq` documentation for working with JSON data on the command line.


Full bibliographic data
=======================
Display bibliographic data for given query expression::

    p2n adhoc dump --expression='TA=lentille'

Expand each hit to its whole family::

    p2n adhoc dump --expression='TA=lentille' --with-family

Enrich each document with its register information::

    p2n adhoc dump --expression='TA=lentille' --with-family --with-register

For dumping data using the legacy Patent2Net brevet format::

    p2n adhoc dump --expression='TA=lentille' --format=brevet


Single bibliographic data field
===============================
Display list of publication numbers for given query expression::

    p2n adhoc list --expression='TA=lentille'
    p2n adhoc list --expression='TA=lentille' --with-family

Display list of application numbers in epodoc format::

      p2n adhoc list --expression='TA=lentille' --field='application_number_epodoc'

Display list of ``register.status`` values::

    p2n adhoc list --expression='TA=lentille' --with-family --with-register --field='register.status'

.. note:: You can use all fields available in the OPSExchangeDocument data model.


----


***************
Data formatters
***************

Generate data for world maps using d3plus/geo_map (JSON)::

    p2n adhoc worldmap --expression='TA=lentille' --country-field='country'
    p2n adhoc worldmap --expression='TA=lentille' --country-field='country' --with-family
    p2n adhoc worldmap --expression='TA=lentille' --country-field='applicants'
    p2n adhoc worldmap --expression='TA=lentille' --country-field='inventors'
    p2n adhoc worldmap --expression='TA=lentille' --country-field='register.designated_states' --with-register


Generate data suitable for PivotTable.js (JSON)::

    p2n adhoc pivot --expression='TA=lentille' --with-family


----


********
Synopsis
********


Output of "``p2n --help``"
==========================
::

    $ p2n --help

    -----------
    Ad hoc mode
    -----------
      p2n ops init                          Initialize Patent2Net with OPS OAuth credentials
      p2n adhoc search                      Display search results for given query expression in raw OPS format (JSON)
      p2n adhoc dump                        Display full results for given query expression in OpsExchangeDocument or Patent2NetBrevet format (JSON)
      p2n adhoc list                        Display list of values from single field for given query expression
      p2n adhoc worldmap                    Generate world map for given query expression over given field
      p2n adhoc pivot                       Generate data for pivot table

    Options:
      --expression=<expression>             Search expression in CQL format, e.g. "TA=lentille"
      --format=<format>                     Control output format for "p2n adhoc dump",
                                            Choose from "ops" or "brevet" [default: ops].
      --field=<field>                       Which field name to use with "p2n adhoc list" [default: document_number].
      --with-register                       Also acquire register information for each result hit.
                                            Required for "--country-field=register.designated_states".
      --country-field=<country-field>       Field name of country code for "p2n adhoc worldmap"
                                            e.g. "country", "applicants", "inventors", "register.designated_states"

    Examples:

      # Initialize Patent2Net with OPS OAuth credentials
      p2n ops init --key=ScirfedyifJiashwOckNoupNecpainLo --secret=degTefyekDevgew1

      # Run query and output results in OpsExchangeDocument format (JSON)
      p2n adhoc dump --expression='TA=lentille'

      # Run query and output results in Patent2NetBrevet format (JSON)
      p2n adhoc dump --expression='TA=lentille' --format=brevet

      # Run query and output list of document numbers, including family members (JSON)
      p2n adhoc list --expression='TA=lentille' --with-family

      # Run query and output list of application numbers in epodoc format
      p2n adhoc list --expression='TA=lentille' --field='application_number_epodoc'

      # Generate data for world maps using d3plus/geo_map (JSON)
      p2n adhoc worldmap --expression='TA=lentille' --country-field='country'
      p2n adhoc worldmap --expression='TA=lentille' --country-field='applicants'
      p2n adhoc worldmap --expression='TA=lentille' --country-field='inventors'
      p2n adhoc worldmap --expression='TA=lentille' --country-field='register.designated_states' --with-register

      # Generate data suitable for PivotTable.js (JSON)
      p2n adhoc pivot --expression='TA=lentille' --with-family

