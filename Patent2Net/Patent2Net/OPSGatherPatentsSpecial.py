# -*- coding: utf-8 -*-
"""
Created on Tue Avr 1 13:41:21 2014

@author: dreymond
This script will load the request from file "requete.cql", construct the list
of patents corresponding to this request ans save it to the directorry ../DATA/PatentLists
Then, the bibliographic data associated to each patent in the patent List is collected and
stored to the same file name in the directory ../DATA/PatentBiblio.
"""

# BiblioPropertiesOLD = ['publication-ref', 'priority-active-indicator', 'classification',
#u'resume', 'IPCR1', 'portee', 'IPCR3', 'applicant', 'IPCR4', 'IPCR7', 'label', 'IPCR11',
#'date', 'citations', 'application-ref', 'pays', u'abstract', 'titre', 'inventeur',
#'representative', 'abs' ]
#
#
# BiblioPropertiesOLD2 =  ['applicant', 'application-ref', 'citations', 'classification',
#'inventor', 'IPCR1', 'IPCR11', 'IPCR3', 'IPCR4', 'IPCR7', 'label', 'country', 'kind',
#'priority-active-indicator', 'title','date',"publication-ref","representative",
#"CPC", "prior", "priority-claim", "year", "family-id", "equivalent",
# 'inventor-country', 'applicant-country', 'inventor-nice', 'applicant-nice']

# New in V2... 11/2015
BiblioProperties = ['applicant', 'application-ref', 'citations', 'classification',
                    'prior-Date', 'prior-dateDate'
                    'inventor', 'IPCR1', 'IPCR11', 'IPCR3', 'IPCR4', 'IPCR7', 'label', 'country', 'kind',
                    'priority-active-indicator', 'title', 'date', "publication-ref", "representative",
                    "CPC", "prior", "priority-claim", "year", "family-id", "equivalent",
                    'inventor-country', 'applicant-country', 'inventor-nice', 'applicant-nice', 'CitP', 'CitO', 'references']
#from networkx_functs import *
import pickle
import codecs
# from P2N_Lib import ExtractAbstract, ExtractClassificationSimple2, UniClean, SeparateCountryField, CleanPatent, ExtractPatent, ExtractPubliRefs,
from Patent2Net.P2N_Lib import Initialize, PatentSearch,  GatherPatentsData, LoadBiblioFile, byteify
#from P2N_Lib import ProcessBiblio, MakeIram,  UnNest3, SearchEquiv, PatentCitersSearch
#from P2N_Lib import Update
#from P2N_Lib import EcritContenu, coupeEnMots
from Patent2Net.P2N_Config import LoadConfig
from p2n.config import OPSCredentials
import datetime
import epo_ops
import os
import sys
#from epo_ops.models import Docdb
#from epo_ops.models import Epodoc
os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'
global key
global secret

# put your credential from epo client in this file...
# chargement clés de client
c = OPSCredentials(credentials_file='../cles-epo.txt')
key, secret = c.read()

DureeBrevet = 20
SchemeVersion = '20140101'  # for the url to the classification scheme
import os

ListeBrevet = []  # LA iste de brevets
# ouverture fichier de travail

ficOk = False
cptNotFound = 0
nbTrouves = 0

lstBrevets = []  # The patent List
BiblioPatents = []  # The bibliographic data


#configFile = LoadConfig()
requete = "special Brasil"
ndf = "LattesMiss"
GatherBiblio = False#configFile.GatherBiblio
GatherBibli = True #configFile.GatherBiblio
GatherPatent = True #configFile.GatherPatent
GatherFamilly = True #configFile.GatherFamilly

# should set a working dir one upon a time... done it is temporPath
ResultListPath = "LattesMiss"
ResultBiblioPath = "../DATA/LattesMiss/PatentBiblios"#configFile.ResultBiblioPath
ResultContentsPath =  "../DATA/LattesMiss/PatentBiblios" #configFile.ResultContentsPath
temporPath = '../DATA/LattesMiss/tempo' #configFile.temporPath
ResultAbstractPath = '../DATA/LattesMiss/PatentContents/Abstract' #configFile.ResultAbstractPath

with open("internacionais.txt", 'r') as ficSRC:
    data = fic.readlines()

lstPat = []
listeLabel = []
for ligne in data:
    ligne = ligne.split('\t')
    lattesId=col[0]
    Nom = col[1]
    epoId=col[2].replace(' ', '')
    lstPat.append(epoId, Nom, lattesId)
    listeLabel.append(epoId)


#listeLabel = []
# Entering PatentBiblio feeding
print("Checking and/or gathering bibliographic data")

#    except:    #new data model
#        DataBrevets = dict()
#        DataBrevets['brevets'] = []
#        if ndf in os.listdir(ResultBiblioPath+'//'):
#            with open(ResultBiblioPath+'//'+ndf, 'r') as fic:
#                while 1:
#                    try:
#                        DataBrevets['brevets'].append(cPickle.load(fic))
#                    except EOFError:
#                        break
#            with open(ResultBiblioPath+'//Description'+ndf, 'r') as fic:
#                Descript = cPickle.load(fic)
#                DataBrevets['ficBrevets'] = Descript['ficBrevets']
#                DataBrevets['requete'] =  Descript['requete']
#            if len(DataBrevets['brevets']) == len(lstBrevets):
#                print len(BiblioPatents), " bibliographic patent data gathered yet? Nothing else to do :-)"
#                GatherBibli = False
#                for brevet in DataBrevets['brevets']:
#                    ndb =brevet[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$'] #nameOfPatent for file system save (abstract, claims...)
#                    listeLabel.append(ndb)
#            else:
#                ficOk = False
#                print str(abs(len(DataBrevets['brevets']) - len(BiblioPatents))), "patents data missing. Gathering."
#                GatherBibli = True
#        else:
#            print str(abs(len(lstBrevets))), " patents data missing. Gathering."
#
#            BiblioPatents = [] # gathering all again, I don t know if of serves the same ordered list of patents
#            GatherBibli = True

DataBrevets = dict()


DataBrevets["brevets"]= []
DataBrevets['requete'] =  requete


YetGathered =[]
for brevet in listeLabel:

    try:
        BiblioPatents = GatherPatentsData(
                        brevet, ops_client, ResultContentsPath, ResultAbstractPath,  PatIgnored, [])
    except:
        print(ndb, " ignored... error occured")
                    #some errors coming from OEB inconsistency
        next
                
    # parsing
    if BiblioPatents is None:
        BiblioPatents = []
    else:
        YetGathered.append(brevet)
    tempor = []
    for pat in BiblioPatents:
        if "year" not in list(pat.keys()):  # something didn't go well... Forcing
            if 'date' not in list(pat.keys()) and 'prior-Date' not in list(pat.keys()) and 'dateDate' not in list(pat.keys()) and 'prior-dateDate' not in list(pat.keys()):
                pat['date'] = ['1-1-1']
                pat['prior-Date'] = ['1-1-1']
                pat['dateDate'] = datetime.date(1, 1, 1)
                pat['prior-dateDate'] = datetime.date(1, 1, 1)
                pat['year'] = ['1']
            elif 'date' not in list(pat.keys()) and 'prior-Date' not in list(pat.keys()) and 'dateDate' not in list(pat.keys()):
                if isinstance(pat['prior-dateDate'], list) and len(pat['prior-dateDate']) == 1:
                    if pat['prior-dateDate'][0].year > 1:
                        pat['date'] = [str(pat['prior-dateDate'][0].year) + '-' + str(
                            pat['prior-dateDate'][0].month) + '-' + str(pat['prior-dateDate'][0].day)]
                        pat['prior-Date'] = pat['date']
                        pat['dateDate'] = pat['prior-dateDate'][0]
                        pat['year'] = [str(pat['prior-dateDate'][0].year)]
                    else:
                        pat['date'] = ['1-1-1']
                        pat['prior-Date'] = ['1-1-1']
                        pat['dateDate'] = datetime.date(1, 1, 1)
                        pat['prior-dateDate'] = datetime.date(1, 1, 1)
                        pat['year'] = ['1']
                else:  # booring cases, forcing a little hereafter... many case will be good, others less.... need developper here !
                    pat['date'] = ['1-1-1']
                    pat['prior-Date'] = ['1-1-1']
                    pat['dateDate'] = datetime.date(1, 1, 1)
                    pat['prior-dateDate'] = datetime.date(1, 1, 1)
                    pat['year'] = ['1']

            elif 'dateDate' not in list(pat.keys()):
                pat['date'] = ['1-1-1']
                pat['prior-Date'] = ['1-1-1']
                pat['dateDate'] = datetime.date(1, 1, 1)
                pat['prior-dateDate'] = datetime.date(1, 1, 1)
                pat['year'] = ['1']

            else:
                pat['date'] = ['1-1-1']
                pat['prior-Date'] = ['1-1-1']
                pat['dateDate'] = datetime.date(1, 1, 1)
                pat['prior-dateDate'] = datetime.date(1, 1, 1)
                pat['year'] = ['1']

        tempor.append(pat)
    BiblioPatents = tempor
    if BiblioPatents is not None and BiblioPatents != []:
        with open(ResultBiblioPath + '//' + ndf, 'ab') as ficRes:
            pickle.dump(BiblioPatents[0], ficRes)
            YetGathered.append(BiblioPatents[0]["label"])
            print(len(YetGathered), " patent bibliographic data already gathered.")
    else:
        # may should put current ndb in YetGathered...
        # print
        pass
#
    with open(ResultBiblioPath + '//Description' + ndf, 'wb') as ficRes:
        DataBrevets['ficBrevets'] = ndf
        DataBrevets['requete'] = requete
        DataBrevets["YetGathered"] = YetGathered
        DataBrevets.pop("brevets")
        pickle.dump(DataBrevets, ficRes)

    NotGathered = [pat for pat in listeLabel if pat not in YetGathered]
    print("Ignored  patents from patent list", PatIgnored)
    print("unconsistent patents: ", len(NotGathered))
    print("here is the list: ", " DATA\PatentContentHTML\\" + ndf)

    print("Export in HTML using FormateExport")
else:
    print("Nothing to do, fine!")
#os.system("FormateExport.exe "+ndf)
#os.system("CartographyCountry.exe "+ndf)
