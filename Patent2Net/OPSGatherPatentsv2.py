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
from Patent2Net.P2N_Lib import Initialize, PatentSearch,  GatherPatentsData, LoadBiblioFile, byteify, AnnonceProgres, AnnonceLog
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


ListeBrevet = []  # LA iste de brevets
# ouverture fichier de travail

ficOk = False
cptNotFound = 0
nbTrouves = 0

lstBrevets = []  # The patent List
BiblioPatents = []  # The bibliographic data


configFile = LoadConfig()
requete = configFile.requete
ndf = configFile.ndf
GatherBiblio = configFile.GatherBiblio
GatherBibli = configFile.GatherBiblio
GatherPatent = configFile.GatherPatent
GatherFamilly = configFile.GatherFamilly

# should set a working dir one upon a time... done it is temporPath
ResultListPath = configFile.ResultListPath
ResultBiblioPath = configFile.ResultBiblioPath
ResultContentsPath = configFile.ResultContentsPath
temporPath = configFile.temporPath
ResultAbstractPath = configFile.ResultAbstractPath

Fusion = False # switch for fusion
# by default, data are not gathered yet
# building patentList
nbTrouves = 0
# if GatherPatent:
BiblioPatents, PatIgnored = [], Initialize(GatherPatent, GatherBiblio)

ops_client = epo_ops.Client(key, secret)
#        data = ops_client.family('publication', , 'biblio')
ops_client.accept_type = 'application/json'

AnnonceLog(Appli = 'p2n_gather_biblio', texte= "Starting gathering patent list for request:" + requete )
if ndf in os.listdir(ResultListPath):
    with codecs.open(ResultListPath + '//' + ndf, 'rb') as fic:
        DataBrevets = pickle.load(fic)
        lstBrevets = DataBrevets['brevets']
        nbActus = DataBrevets['number']
        if 'fusion' in DataBrevets.keys():
            ficOk = True
            print(nbActus, " patents gathered yet. No more patents to retreive. Steping to bibliographic data.")
            AnnonceLog(Appli = 'p2n_req', texte='Gather patent (fusion)' + str(nbActus) +" patents gathered yet. No more patents to retreive. Steping to bibliographic data.")
            AnnonceProgres (Appli = 'p2n_req', valMax = 100, valActu =100)
            GatherBibli = False
            requete = DataBrevets['brevets']
            Fusion = True
        if 'FusionPat' in DataBrevets.keys():
            ficOk = True
            print(nbActus, " patents list gathered yet. Steping to bibliographic data.")
            AnnonceLog(Appli = 'p2n_req', texte= 'Gather patent (fusion patentlist ?)' + str(nbActus) +" patents gathered yet. No more patents to retreive. Steping to bibliographic data.")
            AnnonceProgres (Appli = 'p2n_req', valMax = 100, valActu =100)
            GatherPatent = False
            Gatherbibli = False
            requete = DataBrevets['brevets']
            Fusion = True
        if GatherPatent:  # Patent List to build from request. 
            if DataBrevets['requete'] != requete:
                AnnonceLog(Appli = 'p2n_req', texte=  'Gather patent' +" Datadirectory exists. Deleting it.")

                print("care of using on file for one request, deleting this one.")
                input('sure? Unlee use ^C ( CTRL+C)')
            lstBrevets2, nbTrouves = PatentSearch(ops_client, requete)
            if len(lstBrevets2) == nbTrouves and nbActus != nbTrouves:
                ficOk = True
                print(nbTrouves, " patents gathered yet. No more patents to retreive. Steping to bibliographic data.")
                AnnonceLog(Appli = 'p2n_req', texte=  str(nbTrouves) + " patents gathered yet. No more patents to retreive. Steping to bibliographic data.")
                AnnonceProgres (Appli = 'p2n_req', valMax = 100, valActu = 100)
                Gatherbibli = True
                GatherPatent = False
            elif len(lstBrevets) == nbTrouves and nbActus == nbTrouves:
                Gatherbibli = False
                GatherPatent = False
                DataB =dict()
                with open(ResultBiblioPath + '//Description' + ndf, 'wb') as ficRes:
                        DataB['ficBrevets'] = ndf
                        DataB['requete'] = requete
                        DataB["YetGathered"] = nbActus
                        
                        pickle.dump(DataB, ficRes)
                print('Checking bibliographic data')
                AnnonceLog(Appli = 'p2n_req', texte= " Checking bibliographic data.")
                AnnonceProgres (Appli = 'p2n_req', valMax = 100, valActu = 100)
                #we should exit now
            else:
                ficOk = False
                print(nbTrouves, " patents corresponding to the request.")
                AnnonceLog(Appli = 'p2n_req', texte=  str(nbTrouves) + "  patents corresponding to the request.  Retreiving associated bibliographic data")
                AnnonceProgres (Appli = 'p2n_req', valMax = 100, valActu = 100)
                print(len(lstBrevets), ' in file corresponding to the request. Retreiving associated bibliographic data')
        else:
            AnnonceProgres (Appli = 'p2n_req', valMax = 100, valActu =100)
            print("Stepping to bibliographic data gathering")
else:
    lstBrevets = []  # gathering all again, I don t know if of serves the same ordered list of patents
    ficOk = False        
    nbTrouves = 1
#except:
#    try:
#
#        lstBrevets = LoadBiblioFile(ResultBiblioPath, ndf)
#        nbActus = len(lstBrevets)
#        ficOk = True
#
#    except:
#        lstBrevets = []  # gathering all again, I don t know if of serves the same ordered list of patents
#        ficOknd = False
#        nbTrouves = 1
STOP = False
# else:
#
#    print "Good, nothing to do"

AnnonceProgres (Appli = 'p2n_req', valMax = 100, valActu = 0)
if not ficOk and GatherPatent:
    ajouts = 0
    while len(lstBrevets) < nbTrouves and not STOP:
        if len(lstBrevets) + 25 < 2000:
            temp,  nbTrouves = PatentSearch(
                ops_client, requete, len(lstBrevets) + 1, len(lstBrevets) + 25)
            
        else:
            temp,  nbTrouves = PatentSearch(ops_client, requete, len(
                lstBrevets) - 25, 2000)  # hum should gather twice here
            if 'ajouts' not in locals():
                ajouts = 0
            STOP = True
        for p in temp:
            if p not in lstBrevets:

                lstBrevets.append(p)
                ajouts += 1

        if ajouts == 0:
            STOP = True
            print("too many similar previous matches. Exciting")
            #•AnnonceProgres (Appli = 'p2n_req', valMax = 100, valActu = temp)
        # cos.system('cls')
        print(nbTrouves, " patents corresponding to the request.")
        print(len(lstBrevets), ' patents added', end=' ')
        AnnonceProgres (Appli = 'p2n_req', valMax = 100, valActu =100)
        AnnonceLog(Appli = 'p2n_req', texte=   str(len(lstBrevets)) + "  patents retreived. Saving")
                
    with open(ResultListPath + '//' + ndf, 'wb') as ficRes1:
        DataBrevets = dict()  # this is the list of patents, same variable name as description and patent data in the following
        # this may cause problem sometime
        DataBrevets['brevets'] = lstBrevets
        DataBrevets['number'] = nbTrouves
        DataBrevets['requete'] = requete
        pickle.dump(DataBrevets, ficRes1)
listeLabel = []


#listeLabel = []
# Entering PatentBiblio feeding
AnnonceLog(Appli = 'p2n_gather_biblio', texte= "Checking and/or gathering bibliographic data")
print("Checking and/or gathering bibliographic data")
if GatherBiblio:
    for brevet in lstBrevets:
        # nameOfPatent for file system save (abstract, claims...)
        ndb = brevet['document-id']['country']['$'] + brevet['document-id']['doc-number']['$']
        listeLabel.append(ndb)

AnnonceLog(Appli = 'p2n_gather_biblio', texte= "Found almost" + str(len(lstBrevets)) + " patents. Saving list")
AnnonceLog(Appli = 'p2n_gather_biblio', texte="Within " + str(len(set(listeLabel))) + " unique patents")
print("Found almost", len(lstBrevets), " patents. Saving list")
print("Within ", len(set(listeLabel)), " unique patents")
BibliDataBrevets = dict()
BibliDataBrevets['brevets'] = []
    
# loading already gathered bibliographic daata
if ndf in os.listdir(ResultBiblioPath):
    BibliDataBrevets = LoadBiblioFile(ResultBiblioPath, ndf)
#        with codecs.open(ResultBiblioPath + '//' + ndf, 'rb', "utf-8") as fic:
#            while 1:
#                try:
#                    DataBrevets['brevets'].append(byteify(pickle.load(fic)))
#                except EOFError:
#                    break

    if len(BibliDataBrevets['brevets']) == len(listeLabel):
            print(len(BibliDataBrevets['brevets']), " bibliographic patent data gathered yet? ")
            GatherBibli = False
            
            AnnonceProgres (Appli = 'p2n_gather_biblio', valMax = 100, valActu = 100)
            sys.exit('Nothing else to do :-). Good bye')
    else:
        print(len(listeLabel)-len(BibliDataBrevets['brevets']), " patent misssing... processing")
 
        GatherBibli = True
        AnnonceProgres (Appli = 'p2n_gather_biblio', valMax = 100, valActu = 100 * len(BibliDataBrevets['brevets'])/len(listeLabel))
#                for brevet in lstBrevets:
#                    # nameOfPatent for file system save (abstract, claims...)
#                    ndb = brevet['document-id']['country']['$'] + \
#                        brevet['document-id']['doc-number']['$']
#                    listeLabel.append(ndb)
else:
    ficOk = False
    print(str(abs(len(listeLabel) - len(BibliDataBrevets['brevets']))), " patents data missing. Gathering.")
    GatherBibli = True
    AnnonceProgres (Appli = 'p2n_gather_biblio', valMax = 100, valActu = 100 * len(BibliDataBrevets['brevets'])/len(listeLabel))
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
PatIgnored = 0


if Fusion or (GatherBibli and GatherBiblio):
    ops_client = epo_ops.Client(key, secret)
    # This step is unclear at this time. 
    # p2n should firt gather the patent list, then gather all bibliographic data for each patent in list
    # add a consistency step would be nice also....
    
    ops_client.accept_type = 'application/json'
    
    if "brevets" in list(BibliDataBrevets.keys()):
        YetGathered = list(set([bre['label'] for bre in BibliDataBrevets ['brevets']]))
        print(len(YetGathered), " patent bibliographic data gathered.")
        AnnonceLog(Appli = 'p2n_gather_biblio', texte= str(len(YetGathered)) + " patent bibliographic data gathered.")
        BibliDataBrevets["YetGathered"] = YetGathered

        AnnonceProgres (Appli = 'p2n_gather_biblio', valMax = 100, valActu = len(YetGathered)*100/len(listeLabel))
    else:
        YetGathered = []

    for brevet in lstBrevets:

        # may be current patent has already be gathered in a previous attempt
        # should add a condition here to check in os.listdir()
        if 'invalid result' not in str(brevet) and 'document-id' in list(brevet.keys()):
            # nameOfPatent for file system save (abstract, claims...)
            ndb = brevet['document-id']['country']['$'] + \
                brevet['document-id']['doc-number']['$']
#            listeLabel.append(ndb)
            if ndb not in YetGathered:
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
                        AnnonceProgres (Appli = 'p2n_gather_biblio', valMax = 100, valActu = 100*len(YetGathered)/len(listeLabel))
                else:
                    # may should put current ndb in YetGathered...
                    # print
                    pass
    #
            else:
                pass  # yet gathered
        else:
            print("invalid result")
            if 'label' in list(brevet.keys()):
                if brevet['label'] not in YetGathered:
                    with open(ResultBiblioPath + '//' + ndf, 'ab') as ficRes:

                        pickle.dump(brevet, ficRes)
                        YetGathered.append(brevet["label"])
                        print(len(YetGathered), " patent bibliographic data gathered.")
                        AnnonceProgres (Appli = 'p2n_gather_biblio', valMax = 100, valActu = 100*len(YetGathered)/len(listeLabel))
                else:
                    pass  # bad OPS entry
    with open(ResultBiblioPath + '//Description' + ndf, 'wb') as ficRes:
        DataBrevets['ficBrevets'] = ndf
        DataBrevets['requete'] = requete
        DataBrevets["YetGathered"] = YetGathered
        DataBrevets.pop("brevets")
        pickle.dump(DataBrevets, ficRes)

    NotGathered = [pat for pat in listeLabel if pat not in YetGathered]
    AnnonceLog(Appli = 'p2n_gather_biblio', texte="""Ignored  patents from patent list: """ +str(PatIgnored))  
    
    AnnonceLog(Appli = 'p2n_gather_biblio', texte=""" unconsistent patents: """ +str(len(NotGathered))) 
                        
                        
    print("Ignored  patents from patent list", PatIgnored)
    print("unconsistent patents: ", len(NotGathered))
    print("here is the list: ", " DATA\PatentContentHTML\\" + ndf)

    print("Export in HTML using FormateExport")
else:
    print("Nothing to do, fine!")
    AnnonceProgres (Appli = 'p2n_gather_biblio', valMax = 100, valActu = 100)
    AnnonceLog(Appli = 'p2n_gather_biblio', texte="""Nothing else to do, fine!""") 

#os.system("FormateExport.exe "+ndf)
#os.system("CartographyCountry.exe "+ndf)
