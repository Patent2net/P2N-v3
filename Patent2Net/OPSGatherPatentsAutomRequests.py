# -*- coding: utf-8 -*-
"""
Created on Tue Avr 1 13:41:21 2014

@author: dreymond
This script will proccess ALL requests file in RequestAutom directory (processed by AutomRequestSplitter scripts) and gather patent list. 
Fusion script is aimed to be called to merge all PatentListIn one big patent list. That's the way to get around the OPS 2000's patents limit.

This scipt need a consistency control step as for each cql file OPSGather is called and if it fail (network failure) nothing controls that patents are gathered
"""


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

from p2n.util import run_script
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


# by default, data are not gathered yet
# building patentList
nbTrouves = 0
# if GatherPatent:
BiblioPatents, PatIgnored = [], Initialize(GatherPatent, GatherBiblio)

ops_client = epo_ops.Client(key, secret)
#        data = ops_client.family('publication', , 'biblio')
ops_client.accept_type = 'application/json'


nbFiles =  len(os.listdir("../RequestAutom"))
cpt = 0
AnnonceProgres (Appli = 'p2n_req', valMax = nbFiles, valActu = 0)
for conf in os.listdir("../RequestAutom"):
    run_script('OPSGatherPatentsv2.py', configfile="../RequestAutom/"+conf,directory='.')
    cpt += 1
    AnnonceProgres (Appli = 'p2n_req', valMax = nbFiles, valActu = cpt)    
    




#listeLabel = []
# Entering PatentBiblio feeding
AnnonceLog(Appli = 'p2n_gather_biblio', texte= "Checking and/or gathering bibliographic data")
print("Fusion should start now")
