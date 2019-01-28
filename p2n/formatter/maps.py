# -*- coding: utf-8 -*-
# (c) 2017 The Patent2Net Developers
import types
import logging
import operator
import pkg_resources
from p2n.util import memoize

logger = logging.getLogger(__name__)


def d3plus_data_brevets(document_list, field):
    """
    Compute data suitable for feeding to d3plus/geo_map from Patent2NetBrevet data model.

    Obtains a list of document dictionaries in the legacy Patent2Net brevet format and
    a field name designating which dictionary key to use for the country information,
    e.g. "country", "Applicant-Country" or "Inventor-Country".

    This code was taken from the "FormateExportAttractivityCartography.py" and
    "FormateExportCountryCartography.py" files.
    """

    NomPays, NomTopoJSON = read_name_country_map()

    cptPay = dict()
    for document in document_list:

        if document[field] == '': continue
        country = document[field]

        if isinstance(country, list):
            for country in country:
                if country in NomPays.keys(): # patent country in name (ouf)
                    if cptPay.has_key(NomPays[country]): # has it been found yet?
                        cptPay[NomPays[country]] += 1 # so add one
                    else: # set it instead to one
                        cptPay[NomPays[country]] = 1
                elif country == 'SU':
                    if cptPay.has_key('RU'): # has it been found yet?
                        cptPay[NomPays['RU']] += 1 # so add one
                    else: # set it instead to one
                        cptPay[NomPays['RU']] = 1
                else:
                    msg = 'Skipping country "{country}" for drawing on map, origin was "{label}".'.format(country=country, label=document['label'])
                    logger.info(msg)

        elif country in NomPays.keys(): #patent country in name (saved :-)
            if cptPay.has_key(NomPays[country]): #has it been found yet ?
                cptPay[NomPays[country]] += 1 #so add one
            else: #set it intead to one
                cptPay[NomPays[country]] = 1

        else:
            msg = 'Skipping country "{country}" for drawing on map, origin was "{label}".'.format(country=country, label=document['label'])
            logger.info(msg)

    mapdata = dict()
    for k in cptPay.keys():
        tempo = dict()
        tempo["value"] = cptPay[k]
        tempo["name"] = k
        tempo["country"] = NomTopoJSON[k]
        if "data" in mapdata.keys():
            mapdata["data"].append(tempo)
        else:
            mapdata["data"]=[tempo]

    return mapdata


def d3plus_data_documents(document_list, field):
    """
    Compute data suitable for feeding to d3plus/geo_map from OPSExchangeDocument data model.

    Obtains a list of document objects of type OPSExchangeDocument and
    a field name designating which object attribute to use for the country information,
    e.g. "country", "applicants", "inventors" or "register.designated_states".

    This also accounts for item uniqueness as e.g. you don't want to count the same inventors
    twice or more across family members. However, here is still room for improvement regarding
    full applicant- or inventor name disambiguation [TODO].

    It will also associate a list of multiple terms for each country to be able to e.g. display the
    list of associated inventors or applicants inside the per-country info box (d3plus/geo_map tooltip).
    """


    # Read world country utility mappings
    countrycode_map, topojson_map = read_name_country_map()


    # Aggregate list of unique items over designated country,
    # associated terms and whole list of documents.
    unique_items = []
    for document in document_list:

        # Get value from document attribute, even accepts dotted notation
        # to access nested structures like "register.designated_states".
        try:
            value = operator.attrgetter(field)(document)
        except AttributeError:
            continue

        # Skip empty values
        if not value: continue

        # For running with --country-field='country'
        if not isinstance(value, list):
            value = [{'country': value, 'name': document.publication_number_epodoc}]

        # For running with --country-field='applicants|inventors|register.designated_states'
        for item in value:

            # For running with --country-field='register.designated_states'
            if type(item) in types.StringTypes:
                item = {'country': item, 'name': document.publication_number_epodoc}

            # Skip duplicates
            if item in unique_items: continue

            # Aggregate items
            unique_items.append(item)

    # Debugging
    #print 'unique_items'; pprint(unique_items)


    # Compute intermediary format holding the count-per-country information
    # and a list of terms associated with the respective country.
    data = {}
    for item in unique_items:

        country_code = item['country']

        if country_code in countrycode_map:
            data.setdefault(country_code, {'count': 0, 'terms': []})
            data[country_code]['count'] += 1
            data[country_code]['terms'].append(item['name'])
        else:
            msg = 'Skipping country "{country}" for drawing on map, ' \
                  'origin was "{label}".'.format(country=country_code, label=item['name'])
            logger.info(msg)

    # Debugging
    #print 'data:', data


    # Compute data suitable for feeding to d3plus/geo_map.
    mapdata = []
    for country_code, entry in data.items():
        mapitem = dict()
        mapitem["country"] = topojson_map[country_code]
        mapitem["name"] = countrycode_map[country_code]
        mapitem["value"] = entry['count']
        mapitem["Terms"] = '<br/>'.join(entry['terms'])
        mapdata.append(mapitem)

    result = {
        'data': mapdata
    }

    return result


@memoize
def read_name_country_map(filename=None):
    """
    Read country codes and names into dictionaries
    for being able to map them against each other.

    ``countrycode_map`` maps short country codes to full country names and back,
    ``topojson_map`` maps short country codes and full country names to longer topojson country codes.
    """

    if not filename:
        filename = pkg_resources.resource_filename('p2n.resources', "NameCountryMap.csv")

    countrycode_map = dict()
    topojson_map = dict()

    with open(filename, 'r') as fic:

        for line in fic.readlines():

            # Read line
            row = line.decode('utf-8').strip().split(';')

            # Decode row
            longcode = row[0]
            longname = row[1]
            countrycode = row[2].upper()

            # Assign to mapping dictionaries while
            # using the same dict for reverse/additional mapping.

            countrycode_map[countrycode] = longname
            countrycode_map[longname] = countrycode

            topojson_map[countrycode] = longcode
            topojson_map[longname] = longcode

    return countrycode_map, topojson_map
