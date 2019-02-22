# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 07:57:19 2015

@author: dreymond

Draws the map of patent applicants' and inventors' origin countries for a universe.
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
            logger.info("Generating maps about applicants' and inventors' origin countries for {}. ".format(label))

            # Compute storage slot
            storage_name = prefix + configFile.ndf

            # Read data from storage, generate map and save JSON and HTML to filesystem
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
        logger.error('Could not read "{storage_name}" from storage path "{storage_path}".'.format(**locals()))
        sys.exit(1)

    # Status message
    logger.info("Mapping {count} patents. Excepting EP and WO.".format(count=len(result['brevets'])))

    # Compute map data
    mapdata_all = {
        'Applicant-Country': p2n.formatter.maps.d3plus_data_brevets(result['brevets'], 'Applicant-Country'),
        'Inventor-Country': p2n.formatter.maps.d3plus_data_brevets(result['brevets'], 'Inventor-Country'),
    }

    # Create output path
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    # Render maps
    for field, mapdata in mapdata_all.items():

        field_name = field.split('-')[0]

        jsonfile = '{storage_name}Map{field_name}.json'.format(**locals())
        htmlfile = '{storage_name}Carto{field_name}.html'.format(**locals())

        with open(os.path.join(output_path, jsonfile), "w") as mapdatafile:
            json.dump(mapdata, mapdatafile)

        RenderTemplate(
            "ModeleCartoDeposant.html",
            os.path.join(output_path, htmlfile),
            field=field_name,
            request=result["requete"],
            jsonFile=jsonfile,
        )


if __name__ == '__main__':
    run()
