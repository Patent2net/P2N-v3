# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 07:50:48 2015

@author: dreymond
"""

import sys, os
import pickle
from collections import OrderedDict as dict
import epo_ops


os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'
global key
global secret

fic = open('..//cles-epo.txt', 'r')
key, secret = fic.read().split(',')
key, secret = key.strip(), secret.strip()
fic.close()
ops_client = epo_ops.Client(key, secret)
    #        data = ops_client.family('publication', , 'biblio')
ops_client.accept_type = 'application/json'

print("Usage: FusionPatList dir1 dir2 [...] dirN dirResult")

###tout est faux en changeant le modèle de stockage de fichiers
#ListBiblioPath = ['..//DATA//'+ndf1+'//PatentBiblios', '..//DATA//'+ndf2+'//PatentBiblios']
#ResultListPath = ['..//DATA//'+ndf1+'//PatentLists', '..//DATA//'+ndf2+'//PatentLists']#List
#ListContentPath = ['..//DATA//'+ndf1+'//PatentContents', '..//DATA//'+ndf2+'//PatentContents']

data = dict()
import copy
def BrevetFusion(Brevet1, Brevet2):
    BrevetFusion = copy.copy(Brevet1)
    BrevetFusion.extend(Brevet2)
    return BrevetFusion

#lstReq = [subFolders for root, subFolders, files in os.walk('..//DATA//')]
if len(sys.argv)>3:
    lstReq = sys.argv[1:len(sys.argv)-1]
    res = sys.argv[len(sys.argv)-1]

else:
    lstReq = [subFolders for root, subFolders, files in os.walk('..//DATA//')]
    res = "Fusion"
ResultFolder = '..//DATA//'+res
ResultFolderWin = '..\\DATA\\'+res
try:
    os.makedirs(ResultFolder+'//PatentLists')
except:
    if res.title() in lstReq:
        lstReq[0].remove(res.title())
    pass
lig= ""
BrevetRes = dict()
BrevetRes["brevets"] = []
BrevetRes["number"] =0
BrevetRes["requete"] = ''
with open(ResultFolder+'//PatentLists/'+res, 'wb') as ficRes:
    for ndf in lstReq:
        lstBrevets2, nbTrouves = [], 0
        if ndf in os.listdir('..//DATA//') and ndf in os.listdir('..//DATA//'+ndf+'//PatentLists//'):
            with open('..//DATA//'+ndf+'//PatentLists//'+ndf, 'rb') as fic:
                Brevet1 = pickle.load(fic)
                print("Doing ", ndf, "Found ", len(Brevet1 ["brevets"]), "patents in list")

        BrevetRes["brevets"] = BrevetFusion(Brevet1["brevets"], BrevetRes["brevets"])
        BrevetRes["number"] = len(BrevetRes["brevets"])
        if len(BrevetRes["requete"])>0:
            BrevetRes["requete"] = Brevet1["requete"] + " UNION " + BrevetRes["requete"]
        else:
            BrevetRes["requete"] = Brevet1["requete"]

    pickle.dump(BrevetRes, ficRes)

    print("Fusion done. Total in list: ", BrevetRes["number"])
    

with open('..//Fusion'+res +'.txt', 'w', encoding='utf8') as ficSav:
    ficSav.write(BrevetRes["requete"])
print("create requete.cql with ", res, " as dataDirectory and setting GatherPatent to False")
print("Use the following sentence as Request value (writen in Fusion'"+res+".txt file) \n")
print(BrevetRes["requete"])
