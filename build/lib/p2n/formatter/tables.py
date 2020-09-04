# -*- coding: utf-8 -*-
# (c) 2017 The Patent2Net Developers
import logging
import operator
from p2n.util import filterdict, dictproduct, unique, object_to_dictionary

logger = logging.getLogger(__name__)


def pivottables_data_brevets(document_list):
    """
    Compute data suitable for feeding to PivotTable.js from Patent2NetBrevet data model.

    Obtains a list of document dictionaries in the legacy Patent2Net brevet format,
    filters each dictionary by designated keys and normalizes/flattens the dictionaries
    by expanding all entries containing multivalued attributes to all combinations
    of themselves with scalar values only (cartesian product).

    The reason for this is because PivotTable.js assumes all attributes to be
    scalar values (i.e. strings or numbers) and not objects, see also:
    https://github.com/nicolaskruchten/pivottable/wiki/Input-Formats

    This is an attempt of a clean-room reimplementation of the core of
    "FormateExportPivotTable.py" and "P2N_Lib.DecoupeOnTheFly".
    """

    fields = [
        'label', 'country', 'kind', 'year',
        #'priority-active-indicator',   # TODO
        #'prior-Date',                  # TODO
        'applicant', 'inventor', 'representative',
        'IPCR4', 'IPCR7',
        "Inventor-Country", "Applicant-Country",
        # Excluded due to excessive amount of entries after multivalue expansion
        #"CPC",
        #"equivalents",
    ]

    expanded_all = []
    for document in document_list:

        # Use only designated fields, skip others
        document = filterdict(document, fields)

        # Compute cartesian product to satisfy PivotTable.js
        expanded = dictproduct(document)

        # Add to list of expanded data
        expanded_all += expanded

    return expanded_all


def pivottables_data_documents(document_list):
    """
    Compute data suitable for feeding to PivotTable.js from OPSExchangeDocument data model.

    Obtains a list of document objects of type OPSExchangeDocument, simplifies its structure and
    filters each dictionary by designated keys and normalizes/flattens the dictionaries
    by expanding all entries containing multivalued attributes to all combinations
    of themselves with scalar values only (cartesian product).

    The reason for this is because PivotTable.js assumes all attributes to be
    scalar values (i.e. strings or numbers) and not objects, see also:
    https://github.com/nicolaskruchten/pivottable/wiki/Input-Formats

    This is an attempt of a clean-room reimplementation of the core of
    "FormateExportPivotTable.py" and "P2N_Lib.DecoupeOnTheFly"
    together with dynamic rule-based dictionary transformation
    to massage the data appropriately.
    """

    rules = [

        # Simple scalar fields not requiring any transformation
        'document_number',
        'country',
        'kind',
        'application_year',
        'publication_year',

        #'priority-active-indicator',   # TODO
        #'prior-Date',                  # TODO
        {
            'name': 'ipcr4',
            'getter': lambda document: document.classifications['IPCR'],
            'recipe': lambda items: unique([item[:4] for item in items]),
        },
        {
            'name': 'ipcr7',
            'getter': lambda document: document.classifications['IPCR'],
            'recipe': lambda items: unique([item.split('/')[0] for item in items]),
        },
        {
            'name': 'applicant',
            'getter': operator.attrgetter('applicants'),
            'recipe': lambda items: unique([item['name'] for item in items if item]),
        },
        {
            'name': 'inventor',
            'getter': operator.attrgetter('inventors'),
            'recipe': lambda items: unique([item['name'] for item in items if item]),
        },
        {
            'name': 'applicant_country',
            'getter': operator.attrgetter('applicants'),
            'recipe': lambda items: unique([item['country'] for item in items if item]),
        },
        {
            'name': 'inventor_country',
            'getter': operator.attrgetter('inventors'),
            'recipe': lambda items: unique([item['country'] for item in items if item]),
        },
        {
            'name': 'designated_state',
            'getter': lambda document: document.register and document.register.designated_states,
        },

        # Excluded due to excessive amount of entries after multivalue expansion
        #"CPC",
        #"equivalents",
    ]

    expanded_all = []
    for document in document_list:

        # Use only designated fields, skip others
        document = object_to_dictionary(document, rules)

        # Compute cartesian product to satisfy PivotTable.js
        expanded = dictproduct(document)

        # Add to list of expanded data
        expanded_all += expanded

    return expanded_all
