import numpy as np

from tqdm import notebook as tqdm
from requests.exceptions import RetryError
import os
#os.environ['PYTHONPATH'] += ":/content/drive/My Drive/Projet7/EssaisTratements/"

import sys

path_to_module = '.'
sys.path.append(path_to_module)

import P2N_Lib
import pandas as pd # pd sera le petit nom utilisé pour utiliser les éléments de la librairie
import numpy as np  # librairie spéciale pour les calculs. Contient notamment la valeur infinie et la valeur "néant"
import requests
from P2N_Lib import Initialize, PatentSearch,  GatherPatentsData
import epo_ops
from tqdm import tqdm
os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'
global key
global secret

with open ('../cles-epo.txt', 'r') as fic:
    pubApiKey = fic.read().strip()
    pubApiKey = pubApiKey.split(',')
key, secret = pubApiKey [0], pubApiKey [1]

ops_client = epo_ops.Client(key, secret)
    #        data = ops_client.family('publication', , 'biblio')
ops_client.accept_type = 'application/json'


Corpus = ["Large", "Univ", "Largebis"]
df =dict()
dfOld = dict()
fics = dict()
for crp in Corpus:
  url = "http://p2n.ecmn-tln.fr/DATA/P7-"+ crp +"/PatentBiblios/P7-" + crp +  '.json'

  dfOld [crp]= pd.read_json (url, orient='table')
  print (crp .strip(), '\t', dfOld [crp] .shape [0], '\tbrevets chargés ')

for crp in Corpus: # nouvelles données post réu 22/09/22
  fics [crp] = 'http://p2n.ecmn-tln.fr/DATA/P7/P7-'+crp + '.json'
  df [crp]= pd.read_json (fics[crp], orient='table')
  print (crp .strip(), '\t', df [crp] .shape [0], '\tbrevets chargés ')
  df[crp] ['Family-Count']= df [crp]['Family-Count'].astype(int)
  df [crp] = df [crp].drop(columns = ['TousAcadFr', 'TousPubliants', 'AcadFr', 'AuteursFrEtNonAuteur','SansPubliants'])

for crp in Corpus:
  df [crp] ['applicant-old'] = dfOld [crp] ['applicant-old']
  df [crp] ['inventor-old'] = dfOld [crp] ['inventor-old']

listeLabel = df [crp] [df [crp]['CitedBy'].isin(['', []])].label

listeLab = []
for champ in ['applicant', 'inventor', 'IPCR1', 'CitedBy']:
  listeLab .extend( df [crp] [df [crp][champ].isin(['', []])].label)


def ExtraitCitations(donne):
    citP = []
    citNpl = []
    if isinstance(donne, dict):
        if "references-cited" in donne.keys():
            assert type(donne) == type(list())
            print("wtf")
        if 'citation' in donne.keys():
            for cita in donne['citation']:
                citPtemp, citNpltemp = ExtraitCitations(cita)
                citP.extend(citPtemp)
                citNpl.extend(citNpltemp)
        if 'patcit' in donne.keys():
            if isinstance(donne['patcit']['document-id'], list):
                for cita in donne['patcit']['document-id']:
                    if cita['@document-id-type'] == "epodoc":
                        citP.append(cita['doc-number']['$'])
            else:
                citP.append(donne['patcit']['document-id']['doc-number']['$'])
        if "nplcit" in donne.keys():

            if 'document-id' in donne['nplcit'].keys():
                if isinstance(donne['nplcit']['document-id'], list):
                    for cita in donne['nplcit']['document-id']:
                        citNpl.append(cita['doc-number']['$'])
                else:
                    citNpl.append(donne['nplcit']['document-id']['doc-number']['$'])
            else:
                citNpl.append(donne['nplcit']["text"]['$'])
                # citNpl = len(donne ['nplcit'])
                # print (donne ['nplcit'])
    else:
        if isinstance(donne, list):
            print('aillle')
            print(donne)

        pass

        # tempo = [ExtraitCitations (dat) for dat in donne]
        # print(tempo)
    return citP, citNpl



def TraiteBrevet(dico):
    res = dict()
    # print(dico.keys())
    # rajouter traitement brevet prioritaire !
    # conserver dans colonne spécifique
    # identifier refs du doc original;
    # identifier refs du brevet prio
    #
    if isinstance(dico, list):
        for machin in dico:
            return TraiteBrevet(machin)
    if 'bibliographic-data' not in dico.keys():  # utile ou pas ????
        if 'publication-reference' in dico .keys():
            if dico['publication-reference']['document-id']['@document-id-type'] == 'epodoc':
                res['num'] = dico['publication-reference']['document-id']['doc-number']['$']
        else:
            res['num'] = dico ['exchange-document']['@country'] + dico ['exchange-document']['@doc-number']+dico ['exchange-document']['@kind'] # docdb

    if 'exchange-documents' in dico.keys():
        if isinstance(dico['exchange-documents'], dict):
            if isinstance(dico['exchange-documents']['exchange-document'], dict):
                return TraiteBrevet(dico['exchange-documents']['exchange-document'])
            else:
                for truc in dico['exchange-documents']['exchange-document']:
                    return TraiteBrevet(truc)  # HUM big bazard potentiel là !!!!
        else:
            for truc in dico['exchange-documents']:
                return TraiteBrevet(truc)
    elif 'exchange-document' in dico.keys():
        dico = dico['exchange-document']
        if 'publication-reference' in dico.keys():
            if isinstance(dico['publication-reference'], list):
                for nom in dico['publication-reference']['document-id']:
                    if nom['@document-id-type'] == 'epodoc':
                        res['num'] = nom['doc-number']['$']
            else:
                if dico['publication-reference']['document-id']['@document-id-type'] == 'epodoc':
                    res['num'] = dico['publication-reference']['document-id']['doc-number']['$']
                else:
                    print("as de nom", dico['publication-reference']['document-id'])
    elif 'bibliographic-data' in dico.keys():
        if 'publication-reference' in dico['bibliographic-data'].keys():
            for nom in dico['bibliographic-data']['publication-reference']['document-id']:
                if nom['@document-id-type'] == 'epodoc':
                    res['num'] = nom['doc-number']['$']
    elif 'ops:biblio-search' in dico.keys():
        if 'ops:search-result' in dico['ops:biblio-search'].keys():
            return TraiteBrevet(dico['ops:biblio-search']['ops:search-result'])


    else:
        return TraiteBrevet(dico['exchange-documents']['exchange-document'])  # HUM big bazard potentiel là !!!!
        # print(dico['bibliographic-data']['publication-reference']['document-id'])

    if 'abstract' in dico.keys():
        if isinstance(dico['abstract'], dict):
            lang = dico['abstract']['@lang']
            resum = dico['abstract']['p']['$']
            res['abstract'] = [lang, resum]
        else:
            res['abstract'] = []
            for truc in dico['abstract']:
                lang = truc['@lang']
                resum = truc['p']['$']
                res['abstract'].append([lang, resum])
    else:
        res['abstract'] = []

    if 'applicants' in dico['bibliographic-data']["parties"].keys():
        res['applicants'] = []
        if isinstance(dico['bibliographic-data']["parties"]['applicants'], list):
            for app in dico['bibliographic-data']["parties"]['applicants']:
                if isinstance(app, dict):
                    if isinstance(app['applicant'], list):
                        for ap in app['applicant']:
                            if ap['@data-format'] == "epodoc":
                                res['applicants'].append(ap['applicant-name']['name']['$'])
                    else:
                        res['applicants'].append(app['applicant']['applicant-name']['name']['$'])
        elif isinstance(dico['bibliographic-data']["parties"]['applicants'], dict):
            if isinstance(dico['bibliographic-data']["parties"]['applicants']['applicant'], list):
                for app in dico['bibliographic-data']["parties"]['applicants']['applicant']:
                    if isinstance(app, dict):
                        if app['@data-format'] == "epodoc":
                            res['applicants'].append(app['applicant-name']['name']['$'])
                        else:
                            pass
                    else:
                        pass
            else:

                pass
        elif dico['bibliographic-data']["parties"]['applicants']['applicant']['@data-format'] == "epodoc":
                res['applicants'].append(dico['bibliographic-data']["parties"]['applicants']['applicant']['name']['$'])
        else:
            pass
                    #print(app)
                    # print ('match')

                # print (dico['bibliographic-data']["parties"]['applicants']['applicant'])
            # print(dico['bibliographic-data']["parties"]['applicants'])
    # data2 ['ops:world-patent-data']['ops:equivalents-inquiry'] ['ops:inquiry-result'][0]['exchange-documents']['exchange-document']['bibliographic-data']["parties"]['inventors']['inventor'][1]['inventor-name']['name']['$']
    if 'inventors' in dico['bibliographic-data']["parties"].keys():
        res['inventors'] = []
        if isinstance(dico['bibliographic-data']["parties"]['inventors'], list):
            for app in dico['bibliographic-data']["parties"]['inventors']:
                if isinstance(app, dict):
                    if isinstance(app['inventor'], list):
                        for ap in app['inventor']:
                            if ap['@data-format'] == "epodoc":
                                res['inventors'].append(ap['inventor-name']['name']['$'])
                    else:
                        res['inventors'].append(app['inventor']['inventor-name']['name']['$'])
        elif isinstance(dico['bibliographic-data']["parties"]['inventors']['inventor'], list):
            for inv in dico['bibliographic-data']["parties"]['inventors']['inventor']:
                if inv ['@data-format'] == "epodoc":
                    res['inventors'].append(inv['inventor-name']['name']['$'])
        elif dico['bibliographic-data']["parties"]['inventors']['inventor']['@data-format'] == 'epodoc':
                    res['inventors'].append(
                        dico['bibliographic-data']["parties"]['inventors']['inventor']['inventor']['inventor-name']['name']['$'])
                    # print ('match')
        else:
            print("WTF inventors") # pas de nom d'inventeur au format epodoc... Tout passer à "original" ?
                #res['inventors'].append(dico['bibliographic-data']["parties"]['inventors']['inventor']['inventor-name']['name']['$'])
            pass

        # res ['inventors'] =  dico['bibliographic-data']["parties"]['inventors']
    if 'invention-title' in dico['bibliographic-data'].keys():
        if isinstance(dico['bibliographic-data']["invention-title"], list):
            for truc in dico['bibliographic-data']["invention-title"]:
                if "@lang" in truc.keys():
                    titreEN, titreOl, titreFR = "", "", ""
                    if truc["@lang"] == 'en':
                        res['titreEN'] = truc["$"]
                    elif truc["@lang"] == 'fr':
                        res['titreFR'] = truc["$"]
                    else:
                        res['titreOl'] = truc["$"]
        else:
            truc = dico['bibliographic-data']["invention-title"]
            if "@lang" in truc.keys():
                titreEN, titreOl, titreFR = "", "", ""
                if truc["@lang"] == 'en':
                    res['titreEN'] = truc["$"]
                elif truc["@lang"] == 'fr':
                    res['titreFR'] = truc["$"]
                else:
                    res['titreOl'] = truc["$"]
        # print (dico['bibliographic-data']["invention-title"])
    Classif = []
    if 'classifications-ipcr' in dico['bibliographic-data'].keys():
        for ipc in dico['bibliographic-data']['classifications-ipcr']['classification-ipcr']:
            try:
                Classif.append(ipc['text']['$'].replace(' ', ''))
            except:
                pass
                # print (ipc)
        if len(Classif) ==0:
            Classif.append(dico['bibliographic-data']['classifications-ipcr']['classification-ipcr']['text']['$'].replace(' ', ''))
    res['classif'] = Classif
    if 'references-cited' in dico['bibliographic-data'].keys():
        # print ("refs trouvées")
        # print (dico['bibliographic-data']['references-cited'] )
        res["refP"], res["refNpl"] = [], []
        for pipo in dico['bibliographic-data']['references-cited']['citation']:
            tempoP, tempoNpl = ExtraitCitations(pipo)
            res["refP"].extend(tempoP)
            res["refNpl"].extend(tempoNpl)
        # res ["refP"],res ["refNpl"] = ExtraitCitations(dico['bibliographic-data']['references-cited']['citation'])
    if 'citation' in dico['bibliographic-data'].keys():
        # print ("citations trouvées")
        # print (data ['ops:world-patent-data']['exchange-documents']['exchange-document']['bibliographic-data']['citation'])
        res["citations"] = ExtraitCitations(dico['bibliographic-data']['citation'])
    priority =[]
    if 'priority-claims' in dico['bibliographic-data'].keys():
        if isinstance(dico['bibliographic-data']['priority-claims']['priority-claim'], list):
            for machin in dico['bibliographic-data']['priority-claims']['priority-claim']:
                if isinstance(machin['document-id'], list):
                    for truc in machin['document-id']:
                        if  truc ['@document-id-type'] == 'epodoc':
                            prior = truc ['doc-number']['$']
                            date = truc ['date']['$']
                            priority.append((prior, date))
                elif machin['document-id'] ['@document-id-type'] == 'epodoc':
                    prior = machin ['document-id']['doc-number']['$']
                    date = machin ['document-id']['date']['$']
                    priority.append((prior, date))
                # print (type(dico['bibliographic-data']['priority-claims']['priority-claim']['document-id']))
        elif isinstance(dico['bibliographic-data']['priority-claims']['priority-claim']['document-id'], list):
            for truc in dico['bibliographic-data']['priority-claims']['priority-claim']['document-id']:
                if truc ['@document-id-type'] == 'epodoc':
                    prior = truc['doc-number']['$']
                    date = truc['date']['$']
                    priority.append((prior, date))
                else:
                    pass
        else:
            if dico['bibliographic-data']['priority-claims']['priority-claim']['document-id']['@document-id-type'] == 'epodoc':
                prior = dico['bibliographic-data']['priority-claims']['priority-claim']['document-id']['doc-number']['$']
                date = dico['bibliographic-data']['priority-claims']['priority-claim']['document-id']['date']['$']
                priority.append((prior, date))
            else:
                pass
                #print (dico['bibliographic-data']['priority-claims']['priority-claim']['document-id'])

    res ['priority'] = list(set(priority))
    return res


    #df [crp] .astype('object')

#Corpus = ['Univ', 'Largebis']

for crp in Corpus:
    for truc in ['CitP-new', 'CitO-new', 'Citations-new',  'CitedBy-new','references-new', "equivalents-new",'inventor-new', 'applicant-new', 'inventor-newCheck','classification-prio', 'IPCR1-prio','IPCR3-prio', 'IPCR4-prio', 'IPCR7-prio', 'IPCR11-prio', 'CitP-prio', 'CitO-prio', 'CitedBy-prio', 'Citations-prio', 'Citations-prio', 'references-prio', 'equivalents-prio', 'applicant-prio', 'inventor-prio']:
         df [crp][truc] = '' #pd.Series(dtype='object')
    listeLab = []
    for champ in ['applicant', 'inventor', 'IPCR1', 'CitedBy']: # on ne prends que ceux qui manquent
        listeLab .extend( df [crp] [df [crp][champ].isin(['', []])].label)
    listeLab = df[crp] ['label'].tolist() # Finalement on les prends tous
    listeLabel = list(set(listeLab))
    print(crp)
    pbar = tqdm (listeLabel , desc = crp)

    for lab in pbar:
        # creation nouvelles colonnes:

        try:
            bre = ops_client.published_data(  # Retrieve bibliography data
                reference_type = 'publication',  # publication, application, priority
                input =  epo_ops.models.Epodoc (lab),  # original, docdb, epodoc
                endpoint = 'biblio',  # optional, defaults to biblio in case of published_data
                constituents = ['']  # optional, list of constituents
            )
            data = bre .json()
            donnes = data ['ops:world-patent-data']

            res1 = [TraiteBrevet (donnes['exchange-documents']['exchange-document'])]

        except: # sinon on essaye de retrouver
            try:
                bre = ops_client.published_data_search(  # Retrieve bibliography data
                    # reference_type = 'publication',  # publication, application, priority
                    cql= 'pn= ' +lab,  # original, docdb, epodoc
                    # endpoint = 'biblio',  # optional, defaults to biblio in case of published_data
                    constituents = ['biblio']  # optional, list of constituents
                )
                datab = bre .json()
                if isinstance(datab['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents'], list):
                    res1 = []
                    for doc in datab['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']:
                        res1 .append(TraiteBrevet (doc))
                else:
                    res1 = [TraiteBrevet(datab['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']['exchange-document'])]
            except: # pour éviter le mélange de données
                bre =dict()
                res1 = []
                pass


        try:
            bre2 = ops_client.published_data(  # Retrieve bibliography data
                reference_type='publication',  # publication, application, priority
                input=epo_ops.models.Epodoc(lab),  # original, docdb, epodoc
                endpoint='equivalents',  # optional, defaults to biblio in case of published_data
                constituents=['biblio']  # optional, list of constituents
            )
            data2 = bre2.json()  #
            res2 = []
            if isinstance(data2['ops:world-patent-data']['ops:equivalents-inquiry']['ops:inquiry-result'], list):
                for truc in data2['ops:world-patent-data']['ops:equivalents-inquiry']['ops:inquiry-result']:
                    res2.append(TraiteBrevet(truc))
            else:
                res2 = [TraiteBrevet(data2['ops:world-patent-data']['ops:equivalents-inquiry']['ops:inquiry-result'])]

        except:  # sinon on essaye de retrouver par le num retrouvé à l'exception précédente
            nums = []
            if "res2" not in locals():
                res2=[]
            for br in res1:
                if "num" in br.keys():
                    nums.append(br["num"])
            data3 = dict()
            if len(nums) > 0:
                try:
                    bre2 = ops_client.published_data(  # Retrieve bibliography data
                        reference_type='publication',  # publication, application, priority
                        input=epo_ops.models.Epodoc(nums[0]),  # original, docdb, epodoc
                        endpoint='equivalents',  # optional, defaults to biblio in case of published_data
                        constituents=['biblio']  # optional, list of constituents
                    )
                    data3 = bre2.json()  # sinon çà explose je suppose
                    if isinstance(data3['ops:world-patent-data']['ops:equivalents-inquiry']['ops:inquiry-result'], list):
                        for truc in data3['ops:world-patent-data']['ops:equivalents-inquiry']['ops:inquiry-result']:
                            res2.append(TraiteBrevet(truc))
                    else:
                        res2 = [TraiteBrevet(data3['ops:world-patent-data']['ops:equivalents-inquiry']['ops:inquiry-result'])]
                except:
                    pass
            else:
                pass
                print (nums, res1, lab)


        avEqui = len(list(df[crp].loc[(df[crp]['label'] == lab)]['equivalents'])[0])
        avCita = int(df[crp].loc[(df[crp]['label'] == lab)]['Citations'])
        avRef = int(df[crp].loc[(df[crp]['label'] == lab)]['references'])
        avClassif = len(list(df[crp].loc[(df[crp]['label'] == lab)]['classification'])[0])
        # print (data2)

        df[crp].astype('object')


        for br in res1:
            res2.append(br)
        equiv = [lab]
        appli = []
        inv = []
        classe = []
        refP, refNpl, cita = [], [], []
        priorities = []
        priorDate = 0
        priorFR =''
        restemp = []
        for br in res2:
            if len(br.keys())>1:
                if "citations" in br.keys():
                    if len(br ["citations"])> 0:
                        restemp.append(br)
                    else:
                        br.pop("citations")
                        restemp.append(br)
                else:
                    restemp.append(br)
            elif "citations" in br.keys():
                    if len(br ["citations"])> 0:
                        restemp.append(br)
                    else:
                        br.pop("citations")
            else:
                restemp.append(br)

        res2 = restemp
        for br in res2:
            if "num" in br.keys():
                equiv.append(br["num"])
            if "priority" in br .keys():
                if isinstance(br ['priority'], list):
                    for prior in br ['priority']:
                        if prior [0].startswith('FR') and int(prior[1][0:4]) > priorDate:
                            priorFR = prior [0]
                            priorDate = int(prior[1][0:4]) # juste l'année
                        else:
                            priorities .append(br ['priority'])

        ###Citations
        for ind in range(len(res2)):#for label in equiv:
            try:
                label = res2[ind]["num"]
                bre = ops_client.published_data_search(  # Retrieve bibliography data
                    # reference_type = 'publication',  # publication, application, priority
                    cql='ct=' + label,  # original, docdb, epodoc
                    # endpoint = 'biblio',  # optional, defaults to biblio in case of published_data
                    constituents=['biblio']  # optional, list of constituents
                )
                data = bre.json()
                res4 = []
                if isinstance(data['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents'],list):
                    for doc in data['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']:
                        res4.append(TraiteBrevet(doc))
                else:
                    try:
                        res4 = [TraiteBrevet(data['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']['exchange-document'])]
                    except:
                        if isinstance(data['ops:world-patent-data']['exchange-documents'], list):
                            for doc in data['ops:world-patent-data']['exchange-documents']:
                                res4.append(TraiteBrevet(doc))
                        else:
                            res4 = [TraiteBrevet(data['ops:world-patent-data']['exchange-documents'])]

                res2[ind]["citations"] = [br['num'] for br in res4]
            except:  # pour éviter le mélange de données
                res2[ind]["citations"] = []


        resPrior =''

        if priorDate != 0 and priorFR not in equiv:
            if len(priorFR) >0:
                try:
                    bre3 = ops_client.published_data(  # Retrieve bibliography data
                        reference_type='publication',  # publication, application, priority
                        input=epo_ops.models.Epodoc(priorFR),  # original, docdb, epodoc
                        endpoint='biblio',  # optional, defaults to biblio in case of published_data
                        constituents=['']  # optional, list of constituents
                    )
                    data3 = bre3.json()
                    resPrior = []
                    if isinstance(data3['ops:world-patent-data']['ops:equivalents-inquiry']['ops:inquiry-result'], list):
                        for truc in data3['ops:world-patent-data']['ops:equivalents-inquiry']['ops:inquiry-result']:
                            resPrior.append(TraiteBrevet(truc))
                    else:
                        resPrior = [TraiteBrevet(data3['ops:world-patent-data']['ops:equivalents-inquiry']['ops:inquiry-result'])]
                except:
                    try: #numéro de demande
                        bre3 = ops_client.published_data_search(  # Retrieve bibliography data
                                # reference_type = 'publication',  # publication, application, priority
                                cql= "ap =" + priorFR,  # original, docdb, epodoc
                                # endpoint = 'biblio',  # optional, defaults to biblio in case of published_data
                                constituents=['biblio']  # optional, list of constituents
                            )
                        data3 = bre3.json()
                        resPrior = []
                        if isinstance(data3['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents'], list):
                            resPrior = []
                            for doc in data3['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']:
                                resPrior.append(TraiteBrevet(doc))
                        else:
                            resPrior = [TraiteBrevet(data3['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']['exchange-document'])]
                    except:
                        try:  # numéro de priorité
                            bre3 = ops_client.published_data_search(  # Retrieve bibliography data
                                # reference_type = 'publication',  # publication, application, priority
                                cql="pr=" + priorFR,  # original, docdb, epodoc
                                # endpoint = 'biblio',  # optional, defaults to biblio in case of published_data
                                constituents=['biblio']  # optional, list of constituents
                            )
                            data3 = bre3.json()
                            resPrior = []
                            if isinstance(data3['ops:world-patent-data']['ops:biblio-search']['ops:search-result'][
                                              'exchange-documents'], list):
                                resPrior = []
                                for doc in data3['ops:world-patent-data']['ops:biblio-search']['ops:search-result'][
                                    'exchange-documents']:
                                    resPrior.append(TraiteBrevet(doc))
                            else:
                                resPrior = [TraiteBrevet(
                                    data3['ops:world-patent-data']['ops:biblio-search']['ops:search-result'][
                                        'exchange-documents']['exchange-document'])]
                        except:
                            try:  # tous les numéros
                                bre3 = ops_client.published_data_search(  # Retrieve bibliography data
                                    # reference_type = 'publication',  # publication, application, priority
                                    cql="num" + priorFR,  # original, docdb, epodoc
                                    # endpoint = 'biblio',  # optional, defaults to biblio in case of published_data
                                    constituents=['biblio']  # optional, list of constituents
                                )
                                data3 = bre3.json()
                                resPrior = []
                                if isinstance(data3['ops:world-patent-data']['ops:biblio-search']['ops:search-result'][
                                                  'exchange-documents'], list):
                                    resPrior = []
                                    for doc in data3['ops:world-patent-data']['ops:biblio-search']['ops:search-result'][
                                        'exchange-documents']:
                                        resPrior.append(TraiteBrevet(doc))
                                else:
                                    resPrior = [TraiteBrevet(
                                        data3['ops:world-patent-data']['ops:biblio-search']['ops:search-result'][
                                            'exchange-documents']['exchange-document'])]
                            except:
                                print ("aucun num ?????", priorFR)


        for br in res2:
            # if "num" not in br .keys():
            #     pass
            # else:
            #     if br["num"] == priorFR:
            #         switch = True
            #     else:
            #         switch = False
            #     # if switch:
            #     #     resPrio = br
            if "inventors" in br.keys():
                assert type(br["inventors"]) == type(list())
                for invent in br["inventors"]:
                    inv.append(invent)
                    
            if "applicants" in br.keys():
                assert type(br["applicants"]) == type(list())
                for invent in br["applicants"]:
                    appli.append(invent)
            if "num" in br.keys():
                equiv.append(br["num"])
                

            if 'classif' in br.keys():
                assert type(br["classif"]) == type(list())
                aPlat = [truc for truc in [cla[0:len(cla) - 2] for cla in br['classif']]]
                for cla in aPlat:
                    classe.append(cla)
            if 'refP' in br.keys():
                assert type(br["refP"]) == type(list())
                aPlat = [truc for truc in [cla for cla in br['refP']]]
                for ref in aPlat:
                    refP.append(ref)
            if 'refNpl' in br.keys():
                assert type(br["refNpl"]) == type(list())
                aPlat = [truc for truc in [cla for cla in br['refNpl']]]
                for ref in aPlat:
                    refNpl.append(ref)

            if 'citations' in br.keys():
                assert type(br["citations"]) == type(list())
                if len(br["citations"]) > 0:
                    for cit in br["citations"]:
                        cita.append(cit)

        labPrior = set([truc1[0] for truc in priorities  for truc1 in truc ])
        try:
            resPrio = [br for br in [pa for pa in resPrior if 'num' in pa .keys()]  if br ['num'] .startswith('FR')][0]
        except:
            try:
                resPrio = [br for br in [pa for pa in resPrior if 'num' in pa .keys()]  if br['num'].startswith('EP')][0]
            except:
                try:
                    resPrio = [br for br in [pa for pa in resPrior if 'num' in pa .keys()]  if br['num'].startswith('WO')][0]
                except:

                    print ("AILLLLLE")


        for indisp in ['classification', 'CitP', 'CitO', 'CitedBy', 'Citations', 'references', 'equivalents', 'applicant', 'inventor']:
            if indisp not in resPrio.keys():
               for bre in resPrior:
                   if indisp in bre .keys():
                       if len(bre [indisp])>0:
                           resPrio [indisp] = bre [indisp] # joyeux mélange
        if len(resPrio) == 0:
           for br in res2:
               if "num" in br .keys():
                    if br ['num'] in [lab for lab, date in labPrior]:
                        resPrio = br
                   # on parit que le brevet est consistant et qu'on va le trouver !
                   # perdu

        if len(resPrio) != 0:
            #traitement du brevet prioritaire
            try:
                label = resPrio["num"]
                bre = ops_client.published_data_search(  # Retrieve bibliography data
                    # reference_type = 'publication',  # publication, application, priority
                    cql='ct=' + label,  # original, docdb, epodoc
                    # endpoint = 'biblio',  # optional, defaults to biblio in case of published_data
                    constituents=['biblio']  # optional, list of constituents
                )
                data = bre.json()
                res4 = []
                if isinstance(data['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents'],list):
                    for doc in data['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']:
                        res4.append(TraiteBrevet(doc))
                else:
                    try:
                        res4 = [TraiteBrevet(data['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']['exchange-document'])]
                    except:
                        print ('arg')
                resPrio["citations"] = [br['num'] for br in res4]
            except:  # pour éviter le mélange de données
                resPrio ["citations"] = []

            if 'classif' in resPrio.keys():  # la plupart des tests sont inutiles ci-dessous
                temp = resPrio['classif']
                tempp = [cla for cla in temp if len(cla) > 0]
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'classification-prio'] = tempp
                ipcr1, ipcr3, ipcr4, ipcr7 = [], [], [], []
                for cla in temp:
                        ipcr1.append(cla[0:1])
                        ipcr3.append(cla[0:3])
                        ipcr4.append(cla[0:4])
                        if "/" in cla:
                            ipcr7.append(cla[0:cla.index('/')])
                        elif len(cla)>6:
                            ipcr7.append(cla[0:6])
                        else:
                            ipcr7.append(cla)
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'IPCR1-prio'] = list(set(ipcr1)) #pd.Series(list(set(ipcr1)), dtype=object)
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'IPCR3-prio'] = list(set(ipcr3)) #pd.Series(list(set(ipcr3)), dtype=object)
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'IPCR4-prio'] = list(set(ipcr4)) #pd.Series(list(set(ipcr4)), dtype=object)
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'IPCR7-prio'] = list(set(ipcr7)) #pd.Series(list(set(ipcr7)), dtype=object)
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'IPCR11-prio'] = list(set(tempp)) #pd.Series(list(set(tempp)), dtype=object)
            if 'refP' in resPrio.keys():
                temp = pd.Series(resPrio['refP'], dtype=object)
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'CitP-prio'] = temp.values  #
                nbrefP = len(temp)
            if 'refNpl' in resPrio.keys():
                temp = pd.Series(resPrio['refNpl'], dtype=object)
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'CitO-prio'] = temp.values  #
                nbrefNpl = len(temp)
            if 'citations' in resPrio.keys():
                temp = pd.Series(resPrio['citations'], dtype=object)
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'CitedBy-prio'] = temp.values  #
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'Citations-prio'] = len(temp)
            else:
                    df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'Citations-prio'] = 0

            if 'refP' in resPrio.keys() or 'refNpl' in resPrio.keys():
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'references-prio'] = nbrefP + nbrefNpl


            temp = pd.Series(equiv, dtype=object)
            df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'equivalents-prio'] = temp.values

            if 'applicants' in resPrio.keys():
                temp = pd.Series(resPrio['applicants'], dtype=object)
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'applicant-prio'] = temp.values
            if 'inventors' in resPrio.keys():
                temp = pd.Series(resPrio['inventors'], dtype=object)
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'inventor-prio'] = temp.values
        else:
            print("GRRRRR")

        res3 = {"inventors": list(set(inv)),
                "applicants": list(set(appli)),
                "num": list(set(equiv)),
                'classif': list(set(classe)),
                'refP': list(set(refP)),
                'refNpl': list(set(refNpl)),
                "citations": list(set(cita)),
                "equivalents": list(set(equiv))
                }
        refP, refNpl = 0, 0
        if 'classif' in res3.keys():  # la plupart des test sont inutiles ci-dessous
            if len(df[crp].loc[(df[crp]['label'] == lab)]['classification'].tolist()[0]) <= len(res3['classif']):
                temp = res3['classif']
                tempp = [cla for cla in temp if len(cla) > 0]
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'classification'] = tempp
                ipcr1, ipcr3, ipcr4, ipcr7, ipcr11 = [], [], [], [], []
                for cla in temp:
                    if len(cla) > 2:
                        ipcr1.append(cla[0:1])
                    if len(cla) > 3:
                        ipcr3.append(cla[0:3])
                    if len(cla) > 4:
                        ipcr4.append(cla[0:4])
                    if len(cla) > 6:
                        if "/" in cla:
                            ind = cla .index('/')
                            ipcr7.append(cla[0:ind])
                        else:
                            ipcr7.append(cla[0:7])
                    if len(cla) > 7:
                        ipcr11 .append(cla)
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'IPCR1'] = list(set(ipcr1))
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'IPCR3'] = list(set(ipcr3))
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'IPCR4'] = list(set(ipcr4))
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'IPCR7'] = list(set(ipcr7))
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'IPCR11'] = list(set(ipcr11))
        if 'refP' in res3.keys():
            if len(list(df[crp].loc[(df[crp]['label'] == lab)]['CitP'])) <= len(res3['refP']):
                # df [crp].loc[df [crp].loc[df[crp]['label']==lab] .index[0], 'CitP-new'] = df [crp].loc[df [crp].loc[df[crp]['label']==lab] .index[0], 'CitP-new'].astype('object')
                temp = pd.Series(res3['refP'], dtype=object)
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'CitP-new'] = temp.values  #
                refP = len(temp)
        if 'refNpl' in res3.keys():
            if len(list(df[crp].loc[(df[crp]['label'] == lab)]['CitO'])) <= len(res3['refNpl']):
                # df [crp].loc[df [crp].loc[df[crp]['label']==lab] .index[0], 'CitO-new']= df [crp].loc[df [crp].loc[df[crp]['label']==lab] .index[0], 'CitO-new'].astype('object')
                temp = pd.Series(res3['refNpl'], dtype=object)
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'CitO-new'] = temp.values  #
                refNpl = len(temp)
        if 'citations' in res3.keys():
            if len(list(df[crp].loc[df[crp]['label'] == lab, 'CitedBy'])) <= len(res3['citations']):
                # df [crp].loc[df [crp].loc[df[crp]['label']==lab] .index[0], 'CitedBy-new'] = df [crp].loc[df [crp].loc[df[crp]['label']==lab] .index[0], 'CitedBy-new'].astype('object')
                temp = pd.Series(res3['citations'], dtype=object)
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'CitedBy-new'] = temp.values  #
                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'Citations-new'] = len(temp)
            else:
                # df [crp].at[df [crp].loc[df[crp]['label']==lab] .index[0], 'CitedBy-new'] = [] #

                df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'Citations-new'] = 0
        else:
            # df [crp].at[df [crp].loc[df[crp]['label']==lab] .index[0], 'CitedBy-new'] = [] #
            df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'Citations-new'] = 0
        if 'refP' in res3.keys() or 'refNpl' in res3.keys():
            df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'references-new'] = int(refP + refNpl)

        if len(list(df[crp].loc[(df[crp]['label'] == lab)]['equivalents'])[0]) <= len(equiv):
            # df [crp].loc[df[crp]['label']==lab, 'equivalents-new']= df [crp].loc[df[crp]['label']==lab, 'equivalents'].astype('object')
            temp = pd.Series(equiv, dtype=object)
            df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'equivalents-new'] = temp.values
        # df[crp]['applicant-old'] = df[crp]['applicant-old'].astype('object')
        # df[crp]['applicant-new'] = df[crp]['applicant-old'].astype('object')
        appli = [machin for truc in appli for machin in truc if len(machin) > 0]
        if len(res3['applicants']) > 0:
            temp = pd.Series(res3['applicants'], dtype=object)
            df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'applicant-new'] = temp.values

        if len(list(df[crp].loc[(df[crp]['label'] == lab)]['inventor-old'])[0]) == 0 and len(
                set(res3['inventors'])) > 0:
            temp = pd.Series(res3['inventors'], dtype=object)
            df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'inventor-new'] = temp.values
        else:
            temp = pd.Series(res3['inventors'], dtype=object)
            df[crp].at[df[crp].loc[df[crp]['label'] == lab].index[0], 'inventor-newCheck'] = temp.values
        apEqui = len(list(df[crp].loc[(df[crp]['label'] == lab)]['equivalents'])[0])
        apCita = int(df[crp].loc[(df[crp]['label'] == lab)]['Citations'])
        apRef = int(df[crp].loc[(df[crp]['label'] == lab)]['references'])
        apClassif = len(df[crp].loc[(df[crp]['label'] == lab)]['classification'].tolist()[0])


for crp in Corpus:
  json_file = df [crp].to_json(orient='table')
  with open('P7-'+ crp + "Enrichi.json", 'w') as f:
      f.write(json_file)

with pd.ExcelWriter('P7-'+ crp +'-Enrichi.xlsx') as writer:
  for crp in Corpus:
      df[crp] = df[crp].astype(str)
      df [crp].to_excel(excel_writer=writer, sheet_name=crp)
