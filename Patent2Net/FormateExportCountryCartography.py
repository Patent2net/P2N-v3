# -*- coding: utf-8 -*-
"""
Created on Thu Feb 05 16:27:36 2015

@author: dreymond

Draws the map of patent issuing countries for a universe.
Next version should consider EP and WO patents.
"""
import os
import sys
import json
import shutil
import logging
import p2n.storage
import p2n.formatter.maps
from p2n.config import label_from_prefix
from p2n.util import boot_logging
from P2N_Config import LoadConfig
from P2N_Lib import RenderTemplate

logger_name = os.path.basename(__file__).replace('FormateExport', '').replace('.py', '')
logger = logging.getLogger(logger_name)


def run():

    # Bootstrap logging
    boot_logging()

    # Load configuration
    configFile = LoadConfig()

    # Run this step only if enabled
    if configFile.FormateExportCountryCartography:

        # Get some paths from configuration
        storage_path = configFile.ResultBiblioPath
        output_path = configFile.ResultPath

        # Compute prefixes
        prefixes = [""]
        if configFile.GatherFamilly:
            prefixes.append("Families")

        # Build maps for all prefixes
        for prefix in prefixes:

            # Status message
            label = label_from_prefix(prefix)
            logger.info("Generating maps about patent issuing countries for {}. ".format(label))

            # Compute storage slot
            storage_name = prefix + configFile.ndf

            # Generate map
            generate_map(storage_path, storage_name, output_path)


        # Due to limit of D3, countries resources are necessary placed
        # in same working directory... other solution is to start an http server
        # http://stackoverflow.com/questions/17077931/d3-samples-in-a-microsoft-stack

        # Clone required resources into result directory
        shutil.copy('countries.json', os.path.join(output_path, "countries.json"))


def generate_map(storage_path, storage_name, output_path):

    # Read patent data from storage
    result = p2n.storage.read(storage_path, storage_name)
    if not result:
        logger.error('Could not read storage "{}"'.format(storage_name))
        sys.exit(1)

    # List value in countries, avoiding
    for bre in result['brevets']:
        if isinstance(bre['country'], list) and len(bre['country']) == 1:
            # Well, taking the first one, this is an approximation
            bre['country'] = bre['country'][0]

    # Status message
    logger.info("Mapping {count} patents. Excepting EP and WO.".format(count=len(result['brevets'])))

    # Compute map data
    mapdata = p2n.formatter.maps.d3plus_data_brevets(result['brevets'], 'country')

    # Render map
    jsonfile = '{storage_name}CountryMap.json'.format(**locals())
    htmlfile = '{storage_name}Carto.html'.format(**locals())

    with open(os.path.join(output_path, jsonfile), "w") as mapdatafile:
        json.dump(mapdata, mapdatafile)

    RenderTemplate(
        "ModeleCarto.html",
        os.path.join(output_path, htmlfile),
        request=result["requete"],
        jsonFile=jsonfile,
    )


if __name__ == '__main__':
    run()
