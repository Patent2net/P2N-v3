# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 15:23:13 2020
P2N-Indexer
Beta test: need to fix communication way with carrot.
Need also SSE progress bar and process application.
@author: david
"""

from datetime import datetime
from elasticsearch import Elasticsearch
import json
from Patent2Net.P2N_Lib import LoadBiblioFile, AnnonceProgres
from Patent2Net.P2N_Config import LoadConfig
import os

configFile = LoadConfig()
requete = configFile.requete
ndf = configFile.ndf
Rep = configFile.ResultContentsPath
Bib = configFile.ResultBiblioPath
es = Elasticsearch(hosts=[{'host': "elasticsearch", 'port': 9200}])

if 'Description'+ndf in os.listdir(Bib): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
    DataBrevet = LoadBiblioFile(Bib, ndf)
    LstBrevet = DataBrevet['brevets']
elif 'Description'+ndf.title() in os.listdir(Bib): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
    DataBrevet = LoadBiblioFile(Bib, ndf.title())
    LstBrevet = DataBrevet['brevets']
else: #Retrocompatibility
    print("please use Comptatibilizer")

def GenereListeFichiers(rep):
    """ prend un dossier en paramètre (chemin absolu) et génère la liste
    complète des fichiers TXT de l'arborescence"""
    listeFicFR = []
    listeFicEN = []
    listeFicUNK = []
    for root, subFolders, files in os.walk(rep):

        if len(subFolders)>0:
            for sousRep in subFolders:
                temporar = GenereListeFichiers(rep+'//'+sousRep)
                listeFicFR.extend(temporar[0])
                listeFicEN.extend(temporar[1])
                listeFicUNK.extend(temporar[2])
        else:
            for fichier in files:
                if fichier.endswith('.txt') and fichier.lower().startswith('fr'):
                    listeFicFR.append(root+'//'+fichier)
                elif fichier.endswith('.txt') and fichier.lower().startswith('en'):
                    listeFicEN.append(root+'//'+fichier)
                else:
                    if fichier.endswith('.txt'):
                        listeFicUNK.append(root+'//'+fichier)

    return (list(set(listeFicFR)), list(set(listeFicEN)), list(set(listeFicUNK)))


#lstAbs = os.listdir(Rep+'//Abstract')
#getting labels from file names
lstAbs = [truc.split('-')[1].replace('.txt', '') for truc in os.listdir(Rep+'//Abstract') if '-' in truc] 
lstAbs2 =[truc.replace('.txt', '') for truc in os.listdir(Rep+'//Abstract') if '-' not in truc] 
#lstClaims = os.listdir(Rep+'//Claims')
#getting labels from file names
lstClaims = [truc.split('-')[1].replace('.txt', '') for truc in os.listdir(Rep+'//Claims') if '-' in truc] 

lstClaims2 =[truc.replace('.txt', '') for truc in os.listdir(Rep+'//Claims') if '-' not in truc] 

#lstDesc = os.listdir(Rep+'//Description')
#getting labels from file names
lstDesc = [truc.split('-')[1].replace('.txt', '') for truc in os.listdir(Rep+'//Description') if '-' in truc] 
lstDesc2 =[truc.replace('.txt', '') for truc in os.listdir(Rep+'//Description') if '-' not in truc] 

cpt = 0
for bre in LstBrevet: # get patent list from request file
    cpt +=1
    if bre ['label'] in lstAbs or bre ['label'] in lstAbs2: #if abstract file exists for that label in PatentContent///Abstract
        fic = []
        for truc in  os.listdir(Rep+'//Abstract'):
            if '-' in truc and truc.split('-')[1].replace('.txt', '') == bre ['label']:            
                fic.append(truc)
            elif truc.replace('.txt', '') == bre ['label']:
                 fic.append(truc)
            else:
                pass
        if len(fic) == 1:
            with open(Rep+'/Abstract/' + fic [0], 'r', encoding = 'utf8') as data:
                abstract = data.read()
        elif len(fic) > 1:
            fic = [truc for truc in fic if 'en' in truc] # using english only
            if len(fic)>0:
                with open(Rep+'/Abstract/' + fic [0], 'r', encoding ='utf8') as data:
                    abstract = data.read()
            else:
                 abstract = ''
        else:
             abstract = ''
    else:
        abstract = ''
    if bre ['label'] in lstClaims or bre ['label'] in lstClaims2: # if Claims file exists
        #fic = [truc for truc in  os.listdir(Rep+'//Claims') if truc.split('-')[1].replace('.txt', '') == bre ['label']]
        fic = []
        
        for truc in  os.listdir(Rep+'//Claims'):
            if '-' in truc and truc.split('-')[1].replace('.txt', '') == bre ['label']:            
                 fic.append(truc)
            elif truc.replace('.txt', '') == bre ['label']:
                 fic.append(truc)
            else:
                pass
        
        if len(fic) == 1:
            with open(Rep+'/Claims/' + fic [0], 'r', encoding ='utf8') as data:
                Claims = data.read()
        elif len(fic) > 1:
            fic = [truc for truc in fic if 'en' in truc] # using english only
            if len(fic)>0:
                with open(Rep+'/Claims/' + fic [0], 'r') as data:
                    Claims = data.read()
            else:
                 Claims = ''
        else:
             Claims = ''
    else:
        Claims = ''
    if bre ['label'] in lstDesc or bre ['label'] in lstDesc2: # if Description file exists
        #fic = [truc for truc in  os.listdir(Rep+'//Description') if truc.split('-')[1].replace('.txt', '') == bre ['label']]
        fic = []
        
        for truc in  os.listdir(Rep+'//Description'):
            if '-' in truc and truc.split('-')[1].replace('.txt', '') == bre ['label']:            
                 fic.append(truc)
            elif truc.replace('.txt', '') == bre ['label']:
                 fic.append(truc)
            else:
                pass
        if len(fic) == 1:
            with open(Rep+'/Description/' + fic [0], 'r', encoding ='utf8') as data:
                Description = data.read()
        elif len(fic) > 1:
            fic = [truc for truc in fic if 'en' in truc] # using english only
            if len(fic)>0:
                with open(Rep+'/Description/' + fic [0], 'r') as data:
                    Description = data.read()
            else:
                 Description = ''
        else:
             Description = ''
    else:
        Description = ''        
             
    doc = { # indexing a doc field:content
           # hacks should provide other views: citation equivalents or CIB counts... ?
           # I don't know how to do such for the moment
           "lang": "English",
           'author':bre ['inventor'],
           'applicant': bre ['applicant'],
           'country': bre ['country'],
           'kind': bre ['kind'],
           'classification': bre ['classification'],
           'CitO': bre ['CitO'],
           'CitP': bre ['CitP'],
           'date': bre ['date'],
           'CitedBy': bre ['CitedBy'],
           'title': bre ['title'],
           'abstract': abstract,
           'claims': Claims,
           'description': Description,
           'content': abstract + '\n' + Description + '\n' + Claims        
        }
    res = es.index(index=ndf.lower(), id=cpt, body=doc)
    print(res['result'])