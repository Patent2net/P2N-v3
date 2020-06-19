# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

@author: dreymond
"""

import json
import os
import sys
#import pickle as pickle
#import bs4
from Patent2Net.P2N_Lib import UrlInventorBuild, UrlApplicantBuild, UrlIPCRBuild, UrlPatent, LoadBiblioFile, RenderTemplate
from Patent2Net.P2N_Config import LoadConfig
import shutil
import datetime
aujourd = datetime.date.today()

configFile = LoadConfig()
requete = configFile.requete
ndf = configFile.ndf
Gather = configFile.GatherContent
GatherBiblio = configFile.GatherBiblio
GatherPatent = configFile.GatherPatent
GatherFamilly = configFile.GatherFamilly
IsEnableScript = configFile.FormateExportDataTable

 #should set a working dir one upon a time... done it is temporPath
ListBiblioPath = configFile.ResultBiblioPath
temporPath = configFile.temporPath
ResultPathContent = configFile.ResultPath

ResultListPath = configFile.ResultListPath
ResultBiblioPath = configFile.ResultBiblioPath

print("\n> Hi! This is Pre Process for normalizing applicant names: used on:", ndf)
if 'Description'+ndf in os.listdir(ListBiblioPath):
    with open(ListBiblioPath+'//'+ndf, 'r') as data:
        dico = LoadBiblioFile(ListBiblioPath, ndf)
else: #Retrocompatibility
    print("please use Comptatibilizer")
    sys.exit()
LstBrevet = dico['brevets']

for brev in LstBrevet:
  
    # ici tu as accès au contenu d'un brevet.
    # le champ qui interesse c'est ['applicant']
    temp = brev ['applicant']
    

    # sauvegarde dans un fichier tempo
    with open(ResultBiblioPath + '//tempo' + ndf, 'ab') as ficRes:
        pickle.dump(brevet, ficRes)


# remplacement de la source par le résultat
# à n'activer que quand çà marche ^_^
# os.remove(ResultBiblioPath + '//' + ndf)
# shutil.move(ResultBiblioPath + '//tempo' + ndf, ResultBiblioPath + '//' + ndf)


