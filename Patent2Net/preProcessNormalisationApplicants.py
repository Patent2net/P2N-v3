# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

@author: dreymond
"""

import datetime
import os
import sys

import pandas as pd

from Patent2Net.P2N_Config import LoadConfig
# import bs4
from Patent2Net.P2N_Lib import LoadBiblioFile

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
if 'Description' + ndf in os.listdir(ListBiblioPath):
    with open(ListBiblioPath + '//' + ndf, 'r') as data:
        dico = LoadBiblioFile(ListBiblioPath, ndf)
else:  # Retrocompatibility
    print("please use Comptatibilizer")
    sys.exit()
LstBrevet = dico['brevets']

# Lecture du fichier de référence
df = pd.read_csv('../Patent2Net/Resources/20200203_STAN.csv', sep=';', encoding='utf-8')

for brev in LstBrevet:
    # ici tu as accès au contenu d'un brevet.
    # le champ qui interesse c'est ['applicant']
    temp = brev['applicant']
    for appli in temp:
        for index, ligne in df.iterrows():
            if appli in ligne['Variation Name']:
                tempo = ligne['univ'].index(appli)
            else:
                pass

    # sauvegarde dans un fichier tempo
    # with open(ResultBiblioPath + '//tempo' + ndf, 'ab') as ficRes:
    # pickle.dump(brev, ficRes)


# remplacement de la source par le résultat
# à n'activer que quand çà marche ^_^
# os.remove(ResultBiblioPath + '//' + ndf)
# shutil.move(ResultBiblioPath + '//tempo' + ndf, ResultBiblioPath + '//' + ndf)