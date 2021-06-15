# -*- coding: utf-8 -*-
"""
Created on May 2020

@author: Romaric Gauzi

Merge script for date split requests.
Pass the request file before the separation as a script parameter
"""

import sys, os
import pickle
import shutil
from collections import OrderedDict as dict
from Patent2Net.P2N_Config import LoadConfig
from Patent2Net.app.data.fusion_list import FusionList
import epo_ops

os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'
global key
global secret


configFile = LoadConfig()
final_ndf = configFile.ndf

fic = open('./cles-epo.txt', 'r')
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
    basepath = './DATA/'
    lstReq = []
    for entry in os.scandir(basepath):
        if entry.is_dir() and (final_ndf + "_segments_") in entry.name:
            lstReq.append(entry.name)
        
    #lstReq = [subFolders for root, subFolders, files in os.walk('..//DATA//')]
    res = final_ndf
ResultFolder = './/DATA//'+res
ResultFolderWin = '.\\DATA\\'+res
try:
    os.makedirs(ResultFolder+'//PatentLists')
except:
    if res.title() in lstReq: # it seems that already a fusion name is here... BAD
        lstReq.remove(res.title())
    pass
lig= ""
BrevetRes = dict()
BrevetRes["brevets"] = []
BrevetRes["number"] =0
BrevetRes["requete"] = ''
BrevetRes["fusion"] = True


print(final_ndf)
print("Other")

fustion_list = FusionList(final_ndf)
fustion_list.start(lstReq, [])

print("test")

with open(ResultFolder+'//PatentLists/'+res, 'wb') as ficRes:
    for ndf in lstReq:
        lstBrevets2, nbTrouves = [], 0
        if ndf in os.listdir('.//DATA//') and ndf in os.listdir('.//DATA//'+ndf+'//PatentLists//'):
            with open('.//DATA//'+ndf+'//PatentLists//'+ndf, 'rb') as fic:
                Brevet1 = pickle.load(fic)
                print("Doing ", ndf, "Found ", len(Brevet1 ["brevets"]), "patents in list")

        BrevetRes["brevets"] = BrevetFusion(Brevet1["brevets"], BrevetRes["brevets"])
        BrevetRes["number"] = len(BrevetRes["brevets"])
        if len(BrevetRes["requete"])>0:
            BrevetRes["requete"] = Brevet1["requete"] + " UNION " + BrevetRes["requete"]
        else:
            BrevetRes["requete"] = Brevet1["requete"]

        fustion_list.add_done(ndf)

    pickle.dump(BrevetRes, ficRes)

    print("Fusion done. Total in list: ", BrevetRes["number"])



with open('.//Fusion'+res +'.txt', 'w', encoding='utf8') as ficSav:
    ficSav.write(BrevetRes["requete"])
print("create requete.cql with ", res, " as dataDirectory and setting GatherPatent to False")
print("Use the following sentence as Request value (writen in Fusion'"+res+".txt file) \n")
print(BrevetRes["requete"])

def get_cql_file_path():
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if ".cql" in arg.lower():
                return arg

source = get_cql_file_path()
destination = source.replace(".cql", "") + "_fusion.cql"

f_in = open(source, "rt")
f_out = open(destination ,"wt")

for name in f_in:
    f_out.write( name.replace('GatherPatent: True', 'GatherPatent: False' ) )

fustion_list.end()
