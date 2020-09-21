# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 10:44:06 2020

@author: david
"""
from Patent2Net.P2N_Lib import LoadBiblioFile, AnnonceProgres
from Patent2Net.P2N_Config import LoadConfig
import os

configFile = LoadConfig()
requete = configFile.requete
projectName = configFile.ndf
Gather = configFile.GatherContent
GatherBiblio = configFile.GatherBiblio
GatherPatent = configFile.GatherPatent
GatherFamilly = configFile.GatherFamilly
ResultPath = configFile.ResultBiblioPath
ndf = configFile.ndf


print("loading data file ", ndf+' from ', ResultPath, " directory.")
if 'Description'+ndf in os.listdir(ResultPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
    data1 = LoadBiblioFile(ResultPath, ndf)


ResultPath = ResultPath.replace('DATA/', 'DATA/OLD/')

if 'Description'+ndf in os.listdir(ResultPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
    data2 = LoadBiblioFile(ResultPath, ndf)


dataB1 =data1['brevets']

dataB2 =data2['brevets']

labB1 = [bre['label'] for bre in dataB1]

labB2 = [bre['label'] for bre in dataB2]
print(len(labB1))
print(len(labB2))

trucs = [lab for lab in labB2 if lab not in labB1]
trucs2 = [lab for lab in labB1 if lab not in labB2]