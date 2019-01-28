# -*- coding: utf-8 -*-
# (c) 2017 The Patent2Net Developers
import os
import sys
import json
import docopt
import logging
import operator
from p2n import __version__
from p2n.api import Patent2Net
from p2n.config import OPSCredentials
from p2n.util import boot_logging, normalize_docopt_options, run_script, JsonObjectEncoder

logger = logging.getLogger(__name__)

APP_NAME = 'Patent2Net'


def run():
    """
    Usage:
      p2n ops init --key=<ops-oauth-key> --secret=<ops-oauth-secret>
      p2n run [--config=requete.cql] [--with-family]
      p2n acquire [--config=requete.cql] [--with-family]
      p2n maps [--config=requete.cql]
      p2n networks [--config=requete.cql]
      p2n tables [--config=requete.cql]
      p2n bibfile [--config=requete.cql]
      p2n iramuteq [--config=requete.cql]
      p2n freeplane [--config=requete.cql]
      p2n carrot [--config=requete.cql]
      p2n images [--config=requete.cql]
      p2n interface [--config=requete.cql]
      p2n adhoc search --expression=<expression>
      p2n adhoc dump --expression=<expression> [--format=<format>] [--with-family] [--with-register]
      p2n adhoc list --expression=<expression> [--with-family] [--field=<field>] [--with-register]
      p2n adhoc worldmap --expression=<expression> --country-field=<country-field> [--with-family] [--with-register]
      p2n adhoc pivot --expression=<expression> [--format=<format>] [--with-family] [--with-register]
      p2n --version
      p2n (-h | --help)


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

    """

    # Use generic commandline options schema and amend with current program name
    commandline_schema = (run.__doc__).format(program=APP_NAME)

    # Read commandline options
    options = docopt.docopt(commandline_schema, version=APP_NAME + ' ' + __version__)

    # Start logging subsystem
    boot_logging(options)

    # Clean option names
    options = normalize_docopt_options(options)


    # Debugging
    #print('Options:\n{}'.format(pformat(options)))


    # Patent2Net ad-hoc mode interface
    if options['adhoc']:
        adhoc_interface(options)

    # Patent2Net classic interface
    else:
        classic_interface(options)


def adhoc_interface(options):
    """
    Patent2Net ad-hoc mode interface
    """

    # Read OPS credentials from designated file
    credentials = OPSCredentials(credentials_file='cles-epo.txt')
    key, secret = credentials.read()

    # Create Patent2Net instance
    patent2net = Patent2Net(key, secret)

    # Gather data
    results = patent2net.gather(
        options['expression'],
        with_family=options['with-family'],
        with_register=options['with-register'])

    # Display search results for given query expression in raw OPS format (JSON), e.g. run::
    # p2n adhoc search --expression='TA=lentille'
    if options['search']:
        payload = patent2net.response_data
        print(json.dumps(payload, cls=JsonObjectEncoder))

    # Display full results for given query expression in OpsExchangeDocument or Patent2NetBrevet format (JSON), e.g. run::
    # p2n adhoc dump --expression='TA=lentille'
    if options['dump']:
        if options['format'] == 'ops':
            payload = [result.as_dict() for result in results.documents]
        elif options['format'] == 'brevet':
            payload = results.brevets
        else:
            logger.error('Unknown format "{}" for dumping.'.format(options['format']))
            sys.exit(1)

        print(json.dumps(payload, cls=JsonObjectEncoder))

    # Display list of values from single field for given query expression, e.g. run::
    # p2n adhoc list --expression='TA=lentille'
    if options['list']:
        documents = results.documents
        output = []
        for document in documents:
            try:
                values = [operator.attrgetter(options['field'])(document)]
                output += values
            except AttributeError:
                pass
        print(json.dumps(output, indent=4))

    # Generate world map over given field, e.g. run::
    # p2n adhoc worldmap --expression='TA=lentille' --country-field='applicants'
    if options['worldmap']:
        mapdata = results.worldmap(options['country-field'])
        print(json.dumps(mapdata))

    # Generate data for PivotTable.js
    if options['pivot']:
        mapdata = results.pivot(options['format'])
        print(json.dumps(mapdata))

def classic_interface(options):
    """
    Patent2Net classic interface
    """

    # Convenience: Write OPS API credentials to file "cles-epo.txt"
    if options['ops'] and options['init']:
        if options['key'] and options['secret']:
            credentials = OPSCredentials()
            credentials.write(options['key'], options['secret'])
        sys.exit()


    # All tasks from here require a configuration file.
    configfile = options['config']
    if not configfile:
        configfile = os.environ.get('P2N_CONFIG')

    if not configfile:
        logger.error('No configuration file given. Either use --config commandline argument or P2N_CONFIG environment variable.')
        sys.exit(1)


    # Patent2Net classic steps, aggregated

    if options['acquire'] or options['run']:
        run_script('OPSGatherPatentsv2.py', configfile)
        if options['with-family']:
            run_script('OPSGatherAugment-Families.py', configfile)

    if options['maps'] or options['run']:
        run_script('FormateExportCountryCartography.py', configfile)
        run_script('FormateExportAttractivityCartography.py', configfile)

    if options['bibfile'] or options['run']:
        run_script('FormateExportBiblio.py', configfile)

    if options['tables'] or options['run']:
        run_script('FormateExportDataTableFamilies.py', configfile)
        run_script('FormateExportDataTable.py', configfile)
        run_script('FormateExportPivotTable.py', configfile)

    if options['networks'] or options['run']:

        networks = [
            "CountryCrossTech",
            "CrossTech",
            "InventorsCrossTech",
            "Applicants_CrossTech",
            "Inventors",
            "ApplicantInventor",
            "Applicants",
            "References",
            "Citations",
            "Equivalents",
        ]

        for network in networks:
            run_script('P2N-PreNetworks.py {network}'.format(network=network), configfile)
            run_script('P2N-Networks.py {network}'.format(network=network), configfile)
            run_script('P2N-NetworksJS.py {network}'.format(network=network), configfile)

    if options['freeplane'] or options['run']:
        run_script('P2N-FreePlane.py', configfile)

    if options['carrot'] or options['run']:
        run_script('FusionCarrot2.py', configfile)

    if options['interface'] or options['run']:
        run_script('Interface2.py', configfile)

    if options['iramuteq'] or options['run']:
        run_script('OPSGatherContentsV2-Iramuteq.py', configfile)
        run_script('FusionIramuteq2.py', configfile)

    if options['images'] or options['run']:
        run_script('OPSGatherContentsV2-Images.py', configfile)
        run_script('FusionImages.py', configfile)
