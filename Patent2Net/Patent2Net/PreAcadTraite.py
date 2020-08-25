# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 07:41:54 2019
OLD STUFF DO NOT USE

@author: dreymond
"""


import codecs
import os, sys
import pickle

from pymed import PubMed

from Patent2Net.P2N_Lib import LoadBiblioFile
from Patent2Net.P2N_Config import LoadConfig
from Patent2Net.P2N_Lib_Acad import IPCCategorizer, IPCExtractPredictionBrevet,PubMedCheckNameAndGetAffiliation, OPSChercheAbstractBrevet
from fuzzywuzzy import fuzz

from tqdm import tqdm
import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
import pandas as pd
import string
import re
import unidecode
from tqdm import tqdm
#table = string.maketrans("","")


xlsx = pd.ExcelFile('./Resources/EntitésPubliques.xlsx')
Public = []
TypeAppl = dict()
df = pd.read_csv('../Patent2Net/Resources/STANNorm.csv', dtype=str, sep=';', encoding='utf-8')

    
for sheet in xlsx.sheet_names:
   dicotemp = xlsx.parse(sheet).to_dict(orient='list')
   
   for cle, val in dicotemp.items():
        tempoRes = []
        with tqdm(total=len(val), desc="computing", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
        
            for appli in val:
                pbar.update(1)
                #sav = appli
                # appli = unidecode.unidecode(appli)
                # appli= appli.upper()
                # appli = NoPunct(appli)
                
                # appli = appli.replace('  ', ' ')
                # appli = appli.replace('  ', ' ')
               
                #try
                # indx = df.index[df['Variation Name']== appli]
                # if len(indx)>0:
                #     joliNom = df['Norm'].iloc[indx].to_list()[0]
                #     tempoRes.append(joliNom)
                    
                # else:
                #     print (appli)
                tempoRes.append(appli)
            TypeAppl [cle] = tempoRes
            Public.extend(tempoRes)
       
       




print (len(df))
configFile = LoadConfig()
# Les champs nécessaires par brevet.
NeededInfo = ['label', 'date', 'inventor', 'title', 'abstract']

requete = configFile.requete
projectName = configFile.ndf
ndf = projectName
BiblioPath = configFile.ResultBiblioPath
ResultBiblioPath = configFile.ResultBiblioPath
temporPath = configFile.temporPath
ResultPathContent= configFile.ResultContentsPath
ResultAbstractPath = configFile.ResultAbstractPath
Auteur = configFile.ResultPath + '//AcadCorpora'
RepDir = configFile.ResultPath + '//AcadCorpora'
project = RepDir

print("\n> Hi! This is Pre Process for normalizing applicant names: used on:", ndf)
if 'Description' + ndf in os.listdir(ListBiblioPath):
    with open(ListBiblioPath + '//' + ndf, 'r') as data:
        dico = LoadBiblioFile(ListBiblioPath, ndf)
else:  # Retrocompatibility
    print("please use Comptatibilizer")
    sys.exit()
LstBrevet = dico['brevets']

Applis = []
for bre in LstBrevet:
    for appli in bre["applicant"]:
        Applis.append(appli)
        
# with tqdm(total=len(set(Public)), desc="computing", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:

#     for brev in set(Public):
# #        pbar.update(1)
#         indx = df.index[df['Variation Name'] == brev] | df.index[df['Norm'] == brev]
#         if len(indx)==0:
#             indx = df.index[df['Variation Name'] == brev.upper()] | df.index[df['Norm'] == brev.upper()]
#             if len(indx)==0:
#                 print (brev)
            

# test de consistance
with open(Auteur+'//DejaTraites.csv', 'r',) as fic:
    DejaVus = fic.readlines()

if len (set(DejaVus)) == len(DataBrevet['brevets']):
    print ('Youhou, tous les brevets ' + ndf + ' ont été traités.')
    print ('Nb de brevets : ', len(DataBrevet['brevets']))
    
else:
    reste = [bre['label'] for bre in DataBrevet['brevets'] if bre['label'] not in DejaVus ]
    print ('il reste ', len(reste), ' brevets à traiter')
 
# Analyse stat des résultats

