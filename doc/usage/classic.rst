############
Classic mode
############

.. contents::
   :local:
   :depth: 1

----


*******************
Request description
*******************
Patent2Net needs a ``requete.cql`` file for operating in classic mode.
It acts as a request description and contains various parameters you might want to have a look at.

The most important ones are the CQL query to be submitted to OPS and the output directory where
data is stored.

Example::

    # CQL query expression
    request: ta="filter*" and ta="drink* water" AND (pn = U not (pn = UA or pn = US or pn = UY))

    # Output directory
    DataDirectory: Water

You can find some blueprints in the ``/RequestsSets`` directory.


****************
Legacy interface
****************

Run suite of scripts
====================
Use the ``/Patent2Net/ProcessPy.bat`` or the ``/Patent2Net/Process.sh`` file and enjoy!


****************
Modern interface
****************
The modern interface allows to specify a ``requete.cql`` file on the command line
or by using the environment variable ``P2N_CONFIG``.


Acquire data from OPS
=====================
Run Patent2Net::

    p2n acquire --config=/path/to/RequestsSets/Lentille.cql

Alternatively, you can specify the path to the ``requete.cql`` using an environment variable::

    export P2N_CONFIG=`pwd`/RequestsSets/Lentille.cql

then, just run::

    # Acquire patent information from OPS
    p2n acquire

    # Also acquire family information for each hit
    p2n acquire --with-family


Analyze information
===================
When running the analysis commands like this, you should set
the ``P2N_CONFIG`` environment variable for convenience, like described above.

E.g., run::

    # Build all world maps
    p2n maps

    # Build all network graphs
    p2n networks

    # p2n {maps,networks,tables,bibfile,iramuteq,freeplane,carrot}
    # see full list below or run ``p2n --help``


----


********
Synopsis
********


Output of "``p2n --help``"
==========================
::

    $ p2n --help

    ------------
    Classic mode
    ------------
      p2n ops init                          Initialize Patent2Net with OPS OAuth credentials
      p2n run                               Run data acquisition and all formatters
      p2n acquire                           Run document acquisition
        --with-family                       Also run family data acquisition with "p2n acquire"
      p2n maps                              Build maps of country coverage of patents, as well as applicants and inventors
      p2n networks                          Build various artefacts for data exploration based on network graphs
      p2n tables                            Export various artefacts for tabular data exploration
      p2n bibfile                           Export data in bibfile format
      p2n iramuteq                          Fetch more data and export it to suitable format for using in Iramuteq
      p2n freeplane                         Build mind map for Freeplane
      p2n carrot                            Export data to XML suitable for using in Carrot
      p2n images                            Fetch images and build thumbnails
      p2n interface                         Build main Patent2Net html interface

    Options:
      --config=<config>                     Path to requete.cql. Will fall back to environment variable "P2N_CONFIG".

    Examples:

      # Initialize Patent2Net with OPS OAuth credentials
      p2n ops init --key=ScirfedyifJiashwOckNoupNecpainLo --secret=degTefyekDevgew1

      # Run query and gather data
      p2n acquire --config=/path/to/RequestsSets/Lentille.cql --with-family

      # Build all world maps
      export P2N_CONFIG=/path/to/RequestsSets/Lentille.cql
      p2n maps

      # Run data acquisition and all targets
      p2n run

