# -*- coding: utf-8 -*-
"""
Created on Tue Avr 1 13:41:21 2014

@author: dreymond
After loading patent list (created from
OPSGather-BiblioPatent), the script will proceed a check for each patent
if it is orphan or has a family. In the last case, family patents are added to
the initial list (may be some are already in it), and a hierarchic within
the priority patent (selected as the oldest representative) and its brothers is created.
IRAMUTEQ tagguing is added to analyse content
****PatentNumber ****date ****CIB3
"""

#BiblioProperties = ['publication-ref', 'priority-active-indicator', 'classification',
#u'resume', 'IPCR1', 'portee', 'IPCR3', 'applicant', 'IPCR4', 'IPCR7', 'label', 'IPCR11',
#'date', 'citations', 'application-ref', 'pays', u'abstract', 'titre', 'inventeur',
#'representative']

BiblioProperties =  ['applicant', 'application-ref', 'citations', 'classification',
                     'prior-Date', 'prior-dateDate'
'inventor', 'IPCR1', 'IPCR11', 'IPCR3', 'IPCR4', 'IPCR7', 'label', 'country', 'kind',
'priority-active-indicator', 'title','date',"publication-ref","representative",
"CPC", "prior", "priority-claim", "year", "family-id", "equivalent",
 'inventor-country', 'applicant-country', 'inventor-nice', 'applicant-nice', 'CitP', 'CitO', 'references']
#from networkx_functs import *
#import pickle

import os
import sys
import epo_ops
from epo_ops.models import Docdb
from epo_ops.models import Epodoc
from Patent2Net.P2N_Lib import MakeIram2, LoadBiblioFile
from Patent2Net.P2N_Config import LoadConfig


os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'#cacert.pem
os.environ['CA_BUNDLE'] = 'cacert.pem'

global key
global secret

# put your credential from epo client in this file...
# chargement clés de client
fic = open('../cles-epo.txt', 'r')
key, secret = fic.read().split(',')
key, secret = key.strip(), secret.strip()
fic.close()


DureeBrevet = 20
SchemeVersion = '20140101' #for the url to the classification scheme

ListeBrevet = [] # The patent List

configFile = LoadConfig()
requete = configFile.requete
GatherContent = configFile.GatherContent
GatherBiblio = configFile.GatherBiblio
GatherPatent = configFile.GatherPatent
GatherFamilly = configFile.GatherFamilly
IsEnableScript = configFile.GatherIramuteq

 #should set a working dir one upon a time... done it is temporPath
ResultBiblioPath = configFile.ResultBiblioPath
ResultPathContent= configFile.ResultContentsPath
temporPath = configFile.temporPath
ResultAbstractPath = configFile.ResultAbstractPath

#by default, data are not gathered yet
ficOk = False


# à ce niveau de script, la liste des brevets est chargée avec des données
# biblio qui vont être complétées
#import time, pprint

cptNotFound=0
def dictCleaner(dico): #same in OpsGatherAugmentFamilies
    for clef in list(dico.keys()):
        if isinstance(dico[clef], list) and len(dico[clef]) ==1:
            dico[clef] = dico[clef][0]
        elif isinstance(dico[clef], list) and len(dico[clef]) == 0:
            dico[clef] = ''
        elif isinstance(dico[clef], list) and len(dico[clef]) >1:
            if '' in dico[clef]:
                for nb in range(dico[clef].count('')):
                    dico[clef].remove('')
        else:
            pass
    return dico

if IsEnableScript:
    GatherContent = True
    #not fun
    ops_client = epo_ops.Client(key, secret)
    #        data = ops_client.family('publication', , 'biblio')
    ops_client.accept_type = 'application/json'

    for ndf in [fic2 for fic2 in os.listdir(ResultBiblioPath) if fic2.count('Description')==0]:
        if ndf.startswith('Families'):
            typeSrc = 'Families'
        else:
            typeSrc = ''
        if ('Description'+ndf in os.listdir(ResultBiblioPath)) or ('Description'+ndf.lower() in os.listdir(ResultBiblioPath)): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
            ficBrevet = LoadBiblioFile(ResultBiblioPath, ndf)

        else: #Retrocompatibility
            print('gather your data again. sorry')
            sys.exit()

        if 'brevets' in ficBrevet:
            lstBrevet = ficBrevet['brevets']
    #        if data.has_key('requete'):
    #            DataBrevet['requete'] = data["requete"]
            print("Found ",typeSrc, ' file and', len(lstBrevet), " patents! Gathering contents")
        else:
            print('gather your data again')
            sys.exit()

        ops_client = epo_ops.Client(key, secret)
        #        data = ops_client.family('publication', , 'biblio')
        ops_client.accept_type = 'application/json'
        BiblioPatents = []
        #making the directory saving patents

        RepDir = ResultPathContent
        try:
            for directory in ['Abstract', 'Claims', 'Description']:
                if directory not in os.listdir(RepDir):
                    os.makedirs(RepDir+"//"+directory)
                if 'Families'+directory not in os.listdir(RepDir):
                    os.makedirs(RepDir+"//Families"+directory)
        except:
            pass
        #os.chdir(ndf.replace('.dump', ''))
        desc, clm, ft, abstract = 0,0,0, 0
        Langues = set()

        if GatherContent:
            Nombre = dict()
            for brevet in lstBrevet:
                brevet = dictCleaner(brevet)
                ndb = brevet['label']#[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$']brevet['publication-ref'][u'document-id'][0][u'kind']['$'])
                print("Retrieving ", ndb)
        #check for already gathered patents
                pays = brevet['country']
                if isinstance(ndb, list):
                    print(ndb, "using first one...")
                    ndb = ndb[0]
                    for key in ['label', 'country', 'kind']:
                        brevet[key] = list(set(brevet[key])) # hum some problem (again) in cleaning data within the family gatherer... 22/12/15
                if isinstance(pays, list):
                    pays = pays[0]
                for content in [typeSrc+'Abstract', typeSrc+'Claims',typeSrc+'Description']:

                    if content not in list(Nombre.keys()):
                        Nombre [content] = 0
                    try:
                        lstfic = os.listdir(ResultPathContent+'//' + content)
                    except:
                        lstfic = []
                    endP= content.replace(typeSrc, "").lower()
                    if endP == 'abstract':
                        endP = 'biblio'
                    fichier = [fics[3:] for fics in lstfic]   # content already gathered
                    if ndb+'.txt' not in fichier: #hack here as chinese patents seems not be in claims or description endpoint
                    #, u'fulltext'
                        temp =('publication', Epodoc(pays+ndb[2:])) #, brevet[u'document-id'][u'kind']['$']))
                        try:
                            data = ops_client.published_data(*temp, endpoint = endP)             #ops_client.published_data()
                            if data.ok and content.replace(typeSrc, "").lower() in str(data.json()):
                                CheckDocDB = False
                            else:
                                CheckDocDB = True
                        except Exception as err:
                            CheckDocDB = True
                        if CheckDocDB:
                            if isinstance(brevet['kind'], list):
                                tempoData = []
                                for cc in brevet['kind']:
                                    temp =('publication', Docdb(ndb[2:],pays, cc)) # hope all comes from same country
                                    try:
                                        tempoData.append(ops_client.published_data(*temp, endpoint = endP))
                                    except:
                                        data = None
                                        pass
                                for dat in tempoData:
                                    if dat is not None and dat.ok: #doing the same for all content. This may result in redundancy
                                        contenu = content.replace(typeSrc, "")

                                        patentCont = dat.json()
                                        Langs = MakeIram2(brevet, ndb +'.txt', patentCont, RepDir+ '//'+ typeSrc + contenu+'//', contenu)
                                        if endP == 'biblio':
                                            for contenu in ['Claims', 'Description']:
                                                Langs = MakeIram2(brevet, ndb +'.txt', patentCont, RepDir+ '//'+ typeSrc + contenu+'//', contenu)
                            else:
                                temp =('publication', Docdb(brevet['label'][2:],brevet['country'], brevet['kind']))
                                try:
                                    data = ops_client.published_data(*temp, endpoint = endP)
                                except:
                                    data = None
                                    pass
                            #OPS limitation ?
                            #OPS includes character-coded full text only for EP, WO, AT, CH, CA, GB and ES.
                            #http://forums.epo.org/open-patent-services-and-publication-server-web-service/topic3728.html



                        if data is not None and data.ok:
                            contenu = content.replace(typeSrc, "")

                            patentCont = data.json()
                            Langs = MakeIram2(brevet, ndb +'.txt', patentCont, RepDir+ '//'+ typeSrc + contenu+'//', contenu)
                            if endP == 'biblio':
                                for contenu in ['Claims', 'Description']:
                                    Langs = MakeIram2(brevet, ndb +'.txt', patentCont, RepDir+ '//'+ typeSrc + contenu+'//', contenu)
                                    #Lang is unused. Trying to gather in biblio endpoint, just in case....


                                # Next line is for setting analyses variables for Iramuteq....

        else:
            print("no gather parameter set. Finishing.")



        #print ft, " fulltext gathered. See ", ndf.replace('.dump', '')+'/fulltext/ directory for files'
