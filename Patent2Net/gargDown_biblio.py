#!/usr/bin/env python
"""
   Gargantext Software Copyright (c) 2016-2017 CNRS ISC-PIF -
http://iscpif.fr
    Licence (see :
http://gitlab.iscpif.fr/humanities/gargantext/blob/stable/LICENSE )
    - In France : a CECILL variant affero compliant
    - GNU aGPLV3 for all other countries
"""

import os
#import django

#from gargantext.constants import QUERY_SIZE_N_MAX, get_resource, get_resource_by_name
from gargDown.constants import *
from gargDown.util.parsers import *
from collections import defaultdict, Counter
from re          import sub
#from gargantext.util.languages import languages, detect_lang
import codecs
from gargDown.util.crawlers.HAL import HalCrawler
#from gargantext.models import (Node, ProjectNode, DocumentNode,
#                               Ngram, NodeNgram, NodeNgramNgram, NodeNodeNgram)
#from gargantext.util.db import session, get_engine, func, aliased, case
from collections import Counter
import importlib
#from django.http import Http404

# Import those to be available by notebook user
from langdetect import detect as detect_lang
#from gargantext.models import UserNode, User
import functools

class NotebookError(Exception):
    pass


def documents(corpus_id):
    pass
#    return (session.query(DocumentNode).filter_by(parent_id=corpus_id)
#                  #.order_by(Node.hyperdata['publication_date'])
#                   .all())


#import seaborn as sns
import pandas as pd

def parse2(corpus):
    document = list()
    try:
        print("PARSING")
        # print("DETECT_LANG?", DETECT_LANG)
        #1 corpus => 1 or multi resources.path (for crawlers)

        if len(corpus) == 0:
            return
        #all the resources are of the same type for now
        src = corpus['ressources'] 
        #get the sources capabilities for a given corpus resource
        #load the corresponding parserbot
        if src["parser"] is None:
            #corpus.status(error)
            raise ValueError("Resource '%s' has no Parser" %resources["name"])
        parserbot = load_parser(src)

        # print(parserbot)
#
#        #observed languages in default languages
#        observed_languages = []
#        #skipped_languages
#        skipped_languages = []
#        #skipped docs to remember for later processing
#        pending_add_error_stats = False
        skipped_docs = []

        documents_count = 0
        #BY RESOURCE
        Stop = False
        for i,resource in enumerate(corpus['path']):
            if Stop is True:
                continue
            else:
                # BY documents (cf. _Parser.__iter__)
                for hyperdata in parserbot(resource[1]):
                    # indexed text fields defined in CONSTANTS
                    for k in DEFAULT_INDEX_FIELDS:
                        if k in hyperdata.keys():
                            try:
                                hyperdata[k] = normalize_chars(hyperdata[k])
                            except Exception as error :
                                hyperdata["error"] = "Error normalize_chars"

                    # adding lang into record hyperdata JUST if not declared
#                    lang_infos = add_lang(hyperdata, observed_languages, skipped_languages)
#
#                    # update document
#                    if lang_infos['doc_error']:
#                        hyperdata['warning'] = lang_infos['doc_error']
#
#                    if lang_infos['doc_prediction']:
#                        prediction = lang_infos['doc_prediction']
#                        hyperdata['language_iso2'] = prediction[0]
#                        hyperdata['language_iso3'] = prediction[1]
#                        hyperdata['language_name'] = prediction[2]
#                        del prediction

                    # update stats
#                    observed_languages = lang_infos['observed']
#                    skipped_languages = lang_infos['skipped']
#
#                    del lang_infos

                    # init statuses
                    hyperdata['statuses'] = []

                    # only parsing errors can be written straight to doc statuses
                    # because it's a new hyperdata for the DB
                    if "error" in hyperdata.keys():
                        hyperdata['statuses'].append({
                            'action':'Parsing',
                            'error': hyperdata['error']
                            })
#                        pending_add_error_stats = True

                    # -----------------------
                    # save as set
                    # -----------------------
                    document.append( #(type, name, hyperdata)
#                        'DOCUMENT',
#                        hyperdata.get('title', '')[:255],
                        hyperdata
                    )
#                    session.add(document)
                    documents_count += 1
#
#                    if pending_add_error_stats:
#                        #adding skipped_docs for later processing if error in parsing
#                        skipped_docs.append(document.id)
#                        pending_add_error_stats = False

                    #BATCH_PARSING_SIZE
#                    if documents_count % BATCH_PARSING_SIZE == 0:
#                        corpus.status('Docs', progress=documents_count)
#                        corpus.save_hyperdata()
#                        session.add(corpus)
#                        session.commit()
#
#                # Commit any pending document
#                session.commit()

                # update info about the resource
#                resource['extracted'] = True
                #print( "resource n°",i, ":", d, "docs inside this file")

        # mark *corpus-level* status as complete !
#        corpus.status('Docs', progress=documents_count+1, complete=True)
#        corpus.save_hyperdata()

        # end of parsing

        #STORING AGREGATIONS INFO (STATS)

        # skipped_docs (ie docs to be skipped in next steps)
        print(len(skipped_docs), "docs skipped")
#        corpus.hyperdata["skipped_docs"] = list(skipped_docs)
#        corpus.save_hyperdata()

        # documents info
#        docs = corpus.children("DOCUMENT").count()
        docs = len(document)
        if docs == 0:
            print("[ERROR] PARSING FAILED!!!!!")
            corpus.status('Docs', error= "No documents parsed")
        print(docs, "parsed")
        
        # language stats
        #les langues pas belles
#        skipped_langs = dict(Counter(skipped_languages))      # idem
#        #les jolis iso2
#        observed_langs = dict(Counter(observed_languages))
#
#        # print("#LANGAGES OK")
#        # print(observed_langs)
#        # print("#LANGUAGES UNKNOWN")
#        # print(skipped_langs)
#
#        top_langs = sorted(observed_langs.items(), key = lambda x: x[1], reverse=True)
#        if len(top_langs) > 0:
#            corpus.hyperdata["language_id"] = top_langs[0][0]
#        else:
#            corpus.hyperdata["language_id"] = "__unknown__"
#        print("#MAIN language of the CORPUS", corpus.hyperdata["language_id"])
#
#        corpus.hyperdata["languages"] = observed_langs
#        corpus.hyperdata["languages"]["__unknown__"] = list(skipped_langs.keys())
#        corpus.save_hyperdata()

        print ('Saving data parsed')
        with codecs.open (corpus['fileName']+'.txt', 'w', 'utf8') as ficRes:
            for doc in document:
                for k in doc.keys():# PEut être ne garder que DEFAULT_INDEX_FIELDS
                    ficRes.write(k + ' --> \n')
                    if isinstance(doc[k], str):    
                        ficRes.write(doc[k] + '\n')
                    else:
                        ficRes.write(str(doc[k]) + '\n')
    except Exception as error:
#        corpus.status('Docs', error=error)
#        corpus.save_hyperdata()
        raise error


def scan_hal(request):
    from gargDown.util.crawlers.HAL import HalCrawler
    hal = HalCrawler()
    return hal.scan_results(request)


def newCorpus(rep, source, name=None, query=None):
    error = False

    if name is None:
        name = query

    if not isinstance(rep, str):
        error = "a valid project directory"
    if not isinstance(source, int) and not isinstance(source, str):
        error = "a valid source identifier: id or name"
    elif not isinstance(query, str):
        error = "a valid query"
    elif not isinstance(name, str):
        error = "a valid name"

    if error:
        raise NotebookError("Please provide %s." % error)

    resource = get_resource(source) if isinstance(source, int) else \
               get_resource_by_name(source)

    moissonneur_name = get_moissonneur_name(resource) if resource else \
                       source.lower()

    try:
        moissonneur = get_moissonneur(moissonneur_name)
    except ImportError:
        raise NotebookError("Invalid source identifier: %r" % source)
    print(query)
    return run_moissonneur(moissonneur, rep, name, query)


def get_moissonneur_name(ident):
    """ Return moissonneur module name from RESOURCETYPE or crawler name """

    # Does it quacks like a RESOURCETYPE ?
    if hasattr(ident, 'get'):
        ident = ident.get('crawler')

    # Extract name from crawler class name, otherwise assume ident is already
    # a moissonneur name.
    if isinstance(ident, str) and ident.endswith('Crawler'):
        return ident[:-len('Crawler')].lower()


def get_moissonneur(name):
    """ Return moissonneur module from its name """
    if not isinstance(name, str) or not name.islower():
        raise NotebookError("Invalid moissonneur name: %r" % name)

    module = importlib.import_module('gargDown.moissonneurs.%s' % name)
    module.name = name

    return module


def run_moissonneur(moissonneur, rep, name, query):
    """ Run moissonneur and return resulting corpus """

    # XXX Uber-kludge with gory details. Spaghetti rulezzzzz!
    class Dummy(object):
        pass

    request = Dummy()
    request.method = 'POST'
    request.path = 'nowhere'
    request.META = {}
    # XXX 'string' only have effect on moissonneurs.pubmed; its value is added
    #     when processing request client-side, take a deep breath and see
    #     templates/projects/project.html for more details.
    request.POST = {'string': name,
                    'query': query,
                    'N': QUERY_SIZE_N_MAX}
#    request.user = Dummy()
#    request.user.id = project.user_id
#    request.user.is_authenticated = lambda: True

    if moissonneur.name == 'istex':
        # Replace ALL spaces by plus signs
        request.POST['query'] = '+'.join(filter(None, query.split(' ')))

    try:
        import json

        req = moissonneur.query(request)
#        raw_json = r.decode('utf-8')
        if isinstance(req, str):
            data = json.loads(req)#aw_json)

        if moissonneur.name == 'pubmed':
            count = sum(x['count'] for x in req)
            request.POST['query'] = json.dumps(req)#♣.replace("\'", '"')) #hope these are 
        elif moissonneur.name == 'istex':
            count = data.get('total', 0)
        else:
            count = data.get('results_nb', 0)

        if count > 0:
            corpus = moissonneur.save(request, rep, return_corpus=True)
        else:
            return None

    except:
        print ('ca va mal')
        corpus = None

    # Sometimes strange things happens...
#    if corpus.name != name:
#        corpus.name = name
#        session.commit()

    return corpus


ALL_LIST_TYPES = ['main', 'map', 'stop']


#def _ngrams(corpus_id, list_types, entities):
#    list_types = (list_types,) if isinstance(list_types, str) else list_types
#    list_typenames = [
#        '{}LIST'.format(t.upper()) for t in list_types if t in ALL_LIST_TYPES]
#
#    # `Node` is our list, ie. MAINLIST and/or MAPLIST and/or STOPLIST
#    return (session.query(*entities)
#                   .select_from(Ngram)
#                   .filter(NodeNgram.ngram_id==Ngram.id,
#                           NodeNgram.node_id==Node.id,
#                           Node.parent_id==corpus_id,
#                           Node.typename.in_(list_typenames)))
#
#
#def corpus_list(corpus_id, list_types=ALL_LIST_TYPES, with_synonyms=False,
#                with_count=False):
#    # Link between a GROUPLIST, a normal form (ngram1), and a synonym (ngram2)
#    NNN = NodeNgramNgram
#
#    # Get the list type from the Node type -- as in CSV export
#    list_type = (case([(Node.typename=='MAINLIST', 'main'),
#                       (Node.typename=='MAPLIST',  'map'),
#                       (Node.typename=='STOPLIST', 'stop')])
#                 .label('type'))
#
#    # We will retrieve each ngram as the following tuple:
#    entities = (list_type, Ngram.terms.label('ng'))
#
#    if with_count:
#        entities += (Ngram.id.label('id'),)
#
#    # First, get ngrams from wanted lists
#    ngrams = _ngrams(corpus_id, list_types, entities)
#
#    # Secondly, exclude "synonyms" (grouped ngrams that are not normal forms).
#    # We have to exclude synonyms first because data is inconsistent and some
#    # of them can be both in GROUPLIST and in MAIN/MAP/STOP lists. We want to
#    # take synonyms from GROUPLIST only -- see below.
#    Groups = aliased(Node, name='groups')
#    query = (ngrams.outerjoin(Groups, (Groups.parent_id==corpus_id) & (Groups.typename=='GROUPLIST'))
#                   .outerjoin(NNN, (NNN.node_id==Groups.id) & (NNN.ngram2_id==Ngram.id))
#                   .filter(NNN.ngram1_id==None))
#
#    # If `with_synonyms` is True, add them from GROUPLIST: this is the reliable
#    # source for them
#    if with_synonyms:
#        Synonym = aliased(Ngram)
#        ent = (list_type, Synonym.terms.label('ng'), Synonym.id.label('id'))
#        synonyms = (ngrams.with_entities(*ent)
#                          .filter(NNN.ngram1_id==Ngram.id,
#                                  NNN.ngram2_id==Synonym.id,
#                                  NNN.node_id==Groups.id,
#                                  Groups.parent_id==corpus_id,
#                                  Groups.typename=='GROUPLIST'))
#        query = query.union(synonyms)
#
#    # Again, data is inconsistent: MAINLIST may intersect with MAPLIST and
#    # we don't wan't that
#    if 'main' in list_types and 'map' not in list_types:
#        # Exclude MAPLIST ngrams from MAINLIST
#        query = query.except_(_ngrams(corpus_id, 'map', entities))
#
#    if with_count:
#        N = query.subquery()
#        return (session.query(N.c.type, N.c.ng, NodeNodeNgram.score)
#                       .join(Node, (Node.parent_id==corpus_id) & (Node.typename=='OCCURRENCES'))
#                       .outerjoin(NodeNodeNgram, (NodeNodeNgram.ngram_id==N.c.id) &
#                                                 (NodeNodeNgram.node1_id==Node.id) &
#                                                 (NodeNodeNgram.node2_id==corpus_id)))
#
#    # Return found ngrams sorted by list type, and then alphabetically
#    return query.order_by('type', 'ng')
