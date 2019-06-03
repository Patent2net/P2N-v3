# -*- coding: utf-8 -*-
"""
Created on Thu May  2 16:20:09 2019

@author: dreymond
"""

from Patent2Net.P2N_Lib import MakeIram4


def OPSChercheAbstractBrevet(pat, DirStockage ):
    import epo_ops
    from epo_ops.models import Docdb
    from epo_ops.models import Epodoc

    fic = open('../cles-epo.txt', 'r')
    key, secret = fic.read().split(',')
    key, secret = key.strip(), secret.strip()
    fic.close()
    ops_client = epo_ops.Client(key, secret)
    ops_client.accept_type = 'application/json'
    ndb = pat['label']#[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$']brevet['publication-ref'][u'document-id'][0][u'kind']['$'])
    Abstracts = dict()
    if isinstance(ndb, list):
        ndb = ndb[0]
    #print("Retrieving ", ndb)
    pays = pat['country']

    
    for key in ['label', 'country', 'kind']:
        if isinstance(pat[key], list):
            pat[key] = list(set(pat[key])) # hum some problem (again) in cleaning data within the family gatherer... 22/12/15
    if isinstance(pays, list):
        pays = pays[0]
        
    content = 'Abstract'
    endP = 'biblio'
#
    temp =('publication', Epodoc(pays+ndb[2:])) #, brevet[u'document-id'][u'kind']['$']))
    try:
        data = ops_client.published_data(*temp, endpoint = endP)             #ops_client.published_data()
        if data.ok and 'abstract' in str(data.json()):
            CheckDocDB = False
        else:
            CheckDocDB = True
    except Exception as err:
        CheckDocDB = True
    if CheckDocDB:
        if isinstance(pat['kind'], list):
            tempoData = []
            for cc in pat['kind']:
                temp =('publication', Docdb(ndb[2:],pays, cc)) # hope all comes from same country
                try:
                    tempoData.append(ops_client.published_data(*temp, endpoint = endP))
                except:
                    data = None
                    pass
            for dat in tempoData:
                if dat is not None and dat.ok: 
                    contenu = content

                    patentCont = dat.json()
                    Abstracts = MakeIram4(pat, patentCont, contenu)
                    # Make2Iram2 devrait formater le brevet dans un fichier txt au format Iramuteq dans le bon repertoire
                    # Lang est un truc :-) (je crois que cela renvoit la langue de l'abstract récupéré))
    else:
        temp =('publication', Docdb(pat['label'][2:],pat['country'], pat['kind']))
        if data is not None and data.ok:
            contenu = content
            patentCont = data.json()
            Abstracts = MakeIram4(pat, patentCont, contenu)
#    if ops:world-patent-data exchange-documents exchange-documents abstract  
    return Abstracts

def IPCCategorizer(texte, langue):
    import requests
    import xmltodict
    from requests.utils import requote_uri
    import time
    version="20190101" #valid scheme version
    language=langue # or fr, es, de, ru
    number="5" #from 1 to 5
    level= "subgroup" # or class, subclass, maingroup
    # The API service of IPC cat
    if len(texte)>0 and langue in ["fr", "es", "de", "ru"]:
        urlDer = "https://www.wipo.int/classifications/ipc/ipccat?&hierarchiclevel="+level.upper()+"&lang="+language +\
        "&numberofpredictions="+number+"&text="+texte.lower().replace("\n", " ")
        urlDer = requote_uri(urlDer)
        time.sleep(3)
        try:
            req=requests.get(urlDer)
            if req.ok:
                return xmltodict.parse(req.text)
            else:
                return None
        except:
            print("pb  -> ", texte, " ", langue)
    else:
        return None
    
def IPCExtractPredictionBrevet(Predic, seuil):
    Predict = [] # Les prédiction d'IPC dont le score dépasse le seuil
    if 'predictions' in Predic.keys():
        if "msg" in Predic['predictions'].keys():
            if Predic['predictions']['msg'] == 'ok':
                for predic in Predic['predictions']['prediction']:
                    if int(predic["score"]) > seuil:
                        Predict.append(predic)
                    else:
                        pass
            else:
                return None
        else:
            return None
    else:
        return None
    return Predict
    
def strip_accents(text):

    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    import unicodedata
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def PubMedCheckNameAndGetAffiliation(pubmedId, auteur):
    import requests, xmltodict
    from collections import OrderedDict
    Base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=%s&rettype=fasta&retmode=xml" %(pubmedId)
    reponse = requests.get(Base)
    data = None
    if reponse.status_code == 200:
        data = xmltodict.parse(reponse.text)
        Affiliaton = ''
        if 'PubmedArticleSet' in data.keys():
            if 'PubmedArticle' in  data ['PubmedArticleSet'].keys():
                if 'MedlineCitation' in data ['PubmedArticleSet']['PubmedArticle'].keys():
                    if 'Article' in data ['PubmedArticleSet']['PubmedArticle']['MedlineCitation'].keys():
                        if 'AuthorList' in data ['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article'].keys():
                            ListeAuteur = data ['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['AuthorList']
                            if isinstance(ListeAuteur ['Author'], list):
                                for Aut in ListeAuteur ['Author']:
                                    UnicName = False
                                    if not isinstance(Aut, dict):
                                        print ('ARG')
                                    if 'LastName' in Aut.keys():
                                        if 'ForeName' in Aut.keys():
                                            if 'Initials' in Aut.keys():
                                                Nom = Aut['LastName'] +' ' + Aut['ForeName']+ ' ' + Aut['Initials']
                                            else:
                                                Nom = Aut['LastName'] +' ' + Aut['ForeName']
                                        else:
                                            Nom = Aut['LastName']
                                            UnicName = True # in case or a name without lastname in pubmed
                                        Nom = strip_accents(Nom)
                                        if 'AffiliationInfo' in Aut.keys():
                                            # Memo in case of multiple affiliation and the author expected not the first author
                                            if isinstance(Aut['AffiliationInfo'], dict) or  isinstance(Aut['AffiliationInfo'], OrderedDict):
                                                if 'Affiliation' in Aut['AffiliationInfo'].keys():  
                                                    Affiliaton =  Aut['AffiliationInfo']['Affiliation']
                                                elif isinstance(Aut['AffiliationInfo'], list):
                                                    tempo = [aff['Affiliation'] for aff in Aut['AffiliationInfo'] ]
                                                    Affiliaton = '\n'.join(tempo)
                                        #checking it s Firstname and lastname (should work with initials)
                                        if (strip_accents(auteur.split(' ')[0]) in Nom and strip_accents(auteur.split(' ')[1]) in Nom) or (UnicName and (strip_accents(auteur.split(' ')[0]) in Nom or strip_accents(auteur.split(' ')[1]) in Nom)) :
                                            if 'AffiliationInfo' in Aut.keys():
                                                if isinstance(Aut['AffiliationInfo'], dict) or  isinstance(Aut['AffiliationInfo'], OrderedDict):
                                                    if 'Affiliation' in Aut['AffiliationInfo'].keys():  
                                                        return Aut['AffiliationInfo']['Affiliation']
                                                    else:
                                                        print ('inconsistent')
                                                elif isinstance(Aut['AffiliationInfo'], list):
                                                    tempo = [aff['Affiliation'] for aff in Aut['AffiliationInfo'] ]
                                                    return ('\n'.join(tempo))
                                                else:
                                                    print ('Type Affiliation etrange ', type(Aut['AffiliationInfo']), ' --> ', Aut['AffiliationInfo'])
                                            else:
                                                return Affiliaton #if author is the second author in the same structure as primary then the affiliation is not mentioned twice. We use previos.
                                            # I hope the rule is the same for all the number of authors.
                                        else:
                                            pass#This is a co-author
                        
                                    else:
                                        #print (Aut) # CollectiveName
                                        pass
                            else:
                                Aut = ListeAuteur ['Author'] 
                                UnicName = False
                                if not isinstance(Aut, dict):
                                    print ('ARG')
                                if 'LastName' in Aut.keys():
                                    if 'ForeName' in Aut.keys():
                                        if 'Initials' in Aut.keys():
                                            Nom = Aut['LastName'] +' ' + Aut['ForeName']+ ' ' + Aut['Initials']
                                        else:
                                            Nom = Aut['LastName'] +' ' + Aut['ForeName']
                                    else:
                                        Nom = Aut['LastName']
                                        UnicName = True # in case or a name without lastname in pubmed
                                    Nom = strip_accents(Nom)
                                    if 'AffiliationInfo' in Aut.keys():
                                        # Memo in case of multiple affiliation and the author expected not the first author
                                        if isinstance(Aut['AffiliationInfo'], dict) or  isinstance(Aut['AffiliationInfo'], OrderedDict):
                                            if 'Affiliation' in Aut['AffiliationInfo'].keys():  
                                                Affiliaton =  Aut['AffiliationInfo']['Affiliation']
                                            elif isinstance(Aut['AffiliationInfo'], list):
                                                tempo = [aff['Affiliation'] for aff in Aut['AffiliationInfo'] ]
                                                Affiliaton = '\n'.join(tempo)
                                    #checking it s Firstname and lastname (should work with initials)
                                    if (strip_accents(auteur.split(' ')[0]) in Nom and strip_accents(auteur.split(' ')[1]) in Nom) or (UnicName and (strip_accents(auteur.split(' ')[0]) in Nom or strip_accents(auteur.split(' ')[1]) in Nom)) :
                                        if 'AffiliationInfo' in Aut.keys():
                                            if isinstance(Aut['AffiliationInfo'], dict) or  isinstance(Aut['AffiliationInfo'], OrderedDict):
                                                if 'Affiliation' in Aut['AffiliationInfo'].keys():  
                                                    return Aut['AffiliationInfo']['Affiliation']
                                                else:
                                                    print ('inconsistent')
                                            elif isinstance(Aut['AffiliationInfo'], list):
                                                tempo = [aff['Affiliation'] for aff in Aut['AffiliationInfo'] ]
                                                return ('\n'.join(tempo))
                                            else:
                                                print ('Type Affiliation etrange ', type(Aut['AffiliationInfo']), ' --> ', Aut['AffiliationInfo'])
                                        else:
                                            return Affiliaton #if author is the second author in the same structure as primary then the affiliation is not mentioned twice. We use previos.
                                        # I hope the rule is the same for all the number of authors.
                                    else:
                                        pass#This is a co-author
                    
                                else:
                                    print (Aut)
                                    pass
                        else:# no data [..]['AuthorList']
                            pass
                    else: #no data [...]['Article']
                        pass
                    
                else:#no data ['PubmedArticleSet']['PubmedArticle']['MedlineCitation']
                    pass
            else:#no data ['PubmedArticleSet']['PubmedArticle']
                pass
        else:
            #no data ['PubmedArticleSet']
            pass             
    else:
        raise ValueError(reponse.status_code, reponse.reason)
    return None    

