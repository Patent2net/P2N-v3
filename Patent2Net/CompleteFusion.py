# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 07:50:48 2015

Same purpose as FusionPatentList2 which is limited to patentlist.
This script pushes up to the patent bibliographic data and the contents
@author: dreymond
"""

import sys, os
import pickle
from collections import OrderedDict as dict
import epo_ops


os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'
global key
global secret
from Patent2Net.P2N_Lib import LoadBiblioFile

fic = open('..//cles-epo.txt', 'r')
key, secret = fic.read().split(',')
key, secret = key.strip(), secret.strip()
fic.close()
ops_client = epo_ops.Client(key, secret)
    #        data = ops_client.family('publication', , 'biblio')
ops_client.accept_type = 'application/json'

print("""Usage: CompleteFusion dir1 dir2 [...] dirN dirResult
                  Or : CompleteFusion
                  without parameters the script will proceed to the fusion 
                  of ALL directories in the DATA directory to a new one named Fusion""")

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

lstReq =lstReq[0] #first level is enought
#fusion of Patent Lists
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
print("Patent List fusion done. Total patents in Fusion list: ", BrevetRes["number"])    
YetGathered = []
#fusion of Patent Bibliographic Data
BiblioRes = dict()
BiblioRes["brevets"] = []
BiblioRes["number"] =0
BiblioRes["requete"] = ''
try:
    os.makedirs(ResultFolder+'//PatentBiblios')
except:
    if res.title() in lstReq:
        lstReq[0].remove(res.title())
    pass

#biblioFiles
for ndf in lstReq:
    lstBrevets2, nbTrouves = [], 0
    if ndf in os.listdir('..//DATA//') and ndf in os.listdir('..//DATA//'+ndf+'//PatentBiblios//'):
        Brevet1 = LoadBiblioFile('..//DATA//'+ndf+'//PatentBiblios//',ndf)
        print("Doing ", ndf, "Found ", len(Brevet1["brevets"]), "patents in list")

    BiblioRes["brevets"] = BrevetFusion(Brevet1["brevets"], BiblioRes["brevets"])
    BiblioRes["number"] = len(BiblioRes["brevets"])
    if len(BiblioRes["requete"])>0:
        BiblioRes["requete"] = Brevet1["requete"] + " UNION " + BiblioRes["requete"]
    else:
        BiblioRes["requete"] = Brevet1["requete"]


for brevet in BiblioRes ["brevets"]:
     with open(ResultFolder+'//PatentBiblios//'+res, 'ab') as ficRes:
         pickle.dump(brevet, ficRes)
         YetGathered.append(brevet["label"])

DataBrevets =dict()         
with open(ResultFolder+'//PatentBiblios//Description' + res, 'wb') as ficRes:
        DataBrevets['ficBrevets'] = res
        DataBrevets['requete'] = BiblioRes["requete"] 
        DataBrevets["YetGathered"] = YetGathered
        pickle.dump(DataBrevets, ficRes)
print("Patent bibliographic data fusion done. Total bibliographics data in Fusion : ", BiblioRes["number"])    
#families Biblio files
BiblioRes = dict()
BiblioRes["brevets"] = []
BiblioRes["number"] =0
BiblioRes["requete"] = ''      
for ndf in lstReq:
    lstBrevets2, nbTrouves = [], 0
    if ndf in os.listdir('..//DATA//') and ndf in os.listdir('..//DATA//'+ndf+'//PatentBiblios//'):
        Brevet1 = LoadBiblioFile('..//DATA//'+ndf+'//PatentBiblios//','Families'+ndf)
        print("Doing ", 'Families'+ndf, "Found ", len(Brevet1["brevets"]), "patents in list")

    BiblioRes["brevets"] = BrevetFusion(Brevet1["brevets"], BiblioRes["brevets"])
    BiblioRes["number"] = len(BiblioRes["brevets"])
    if len(BiblioRes["requete"])>0:
        BiblioRes["requete"] = Brevet1["requete"] + " UNION " + BiblioRes["requete"]
    else:
        BiblioRes["requete"] = Brevet1["requete"]


for brevet in BiblioRes ["brevets"]:
     with open(ResultFolder+'//PatentBiblios//Families'+res, 'ab') as ficRes:
         pickle.dump(brevet, ficRes)
         YetGathered.append(brevet["label"])

DataBrevets =dict()         
with open(ResultFolder+'//PatentBiblios//FamiliesDescription' + res, 'wb') as ficRes:
        DataBrevets['ficBrevets'] = res
        DataBrevets['requete'] = BiblioRes["requete"] 
        DataBrevets["YetGathered"] = YetGathered
        pickle.dump(DataBrevets, ficRes)


print("Families patent bibliographic data fusion done. Total patents in Families Fusion : ", BiblioRes["number"])    

    

#fusion of Patent content PatentContents ['Abstract', 'Claims', 'Description', 'FamiliesAbstract', 'FamiliesClaims', 'FamiliesDescription']
def GenereListeFichiers(rep):
    """ prend un dossier en paramètre (chemin absolu) et génère la liste
    complète des fichiers TXT et CSV de l'arborescence"""

    listeFicTXT = []

    for ficOuRep in os.listdir(rep):

        if "." not in ficOuRep:
            for fic in os.listdir(rep+'//'+ficOuRep):
                #for fic in os.listdir(root+"//"+sousRep):
               # temporar = GenereListeFichiers(rep+'//'+sousRep)

                         if fic.endswith('.txt'):
                             listeFicTXT.append(rep+"//"+ficOuRep+'//'+fic)
                         else:
                             pass

#                listeFicCSV.extend(temporar[0])
#                listeFicTXT.extend(temporar[1])
#                listeFicUNK.extend(temporar[2])
        else:
           listeFicTXT.append(ficOuRep)
           pass
#                if ficOuRep.endswith('.csv'):
#                    listeFicCSV.append(root+'//'+fichier)
#                elif ficOuRep.endswith('.txt'):
#                    listeFicTXT.append(root+'//'+fichier)
#                else:
#                    pass
                
    return  list(set(listeFicTXT))

from pathlib import Path, PureWindowsPath


lstDir = ['PatentContents//' + rep for rep in ['Abstract', 'Claims', 'Description', 'FamiliesAbstract', 'FamiliesClaims', 'FamiliesDescription']]
lstDir.append('PatentImages')
#create destination directories
os.mkdir(ResultFolder+'//PatentContents')
for rep in lstDir:
    os.mkdir(ResultFolder+'//'+rep)
for ndf in lstReq:
    #lstFic =     GenereListeFichiers('..//DATA//'+ndf+'//' + RepertoireATraiter)
    for RepertoireATraiter in lstDir:
        src = '..//DATA//'+ndf+'//' + RepertoireATraiter+'//' #+fic
        filename = PureWindowsPath(Path(src.replace('/', '\\')))
        dirname =  PureWindowsPath(Path(src.replace('/', '\\')))
        dest = PureWindowsPath(Path(ResultFolder.replace('/', '\\') +'\\'+RepertoireATraiter+'\\'))
        os.system('xcopy /Y /S /Q %s %s' % (dirname, dest))

    print ("All files (Images, Abstract, Claims, Description and families) processed for : ", ndf )    


print("Complete fusion done (Patent list, Bibliographic data and contents).")

    

with open('..//Fusion'+res +'.txt', 'w', encoding='utf8') as ficSav:
    ficSav.write(BrevetRes["requete"])
    
print("create requete.cql with ", res, " as dataDirectory and setting GatherPatent to False")
print("Use the following sentence as Request value (also writen in '"+res+".txt file) \n")
print(BrevetRes["requete"])

print("""Note other files (gephi, carrot etc.) will be obtained by processing P2N on fusioned datadirectory.
       but with ALL GATHERING PARAMETERS to false and All others parameter setted to True""")
