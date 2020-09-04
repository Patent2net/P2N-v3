# -*- coding: utf-8 -*-
# (c) 2017 The Patent2Net Developers
import re
import logging
import operator
from copy import deepcopy
from collections import OrderedDict
from jsonpointer import JsonPointer, JsonPointerException
from p2n.util import to_list

logger = logging.getLogger(__name__)


class OPSExchangeDocumentDecoder:
    """
    Functions for decoding data from raw JSON OPS exchange documents.
    """

    pointer_country = JsonPointer('/exchange-document/@country')
    pointer_docnumber = JsonPointer('/exchange-document/@doc-number')
    pointer_kind = JsonPointer('/exchange-document/@kind')
    pointer_family_id = JsonPointer('/exchange-document/@family-id')

    pointer_application_reference = JsonPointer('/exchange-document/bibliographic-data/application-reference/document-id')
    pointer_publication_reference = JsonPointer('/exchange-document/bibliographic-data/publication-reference/document-id')
    pointer_abstract = JsonPointer('/exchange-document/abstract')
    pointer_applicant = JsonPointer('/exchange-document/bibliographic-data/parties/applicants/applicant')
    pointer_inventor = JsonPointer('/exchange-document/bibliographic-data/parties/inventors/inventor')

    pointer_invention_title = JsonPointer('/exchange-document/bibliographic-data/invention-title')

    pointer_ipc = JsonPointer('/exchange-document/bibliographic-data/classification-ipc/text')
    pointer_ipcr = JsonPointer('/exchange-document/bibliographic-data/classifications-ipcr/classification-ipcr')
    pointer_classifications = JsonPointer('/exchange-document/bibliographic-data/patent-classifications/patent-classification')


    @classmethod
    def document_number_date(cls, docref, id_type):
        """
        Decode document number and filing/grant date from
        /exchange-document/bibliographic-data/{application|publication}-reference/document-id.
        """
        docref_list = to_list(docref)
        for document_id in docref_list:
            if document_id['@document-id-type'] == id_type:
                if id_type == 'epodoc':
                    doc_number = document_id['doc-number']['$']
                else:
                    doc_number = document_id['country']['$'] + document_id['doc-number']['$'] + document_id['kind']['$']
                date = document_id.get('date', {}).get('$')
                date = cls.decode_date(date)
                return doc_number, date
        return None, None

    @staticmethod
    def decode_date(date):
        date = date and '-'.join([date[:4], date[4:6], date[6:8]])
        return date

    @classmethod
    def titles(cls, data):
        """
        Decode titles in all languages.
        """

        try:
            titles = to_list(cls.pointer_invention_title.resolve(data))
        except JsonPointerException:
            return {}

        data = OrderedDict()
        for title in titles:
            language = title.get(u'@lang', u'ol')
            value = title[u'$'] or u''
            if value:
                data[language] = value
        return data

    @classmethod
    def abstracts(cls, data):
        """
        Decode abstracts in all languages.
        """

        try:
            abstracts = to_list(cls.pointer_abstract.resolve(data))
        except JsonPointerException:
            return {}

        data = OrderedDict()
        for abstract in abstracts:
            language = abstract.get(u'@lang', u'ol')

            lines = to_list(abstract['p'])
            lines = map(lambda line: line['$'], lines)
            value = '\n'.join(lines)

            if value:
                data[language] = value

        return data

    @classmethod
    def parties(cls, partylist, name):
        """
        Decode list of applicants or inventors.
        """
        #print 'partylist:', partylist
        parties = []
        for party in partylist:

            # Use only "epodoc" party members, as they contain the origin country
            if party['@data-format'] != 'epodoc':
                continue

            epodoc_name = party[name]['name']['$'].replace(u'\u2002', u' ')
            matches = re.match('(?P<name>.+?) \[(?P<country>.+?)\]', epodoc_name)
            if matches:
                parties.append(matches.groupdict())
            else:
                parties.append({'country': None, 'name': epodoc_name})

        return parties

    @classmethod
    def applicants(cls, data):
        try:
            nodes = to_list(cls.pointer_applicant.resolve(data))
        except JsonPointerException:
            return []
        return cls.parties(nodes, 'applicant-name')

    @classmethod
    def inventors(cls, data):
        try:
            nodes = to_list(cls.pointer_inventor.resolve(data))
        except JsonPointerException:
            return []
        return cls.parties(nodes, 'inventor-name')


    @classmethod
    def classifications_ipc(cls, data):

        try:
            entries = to_list(cls.pointer_ipc.resolve(data))
        except JsonPointerException:
            return []

        entries = map(lambda entry: entry['$'], entries)

        return entries


    @classmethod
    def classifications_ipcr(cls, data):

        try:
            entries = to_list(cls.pointer_ipcr.resolve(data))
        except JsonPointerException:
            return []

        entries = map(lambda entry: entry['text']['$'], entries)
        entries = map(lambda entry: entry[:15].replace(' ', ''), entries)

        return entries

    @classmethod
    def classifications_more(cls, data):

        try:
            nodes = to_list(cls.pointer_classifications.resolve(data))
        except JsonPointerException:
            return {}

        cpc_fieldnames = ['section', 'class', 'subclass', 'main-group', '/', 'subgroup'];

        classifications = {}
        for node in nodes:
            scheme = node['classification-scheme']['@scheme']

            classifications.setdefault(scheme, [])

            entry = None
            if scheme == 'CPC' or scheme == 'CPCNO':
                entry_parts = []
                for cpc_fieldname in cpc_fieldnames:
                    if cpc_fieldname == '/':
                        entry_parts.append('/')
                        continue
                    if node[cpc_fieldname]:
                        part = node[cpc_fieldname]['$']
                        entry_parts.append(part)
                    else:
                        logger.warning('Unknown CPC classification field "{cpc_fieldname}"'.format(**locals()))
                entry = ''.join(entry_parts)

            elif scheme == 'UC' or scheme == 'FI' or scheme == 'FTERM':
                # UC was sighted with US documents, FI and FTERM with JP documents
                entry = node['classification-symbol']['$']

            else:
                logger.warning('Unknown classification scheme "{scheme}"'.format(**locals()))

            if entry:
                classifications[scheme].append(entry)

        return classifications



class OPSRegisterDocumentDecoder:
    """
    Functions for decoding data from raw JSON OPS register documents.
    """

    # Biblio container
    pointer_bibliographic_data = JsonPointer('/reg:register-document/reg:bibliographic-data')

    # Discrete values
    pointer_status = JsonPointer('/reg:register-document/@status')
    pointer_filing_language = JsonPointer('/reg:register-document/reg:bibliographic-data/reg:language-of-filing/$')

    # Historic data
    pointer_publication_reference = JsonPointer('/reg:register-document/reg:bibliographic-data/reg:publication-reference')
    pointer_application_reference = JsonPointer('/reg:register-document/reg:bibliographic-data/reg:application-reference')
    pointer_designated_states = JsonPointer('/reg:register-document/reg:bibliographic-data/reg:designation-of-states')
    pointer_applicants = JsonPointer('/reg:register-document/reg:bibliographic-data/reg:parties/reg:applicants')
    pointer_inventors = JsonPointer('/reg:register-document/reg:bibliographic-data/reg:parties/reg:inventors')
    pointer_agents = JsonPointer('/reg:register-document/reg:bibliographic-data/reg:parties/reg:agents')
    pointer_term_of_grant = JsonPointer('/reg:register-document/reg:bibliographic-data/reg:term-of-grant')
    pointer_licensee_data = JsonPointer('/reg:register-document/reg:bibliographic-data/reg:licensee-data')

    pointer_related_documents = JsonPointer('/reg:register-document/reg:bibliographic-data/reg:related-documents/reg:division/reg:relation')
    pointer_bio_deposit = JsonPointer('/reg:register-document/reg:bibliographic-data/reg:bio-deposit')

    # Actions
    pointer_dates_rights_effective = JsonPointer('/reg:register-document/reg:bibliographic-data/reg:dates-rights-effective')
    pointer_opposition_data = JsonPointer('/reg:register-document/reg:bibliographic-data/reg:opposition-data')
    pointer_ep_patent_statuses = JsonPointer('/reg:register-document/reg:ep-patent-statuses/reg:ep-patent-status')

    """
    TODO:

    # EP14879896P
    u'reg:office-specific-bib-data':

    """

    @classmethod
    def status(cls, data):
        """
        Decode register status.
        """
        return cls.pointer_status.resolve(data)


    @classmethod
    def filing_language(cls, data):
        """
        Decode filing language.
        """
        return cls.pointer_filing_language.resolve(data)


    @classmethod
    def actions(cls, data):
        """
        Decode action information from different places
        scattered around the OPS Exchange Document:

        - dates-rights-effective
        - opposition-data
        - date-application-deemed-withdrawn
        - date-application-withdrawn-by-applicant
        - ep-patent-statuses
        """

        # Information from all actions
        actions = []


        """
        # ap=EP88402018
        u'reg:dates-rights-effective': {u'reg:first-examination-report-despatched': {u'reg:date': {u'$': u'19901213'}},
                                        u'reg:request-for-examination': {u'@change-gazette-num': u'1989/41',
                                                                         u'reg:date': {u'$': u'19890628'}}},
        """
        try:
            for name, item in cls.pointer_dates_rights_effective.resolve(data).items():
                entry = cls.decode_action('dates-rights-effective', name, item)
                actions.append(entry)
        except JsonPointerException:
            pass


        """
        # ap=EP86400204
        u'reg:opposition-data': {u'@change-date': u'19890321',
                                 u'@change-gazette-num': u'1989/19',
                                 u'reg:opposition-not-filed': {u'reg:date': {u'$': u'19890221'}}},
        """
        try:
            opposition_data = cls.pointer_opposition_data.resolve(data)

            # Transform entry into baseline format like "reg:dates-rights-effective"
            change_fields = ['@change-date', '@change-gazette-num']
            change_data = {}
            for change_field in change_fields:
                change_data[change_field] = opposition_data[change_field]
                del opposition_data[change_field]

            for name, item in opposition_data.items():
                for key, value in change_data.items():
                    item.setdefault(key, value)
                entry = cls.decode_action('opposition-data', name, item)
                actions.append(entry)

        except JsonPointerException:
            pass


        """
        # TA=lentille
        u'reg:date-application-deemed-withdrawn': {u'@change-gazette-num': u'2009/11',
                                                   u'reg:date': {u'$': u'20080909'}},

        # TA=lentille
        u'reg:date-application-withdrawn-by-applicant': {u'@change-gazette-num': u'2012/35'},
        """
        deemed_withdrawn_nodes = ['reg:date-application-deemed-withdrawn', 'reg:date-application-withdrawn-by-applicant']
        bibliographic_data = cls.pointer_bibliographic_data.resolve(data)
        for nodename in deemed_withdrawn_nodes:
            #print 'nodename:', nodename
            #print 'bibdate:', bibliographic_data
            if nodename in bibliographic_data:
                kind = 'withdrawn-dates'
                name = nodename.replace('reg:', '')
                item = bibliographic_data[nodename]
                entry = cls.decode_action(kind, name, item)
                actions.append(entry)

        """
        # EP2699357, id=EP12715599P
        u'reg:ep-patent-statuses': {u'reg:ep-patent-status': [{u'$': u'No opposition filed within time limit',
                                                               u'@change-date': u'20171208',
                                                               u'@status-code': u'7'},
                                                              {u'$': u'The patent has been granted',
                                                               u'@change-date': u'20161230',
                                                               u'@status-code': u'8'},
                                                              {u'$': u'Grant of patent is intended',
                                                               u'@change-date': u'20161223',
                                                               u'@status-code': u'12'}]}}}
        """
        ep_patent_statuses = to_list(cls.pointer_ep_patent_statuses.resolve(data))
        for item in ep_patent_statuses:
            entry = OrderedDict()
            entry['kind'] = 'status'
            entry['name'] = item['$']
            entry['date'] = entry['change_date'] = OPSExchangeDocumentDecoder.decode_date(item.get('@change-date'))
            entry['status_code'] = item.get('@status-code')

            # Skip some status changes without "date" information as these won't be sortable
            if entry['date']:
                actions.append(entry)


        # Sort all entries by date in ascending order
        actions = sorted(actions, key=operator.itemgetter('date'))

        return actions

    @staticmethod
    def decode_action(kind, name, item):
        entry = OrderedDict()
        entry['kind'] = kind
        entry['name'] = name.replace('reg:', '')
        entry['date'] = 'reg:date' in item and OPSExchangeDocumentDecoder.decode_date(item['reg:date']['$']) or None
        entry['change_date'] = OPSExchangeDocumentDecoder.decode_date(item.get('@change-date'))
        entry['change_gazette'] = item.get('@change-gazette-num')

        if not entry['date']:
            entry['date'] = entry['change_date']

        return entry

    @classmethod
    def application_reference(cls, data):
        """
        Decode publication reference from register document.
        """

        try:
            nodes = to_list(cls.pointer_application_reference.resolve(data))
        except JsonPointerException:
            return []

        history = cls.read_history(nodes, 'reg:document-id', cls.decode_document_reference)
        history = list(reversed(sorted(history, key=operator.itemgetter('change_date'))))

        return history

    @classmethod
    def publication_reference(cls, data):
        """
        Decode publication reference from register document.

        u'reg:publication-reference': [{u'@change-gazette-num': u'2014/30',
                                        u'reg:document-id': {u'@lang': u'de',
                                                             u'reg:country': {u'$': u'WO'},
                                                             u'reg:date': {u'$': u'20140724'},
                                                             u'reg:doc-number': {u'$': u'2014111240'},
                                                             u'reg:kind': {u'$': u'A1'}}},
                                       {u'@change-gazette-num': u'2015/48',
                                        u'reg:document-id': {u'@lang': u'de',
                                                             u'reg:country': {u'$': u'EP'},
                                                             u'reg:date': {u'$': u'20151125'},
                                                             u'reg:doc-number': {u'$': u'2946041'},
                                                             u'reg:kind': {u'$': u'A1'}}}],
        """

        try:
            nodes = to_list(cls.pointer_publication_reference.resolve(data))
        except JsonPointerException:
            return []

        history = cls.read_history(nodes, 'reg:document-id', cls.decode_document_reference)
        history = list(reversed(sorted(history, key=operator.itemgetter('change_date'))))

        return history

    @staticmethod
    def decode_document_reference(item):
        entry = OrderedDict()
        entry['date'] = 'reg:date' in item and OPSExchangeDocumentDecoder.decode_date(item['reg:date']['$']) or None
        entry['number'] = item['reg:country']['$'] + item['reg:doc-number']['$'] + item.get('reg:kind', {}).get('$', '')
        return entry

    @classmethod
    def designated_states(cls, data):
        """
        Decode designated states from register document.

        # TODO: Multiple designated states entries. e.g. EP16202765P
        """

        try:
            nodes = to_list(cls.pointer_designated_states.resolve(data))
        except JsonPointerException:
            return []

        return cls.read_history(nodes, 'reg:designation-pct', cls.countries_designated)

    @classmethod
    def countries_designated(cls, node):
        """
        Decode list of countries (designated states).
        """
        return cls.decode_countries(node, '/reg:regional/reg:country')

    @classmethod
    def applicants(cls, data):
        """
        Decode list of applicants
        """
        try:
            nodes = to_list(cls.pointer_applicants.resolve(data))
        except JsonPointerException:
            return []

        return cls.read_history(nodes, 'reg:applicant', cls.parties)

    @classmethod
    def inventors(cls, data):
        """
        Decode list of inventors
        """
        try:
            nodes = to_list(cls.pointer_inventors.resolve(data))
        except JsonPointerException:
            return []

        return cls.read_history(nodes, 'reg:inventor', cls.parties)

    @classmethod
    def agents(cls, data):
        """
        Decode list of agents
        """
        try:
            nodes = to_list(cls.pointer_agents.resolve(data))
        except JsonPointerException:
            return []

        return cls.read_history(nodes, 'reg:agent', cls.parties)

    @classmethod
    def countries_lapsed(cls, data):
        """
        Decode list of multiple "lapsed-in-country" entries

        # ap=EP08836401
        u'reg:term-of-grant': [{u'@change-date': u'20140718',
                                u'@change-gazette-num': u'2014/34',
                                u'reg:lapsed-in-country': [{u'reg:country': {u'$': u'HU'},
                                                            u'reg:date': {u'$': u'20080709'}},
                                                           {u'reg:country': {u'$': u'AT'},
                                                            u'reg:date': {u'$': u'20120418'}},
        """
        try:
            nodes = to_list(cls.pointer_term_of_grant.resolve(data))
        except JsonPointerException:
            return []

        return cls.read_history(nodes, 'reg:lapsed-in-country', cls.lapsed_in_country)

    @classmethod
    def lapsed_in_country(cls, node):
        """
        Decode list of "lapsed-in-country" entries.
        """

        entries = to_list(node)

        data = []
        for entry in entries:
            item = {
                'country': entry['reg:country']['$'],
                'date': OPSExchangeDocumentDecoder.decode_date(entry['reg:date']['$']),
            }
            data.append(item)

        return data

    @classmethod
    def parties(cls, node):
        """
        Decode list of applicants, inventors or agents.

        """
        entries = []
        for party in to_list(node):

            addressbook = party['reg:addressbook']

            # TODO: u'reg:nationality', u'reg:residence'

            entry = OrderedDict()
            entry['name'] = addressbook['reg:name']['$']
            entry['country'] = addressbook['reg:address']['reg:country']['$']
            address = []
            for index in range(1, 7):
                fieldname = 'address-{}'.format(index)
                fieldname_ops = 'reg:{}'.format(fieldname)
                try:
                    value = addressbook['reg:address'][fieldname_ops]['$']
                    address.append(value)
                except KeyError:
                    pass

            entry['address'] = address

            entries.append(entry)

        return entries


    @classmethod
    def read_history(cls, nodes, node_name, item_decoder):
        """
        Generically decode arbitrary lists based on the @change-date / @change-gazette-num scheme
        """

        # Collect entries over time
        history = []
        for node in nodes:
            entry = OrderedDict()
            entry['data'] = node_name in node and item_decoder(node[node_name]) or {}
            if '@change-date' in node:
                entry['change_date'] = OPSExchangeDocumentDecoder.decode_date(node['@change-date'])
            elif 'date' in entry['data']:
                entry['change_date'] = entry['data']['date']
            entry['change_gazette'] = node.get('@change-gazette-num', 'N/P')
            history.append(entry)

        # Deduplicate entries. Sometimes, duplicate entries are in the history list,
        # one with 'change_gazette' == 'N/P' and another one with a real value, e.g. '1986/34'.
        # We want to choose the entry with the real value and suppress to other one,
        # but only if all the bibliographic data are equal.
        deduplicated = []
        real = []
        for entry in history:
            entry_dup = deepcopy(entry)
            del entry_dup['change_gazette']

            if deduplicated:
                overwrite = (real[-1]['change_gazette'] == 'N/P' and real[-1]['change_date'] == entry['change_date']) and (deduplicated[-1] == entry_dup)
                if overwrite:
                    real.pop()
                    deduplicated.pop()

            if entry_dup not in deduplicated:
                deduplicated.append(entry_dup)
                real.append(entry)

        return real


    @classmethod
    def related_documents(cls, data):
        """
        u'reg:related-documents': {u'reg:division': {u'reg:relation':
            {u'reg:child-doc':
                {u'reg:document-id': {u'reg:country': {u'$': u''}, u'reg:doc-number': {u'$': u''}}},

            u'reg:parent-doc':
                {u'reg:document-id': [

                    {u'@document-id-type': u'application number',
                    u'reg:country': {u'$': u'EP'},
                    u'reg:doc-number': {u'$': u'20110776418'},
                    u'reg:kind': {u'$': u'D'}},

                    {u'@document-id-type': u'publication number',
                    u'reg:country': {u'$': u'EP'},
                    u'reg:doc-number': {u'$': u'20110776418'},
                    u'reg:kind': {u'$': u'D'}},
        """

        try:
            container = cls.pointer_related_documents.resolve(data)
        except JsonPointerException:
            return {}

        result = {}
        for relation, document in container.items():
            relation = relation.replace('reg:', '').replace('-doc', '')
            result.setdefault(relation, {})
            for document_id in to_list(document['reg:document-id']):
                if '@document-id-type' not in document_id:
                    continue
                key = document_id['@document-id-type'].replace(' number', '')
                doc_number = document_id['reg:country']['$'] + document_id['reg:doc-number']['$'] + document_id['reg:kind']['$']
                result[relation][key] = doc_number

        return result

    @classmethod
    def licensee_data(cls, data):
        """
        # EP2683490, id=EP12704680P
        u'reg:licensee-data': {u'@change-date': u'20141219',
                               u'@change-gazette-num': u'2015/04',
                               u'reg:licensee': {u'@designation': u'as-indicated',
                                                 u'@sequence': u'01',
                                                 u'@type-license': u'right-in-rem',
                                                 u'reg:date': {u'$': u'20141212'},
                                                 u'reg:effective-in': {u'reg:country': [{u'$': u'AL'},
                                                                                        {u'$': u'AT'},
                                                                                        {u'$': u'BE'},


        """
        try:
            nodes = to_list(cls.pointer_licensee_data.resolve(data))
        except JsonPointerException:
            return []

        return cls.read_history(nodes, 'reg:licensee', cls.licensee_item)

    @classmethod
    def licensee_item(cls, node):
        item = OrderedDict()
        item['sequence'] = node['@sequence']
        item['designation'] = node['@designation']
        item['type'] = node['@type-license']
        item['date'] = OPSExchangeDocumentDecoder.decode_date(node['reg:date']['$'])
        item['countries_effective'] = cls.countries_effective(node)
        return item

    @classmethod
    def countries_effective(cls, node):
        """
        Decode list of countries (designated states).
        """
        return cls.decode_countries(node, '/reg:effective-in/reg:country')

    @staticmethod
    def decode_countries(node, pointer):
        countries_pointer = JsonPointer(pointer)
        countries_raw = to_list(countries_pointer.resolve(node))
        countries = [country_raw['$'] for country_raw in countries_raw]
        return countries


    @classmethod
    def bio_deposit(cls, data):
        """
        # EP2699357, id=EP12715599P
        u'reg:bio-deposit': {u'@num': u'',
                             u'reg:bio-accno': {u'$': u''},
                             u'reg:depositary': {u'$': u''},
                             u'reg:dtext': {u'$': u'one or more deposits'}},

        """
        try:
            node = cls.pointer_bio_deposit.resolve(data)
        except JsonPointerException:
            return {}

        data = OrderedDict()
        data['text'] = node['reg:dtext']['$']
        data['depositary'] = node['reg:depositary']['$']
        data['accno'] = node['reg:bio-accno']['$']
        data['num'] = node['@num']
        return data
