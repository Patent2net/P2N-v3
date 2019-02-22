# -*- coding: utf-8 -*-
# (c) 2017 The Patent2Net Developers

import os
import epo_ops
import json
import cPickle
from epo_ops.models import Epodoc
from P2N_Lib import LoadBiblioFile
from P2N_Config import LoadConfig
import traceback


def get_patent_label(patent):
    if isinstance(patent['label'], list):
        return patent['label'][0]
    return patent['label']


def extract_meta_json_images(js):
    docs_instance = []
    inquiry_result = js['ops:world-patent-data']['ops:document-inquiry']['ops:inquiry-result']
    if isinstance(inquiry_result, list):
        for ir in inquiry_result:
            di = ir['ops:document-instance']
            if isinstance(di, list):
                docs_instance += di
            else:
                docs_instance.append(di)
    else:
        di = inquiry_result['ops:document-instance']
        if isinstance(di, list):
            docs_instance = di
        else:
            docs_instance = [di]
    return docs_instance


def get_images_meta(ops_client, patent_label, path_json):
    # Try to retrieve JSON meta info from local, otherwise get online from OPS
    try:
        return json.load(file(path_json))
    except:
        try:
            ans = ops_client.published_data(reference_type='publication',
                                            input=Epodoc(patent_label), endpoint='images')
            file(path_json, 'w').write(ans.content)
            return ans.json()
        except Exception as err:
            print "...Image meta for {} error".format(patent_label), err
            if hasattr(err, 'response') and err.response.status_code == 404:
                file(path_json, 'w').write('{}')
    return None


def extract_best_images(docs_instance):
    chosen_doc = None
    if isinstance(docs_instance, list):
        for doc in docs_instance:
            name = doc['@desc'].lower()
            if name == u'drawing':  # reset anything before and return this as better images results
                chosen_doc = doc
                break
            # elif name == u'fulldocument':
            #     chosen_doc = doc
            # elif name == u'firstpageclipping' and not chosen_doc:
            #     chosen_doc = doc
            # else:
            #     print 'Non recognized image doc instance', doc
    elif isinstance(docs_instance, dict) and docs_instance['@desc'].lower() == 'drawing':
        chosen_doc = docs_instance
    if not chosen_doc:
        return None, None, None
    link = chosen_doc[u'@link']
    page_start = int(chosen_doc[u'ops:document-section'][u'@start-page'])
    num_pages = int(chosen_doc[u'@number-of-pages'])
    return link, page_start, num_pages


def get_images_files(ops_client, path_image, link, page_start, num_pages):
    pathes = []
    for page in range(page_start, page_start + num_pages):
        path_img = path_image.format(page)
        if not os.path.exists(path_img):
            print '... Retrieving img page {} of {}'.format(page, (page_start + num_pages - 1))
            resp = ops_client.image(link, range=page)
            file(path_img, 'wb').write(resp.content)
        pathes.append(path_img)
    return pathes


def save_array_data(images_path, obj):
    cPickle.dump(obj, file(os.path.join(images_path, 'image_data'), 'w'))


os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'  # cacert.pem
os.environ['CA_BUNDLE'] = 'cacert.pem'

global key
global secret

# put your credential from epo client in this file...
# chargement clés de client
fic = open('../cles-epo.txt', 'r')
key, secret = fic.read().split(',')
key, secret = key.strip(), secret.strip()
fic.close()

configFile = LoadConfig()
IsEnableScript = configFile.GatherImages

ResultBiblioPath = configFile.ResultBiblioPath
ResultPathImages = configFile.ResultPathImages
P2NFamilly = configFile.GatherFamilly

if IsEnableScript:
    ops_client = epo_ops.Client(key, secret)
    ops_client.accept_type = 'application/json'

    prefixes = [""]
    if P2NFamilly:
        prefixes.append("Families")

    for prefix in prefixes:
        ndf = prefix + configFile.ndf

        try:
            biblio_file = LoadBiblioFile(ResultBiblioPath, ndf)
        except IOError as ex:
            print 'WARNING: Could not load information for "{}". Not found / error: {}'.format(ndf, ex)

        patents = biblio_file['brevets']
        metadata = {}

        for patent in patents:
            patent_label = get_patent_label(patent)
            pathes = []
            path_json = '{}//{}.json'.format(ResultPathImages, patent_label)
            path_image = '{}//{}-{}.tiff'.format(ResultPathImages, patent_label, '{}')
            print "Processing patent {}".format(patent_label)
            js = get_images_meta(ops_client, patent_label, path_json)
            if not js:
                continue
            # Try to read JSON meta, otherwise we don't have right meta
            try:
                docs_instance = extract_meta_json_images(js)
            except Exception as err:
                print "...Meta info for {} not found / error".format(patent_label), err
                traceback.print_exc()
                continue

            try:
                link, page_start, num_pages = extract_best_images(docs_instance)
                if link:
                    pathes = get_images_files(ops_client, path_image, link, page_start, num_pages)
                else:
                    print '...Images for patent {} not found'.format(patent_label)
                    continue
            except Exception as err:
                print "...Image for {} error".format(patent_label), err
                if (hasattr(err, 'response')):
                    print err.response.text
                traceback.print_exc()
                continue
            metadata[patent_label] = {
                'pathes': pathes,
                'title': patent['title'],
                'year': patent['year'],
                'country': patent['Applicant-Country'],
            }

    save_array_data(ResultPathImages, metadata)
