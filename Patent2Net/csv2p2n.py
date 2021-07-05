# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 08:48:20 2020

csv to patent list uin P2N format.


@author: david
"""


from Patent2Net.P2N_Config import LoadConfig
from Patent2Net.P2N_Lib_Acad import  Nettoie, NoPunct
# import bs4
from Patent2Net.P2N_Lib import LoadBiblioFile
from Patent2Net.app import csv
import sys, os
import pickle
import codecs

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

key = "Publication number"

df = csv.read_from_request_field(requete)
    
print("loading csv file. Using '" + key + " column'")
lstNum = list(set(df [key].tolist()))
nbTrouves = len(lstNum)
print ('Found: ', len(df [key].tolist()), "  patents.")

print ("Finally, unique patents :", nbTrouves)
print ('saving')

if ndf not in os.listdir('../Data/'):
    os.makedir('../Data/' + ndf)
    os.makedir(ResultListPath)    
    os.makedir(ResultBiblioPath)   
lstBrevets = []
for pat in lstNum:
    print(pat)
    brevet = dict()
    brevet['document-id'] =  dict()
    brevet['document-id']['country'] =  dict()
    brevet['document-id']['doc-number'] =  dict()
    brevet['document-id']['kind'] =  dict()

    
    brevet['document-id']['country']['$'] = pat[0:2]
    if pat [-2].isalpha():
        kind = pat [-2:]
        brevet['document-id']['doc-number']['$'] = pat [2:-2]
    else:
        kind = pat [-1:]
        brevet['document-id']['doc-number']['$'] = pat [2:-1]
    brevet['document-id']['kind']['$'] = kind
    lstBrevets.append(brevet) 
    
with open(ResultListPath + '//' + ndf, 'wb') as ficRes1:
    DataBrevets = dict()  # this is the list of patents, same variable name as description and patent data in the following
    # this may cause problem sometime
    DataBrevets['brevets'] = lstBrevets
    DataBrevets['number'] = nbTrouves
    DataBrevets['requete'] = requete

    print(DataBrevets)

    pickle.dump(DataBrevets, ficRes1)

print("Done. Please use p2n with same request.cql file to gather patents.")

with codecs.open('..//DATA//lentille//PatentLists//lentille', 'rb') as fic2:
    lentille = pickle.load(fic2)
    print(lentille)