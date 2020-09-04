# -*- coding: utf-8 -*-
# (c) 2017 The Patent2Net Developers
import logging
import p2n.ops.client
import p2n.formatter.maps
import p2n.formatter.tables
from p2n.model import Patent2NetBrevet
from p2n.ops.client import OPSClient
from p2n.ops.model import OPSBiblioSearchResponse, OPSFamilyResponse, OPSRegisterResponse
from p2n.util import exception_traceback

logger = logging.getLogger(__name__)


class Patent2Net:

    def __init__(self, ops_key, ops_secret):
        self.ops_key = ops_key
        self.ops_secret = ops_secret

        self.ops_client = OPSClient(self.ops_key, self.ops_secret)

        self.response_data = None
        self.documents = []
        self.brevets = []

    def gather(self, expression, with_family=False, with_register=False):
        """
        Submit search expression to OPS published search and
        read response to acquire bibliographic data for each hit.

        Optionally, this will acquire family information for each result document and expand
        the list of documents by all respective family member documents.

        Also optionally, it will acquire register information for each result document.

        Finally, it will convert the list of result documents in ``self.documents``
        into a list of dictionaries in legacy Patent2Net Brevet format in ``self.brevets``.
        """

        # Submit search expression
        self.response_data = self.ops_client.crawl(expression)

        # Debugging
        #print(json.dumps(data))

        # Decode response
        response = OPSBiblioSearchResponse(self.response_data)

        # A list of ``OPSExchangeDocument`` object instances
        self.documents = response.results

        # Optionally, expand document list with each documents' family members
        if with_family:
            self.expand_family()

        # Optionally, enrich each document with register information
        if with_register:
            self.enrich_register()

        # Finally, provide a list of dictionaries in legacy Patent2Net Brevet format
        self.documents_to_brevets()

        return self

    def expand_family(self):
        """
        Acquire family information for each document in ``self.documents`` and expand the
        very same list by ``OPSExchangeDocument`` instances of the respective family members.
        """

        # We are doing bookkeeping using the document's publication number.
        # Uniqueness checks are performed on this list of publication numbers.
        document_numbers = []

        # The full list of documents including their family members
        documents_expanded = []

        # Iterate all result documents
        for ops_exchange_document in self.documents:

            # Use publication number without kindcode as key for uniqueness constraint
            document_number = ops_exchange_document.publication_number_epodoc

            # Start bookkeeping with the root document
            document_numbers.append(document_number)
            documents_expanded.append(ops_exchange_document)

            # Request family information for root document
            data = self.ops_client.family(document_number)
            response = OPSFamilyResponse(data)

            # Iterate all family members of the root document
            # and add them to the list of expanded documents
            family_numbers = []
            for family_member in response.results:

                # Read publication number of family member without kindcode
                family_member_number = family_member.publication_number_epodoc

                # Skip family members which are the same as the document itself
                if family_member_number == document_number:
                    continue

                # Skip duplicates. Currently uses first-come, first-serve policy.
                if family_member_number in document_numbers:
                    continue

                # Record number and document of family member
                family_numbers.append(family_member_number)
                document_numbers.append(family_member_number)
                documents_expanded.append(family_member)

            #logger.info('Family members: {}'.format(family_numbers))

        # Switch the current list of result documents over to the list
        # of documents expanded by their respective family members
        self.documents = documents_expanded

    def enrich_register(self):
        """
        Acquire register information for each ``OPSExchangeDocument``
        object instance in ``self.documents``.

        It will enrich the ``OPSExchangeDocument`` instance by adding
        the attribute ``register``, which is a reference to an instance
        of ``OPSRegisterDocument``.
        """

        # Iterate all result documents
        for document in self.documents:
            document_number = document.publication_number_epodoc

            # Fetch register information from OPS
            data = self.ops_client.register(document_number)

            if not data:
                logger.debug('No register information for document "{}"'.format(document_number))
                continue

            try:

                # Read register information response
                response = OPSRegisterResponse(data)
                if response.results:

                    # TODO: Is there more than one register document sometimes?
                    register_document = response.results[0]

                    # Propagate register information into OPSExchangeDocument object
                    document.register = register_document

            except Exception as ex:
                logger.warning('Could not decode register information for document "{}": {}\n{}'.format(document_number, ex, exception_traceback()))

    def documents_to_brevets(self):
        """
        Convert list of OPSExchangeDocument objects to list
        of dictionaries in legacy Patent2Net Brevet format.
        This can be used to feed the data into the classic P2N scripts.
        """

        self.brevets = []
        for ops_exchange_document in self.documents:

            # Create model instance of Patent2NetBrevet from OPSExchangeDocument
            brevet = Patent2NetBrevet.from_ops_exchange_document(ops_exchange_document)

            # Convert to dictionary in native P2N format
            p2n_brevet = brevet.as_dict()

            # Append to list of results
            self.brevets.append(p2n_brevet)

    def worldmap(self, country_field):
        """
        Generate data suitable for feeding into d3plus/geo_map.
        """

        # Generate map data

        # FIXME: For "Applicant-Country" and "Inventor-Country",
        # this should actually count the number of unique items (name/country).
        # Currently, it just counts *all* countries, so the deviation is even greater
        # when running with "--with-family" as a larger number of duplicate entries
        # will get counted more often.
        #mapdata = p2n.formatter.maps.d3plus_data_brevets(self.brevets, country_field)

        # DONE: Now operates on the native OPS data model and
        # properly aggregates unique applicant/inventor names.
        mapdata = p2n.formatter.maps.d3plus_data_documents(self.documents, country_field)

        return mapdata

    def pivot(self, format='ops'):
        """
        Generate data suitable for feeding into PivotTable.js, either from
        Patent2NetBrevet or from OPSExchangeDocument data model.
        """

        if format == 'ops':
            pivotdata = p2n.formatter.tables.pivottables_data_documents(self.documents)

        elif format == 'brevet':
            pivotdata = p2n.formatter.tables.pivottables_data_brevets(self.brevets)

        else:
            raise ValueError('Unknown format for pivot data "{}"'.format(format))

        return pivotdata
