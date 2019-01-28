# -*- coding: utf-8 -*-
# (c) 2017 The Patent2Net Developers
import logging
import requests
import epo_ops
from epo_ops.models import Epodoc
from p2n.ops.model import OPSBiblioSearchResponse

logger = logging.getLogger(__name__)


class OPSClient:

    def __init__(self, api_key, api_secret):

        self.api_key = api_key
        self.api_secret = api_secret

        # Sanity checks
        if not self.api_key or not self.api_secret:
            message = 'OPSClient needs OAuth credentials for accessing the OPS API'
            logger.error(message)
            raise ValueError(message)

        # Create OPS client instance
        middlewares = [
            epo_ops.middlewares.Dogpile(),
            epo_ops.middlewares.Throttler(),
        ]
        self.client = epo_ops.Client(
            self.api_key, self.api_secret,
            accept_type='json', middlewares=middlewares)

    def search(self, expression, offset=0, limit=100):
        """
        Run data search and request bibliographic data for all results in given range.
        Obtains CQL expression, offset and limit parameters.
        Returns decoded data structure from JSON response.
        """

        range_begin = offset + 1
        range_end = offset + limit

        logger.info('Searching with expression "{expression}". offset={offset}, limit={limit}'.format(**locals()))
        try:
            response = self.client.published_data_search(
                expression, range_begin=range_begin, range_end=range_end, constituents=['biblio'])
        except requests.exceptions.HTTPError as ex:
            logger.error('OPS request error "{}". The response is:\n{}'.format(ex, ex.response.content))
            raise SearchError(ex)

        data = response.json()
        return data

    def crawl(self, expression, chunksize=100):
        """
        Run data search and request bibliographic data for
        all results by issuing multiple requests to OPS.
        Obtains CQL expression and chunksize parameters.
        Returns decoded data structure from JSON response.
        """

        # Fetch first chunk (1-100) from upstream
        data = self.search(expression, offset=0, limit=chunksize)

        # We will use a OPSBiblioSearchResponse for aggregating results across multiple requests.
        # Let's start with the data received from the very first request (chunk #1).
        biblio_response = OPSBiblioSearchResponse(data)

        # Extract total count of results
        total_count = biblio_response.total_result_count
        logger.info('Result count: %s', total_count)

        # The first 2000 hits are accessible from OPS
        if total_count > 2000:
            logger.warn('The OPS interface will only return the first 2000 hits')
        total_count = min(total_count, 2000)

        # Let's start where the very first request left off
        offset_second_chunk = chunksize

        # Request more results with {chunksize} documents each
        for offset in range(offset_second_chunk, total_count, chunksize):

            # Request next chunk
            chunk = self.search(expression, offset=offset, limit=chunksize)

            # Merge chunk into main list of results
            biblio_response.merge_results(chunk)

        return biblio_response.data

    def family(self, document_number):
        """
        Request family information for single document with number in epodoc format.
        """
        logger.info('Requesting family information for document "{}"'.format(document_number))
        response = self.client.family('publication', Epodoc(document_number), 'biblio')
        data = response.json()
        return data

    def register(self, document_number):
        """
        Request register information for single document with number in epodoc format.
        """
        logger.info('Requesting register information for document "{}"'.format(document_number))
        try:
            response = self.client.register('publication', Epodoc(document_number))
        except requests.HTTPError as ex:
            response = ex.response

        try:
            data = response.json()
        except ValueError:
            data = None

        return data


class SearchError(Exception):
    pass
