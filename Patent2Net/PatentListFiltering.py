# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 07:39:38 2020

Patent list filtering process. As set list of patents in response to a request can provide equivalents patents in the same list we
extract from the list the first equivalents in time of apparition.
Other possible methods: 
    1. extract from families the representative set of patents (using EPO indicator) and complete it with  non present patent from initial patent list
    2. use the "prior" patent information in family set ?
I beleive they are more quickest methods....    

BUT: patent lists aren't modified yet!!!!
@author: david
"""


import datetime
import os
import sys
import shutil
import pickle
import pandas as pd
import string
from tqdm import tqdm
from Patent2Net.P2N_Config import LoadConfig
from Patent2Net.P2N_Lib_Acad import  Nettoie, NoPunct
# import bs4
from Patent2Net.P2N_Lib import  flatten, LoadBiblioFile, AnnonceProgres, AnnonceLog 
import re
import unidecode
import copy
from fuzzywuzzy import fuzz


#table = string.maketrans("","")
regex = re.compile('[%s]' % re.escape(string.punctuation))
pd.options.display.max_colwidth = 150

# def NoPunct(s):  # From Vinko's solution, with fix.
#     temp = regex.sub(' ', s)
#     temp = temp.replace('  ', ' ')
#     temp = temp.replace('  ', ' ')
#     temp = temp.strip()
#     return temp

# def Nettoie(Liste):
#     indesirables = ['', u'', None, False, [], ' ', '\t', '\n',  "?", "Empty", "empty"]
#     if isinstance(Liste, list):
    
#         Liste = [' '.join([truc for truc in nom.split(' ') if truc is not None and truc.strip() not in indesirables]) for nom in Liste if nom is not None] 
#         return list(filter(lambda x: x not in indesirables, Liste))
    
#     elif Liste in indesirables:
#         return []
#     else:
#         return [Liste]



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
    # Lecture du fichier de référence
    
DataBrevets = dict()
if 'Old' + ndf in os.listdir(ListBiblioPath):
    print("already processed. Nothing to do.")
    if 'Description' + ndf in os.listdir(ListBiblioPath):
        with open(ListBiblioPath + '//' + ndf, 'r', encoding ="utf8") as data:
            dico = LoadBiblioFile(ListBiblioPath, ndf)
        DataBrevets ['brevets'] = dico ['brevets']
        with open(ResultBiblioPath + '//Description' + ndf, 'wb') as ficRes:
            DataBrevets['ficBrevets'] = ndf
            DataBrevets['requete'] = requete
            DataBrevets["YetGathered"] = [bre ["label"] for bre in DataBrevets ['brevets']]
            DataBrevets["number"] = len(DataBrevets ['brevets'])
            pickle.dump(DataBrevets, ficRes)      
    
    sys.exit()
    

lstApplic = []

Inventeurs = []
Applicants = []
nbAppliAvant = dict()
nbInvAvant = dict()

# traitement des fichiers + familles 
for fic in [ndf]: # Families shouln't be processed like that!!!
    cptInv, cptAppl = 0,0
    
         
    
    print("\n> Hi! This is Pre Process for filtering equivalents patents from dataset gathered by P2N-OPSGather: used on:", fic)
    if 'Description' + fic in os.listdir(ListBiblioPath):
        with open(ListBiblioPath + '//' + fic, 'r', encoding ="utf8") as data:
            dico = LoadBiblioFile(ListBiblioPath, fic)
    else:  # Retrocompatibility
        print("please use Comptatibilizer")
        sys.exit()
    LstBrevet = dico['brevets']
    # patent filtering process
    Filtres = []
    dejaVus = []
    LabBrevets = [brev ['label'] for brev in LstBrevet]
    cpt = 0
    for bre in LstBrevet: # parcours de la listee des brevets
        AnnonceProgres (Appli = 'p2n_filtering', valMax = 100, valActu = cpt*50/len(LstBrevet))   
        cpt +=1
        if bre['label'] not in dejaVus:                 # si pas vu
            dejaVus.append(bre['label'])                #rajout aux vus
            
            # parcours des equivalents. Deux cas : une liste ou un chaine non vide
            if isinstance(bre ['equivalents'], list) and len(bre ['equivalents'])>0:
                # récupération de la liste des dates  de chaque équvalents
                dates = []
                for brev in bre ['equivalents']:
                    if brev in LabBrevets: # si celui-ci fait partie des brevets de départ (sinon ignoré)
                        for brevet in LstBrevet: # on va le chercher
                            if brevet['label'] == brev: # yes c'est lui !!!
                                if isinstance(brevet["date"], list): # les dates sont quelquefois en liste OU en chaine :-()
                                    date = min(brevet["date"])
                                else:
                                    date = brevet["date"]
                                # on rajoute à la structure adhoc : date, brevet, taille (nb de caractères)
                                if len(date)<4:
                                    print ("Aille")
                                dates.append((date, bre, len(str(bre.values()))))
                                #dates.extend((brevet["date"][0], brevet, len(str(brevet.values()))) for brevet in LstBrevet if brevet['label'] == brev )
                        dejaVus.append(brev)
                        
                if len(dates) ==1: # pas d'ambiguité
                    Filtres.append(dates[0][1])
                elif len(dates) >1: #récupération du plus vieux
                    MiniDate = min([dat for dat, brev,val in dates])
                    MaxVal = max (val for dat, brev, val in dates )
                    if len(MiniDate)<5:
                        print (bre['prior-Date'], ' -- > ', MiniDate)
                    # giving priority to the first in date apparition maximizing lenght (su^^posed to be fields with information)
                    candidat = [bre for dat, bre, val in dates if dat == MiniDate and val == MaxVal]
                    if len(candidat) == 0: # ou au max d'apport informationnel
                        # if it doens't work giving priority to max information content
                        candidat = [brev for dat, brev, val in dates if val == MaxVal]
                        if len(candidat) >1:
                            priorDateMin = min([min(brevet ["prior-Date"]) for brevet in candidat] )
                            NewCandidat = [brev for brev in candidat if priorDateMin in brev ["prior-Date"]]
                            if len(NewCandidat) >1:
                                NewCandidat= NewCandidat [0]
                                Filtres.append(NewCandidat)  
                            else:
                                print ("pffff")      
                    else: #aucun des équivalents dans la liste
                        Filtres.append(candidat[0])                                                 
                else:
                    Filtres.append(bre)  

            elif isinstance(bre ['equivalents'], str) and len(bre ['equivalents'])>0:
                #len(bre ['equivalents'])>0 and bre ['equivalents'] in LabBrevets:
                if bre ['equivalents'] in LabBrevets:
                    brevet = [brev for brev in LstBrevet if brev ['label'] == bre ['equivalents']][0]
                    if isinstance(brevet["date"], list): # les dates sont quelquefois en liste OU en chaine :-()
                        date = min(brevet["date"])
                    else:
                        date = brevet["date"]
                    if len(date)<4:
                        print ("Aille")
                    
                    dates = [(date, brevet, len(brevet.values()))]
                    
                    if isinstance(bre["date"], list): # les dates sont quelquefois en liste OU en chaine :-()
                        date = min(bre["date"])
                    else:
                        date = bre["date"]
                    
                    # joining currend patent
                    dates .append((date, bre, len(bre.values())))
                    
                    MiniDate = min([dat for dat, bre, val  in dates])
                    MaxVal = max([val for dat, bre, val  in dates])
                    candidat = [bre for dat, bre, val in dates if dat == MiniDate  and val == MaxVal]
                    if len(candidat) >1:
                       pass
                    elif len(candidat) == 0:
                       # if it doens't work giving priority to max information content
                       candidat = [brev for dat, brev, val in dates if val == MaxVal]
                       if len(candidat) >1:
                           priorDateMin = min([min(brevet ["prior-Date"]) for brevet in candidat] )
                           NewCandidat = [brev for brev in candidat if priorDateMin in brev ["prior-Date"]]
                           if len(NewCandidat) >1:
                               NewCandidat= NewCandidat [0]
                               Filtres.append(NewCandidat)  
                           else:
                                print ("pffff")      
                    else:
                       Filtres.append(candidat[0])  
                    
                else: #equivalent pas dans le corpus
                    Filtres.append(bre)
             
            else:
                Filtres.append(bre)
            for dat, brevet, val in dates:
                dejaVus.append(brevet['label'])
    
    # joining lost patents
    LabFiltered = []
    cpt = 0
    for bre in Filtres:
        AnnonceProgres (Appli = 'p2n_filtering', valMax = 100, valActu = 50+ cpt*10/len(Filtres))  
        cpt+=1
        if isinstance(bre["label"], str):
            LabFiltered.append(bre['label'])
        else:
            LabFiltered.append(bre['label'][0])
            
    EquivFiltered = []
    cpt = 0
    for bre in Filtres:
        AnnonceProgres (Appli = 'p2n_filtering', valMax = 100, valActu = 60+ cpt*10/len(Filtres))   
        cpt+=1
        for pat in bre ['equivalents']:
            EquivFiltered.append(pat)                
    
    complement = [bre for bre in LstBrevet \
            if bre ['label'] not in LabFiltered \
            and sum([eq in EquivFiltered for eq in bre["equivalents"]]) ==0]
    
    
    NewFilt = [] 
    DejaVus = []
    cpt = 0
    for bre in Filtres:
        AnnonceProgres (Appli = 'p2n_filtering', valMax = 100, valActu = 70+ cpt*10/len(Filtres))   
        cpt+=1
        if isinstance(bre['label'], list):
            bre['label'] = bre['label'][0]
        if bre['label'] not in DejaVus:
            equi = []
            cpFilt = copy.copy(Filtres)
            cpFilt.remove(bre)
            for bre1 in cpFilt:
                if isinstance(bre1['equivalents'], list):
                    for eq in bre1['equivalents']:
                            if len(eq) >0 and eq != 'empty':
                                equi.append(eq)
                elif  len(bre1['equivalents']) > 1 and bre1['equivalents'] != 'empty':
                     equi.append(bre1['equivalents'])
                else:
                    pass
            if len(bre['equivalents']) >0 and bre['equivalents'] != 'empty':
                res = sum([pat in equi  for pat in bre['equivalents']]+ [bre['label'] in equi])
            if res >0:
                tempo = [(bre2['date'], bre2, len(bre2.values())) for bre2 in cpFilt if bre['equivalents']] # on pourrait direct aller là et tester sur la taille de tempo :-/
                tempo2 = []
                for dat, brevet, val in tempo:
                    if isinstance(dat, str):
                        tempo2.append((dat, brevet, val))
                    elif isinstance(dat, list):
                        for truc in dat:
                            if len(truc)>0:
                                tempo2.append((truc, brevet, val))
                            else:
                                pass
                tempo = tempo2
                dates = []
                valeurs = []
                for dat, brevet, val in tempo:
                    dates.append(dat)
                    valeurs.append(val)
                miniDate = min(dates)
                maxVal = max(valeurs)
                tempo2 = [bre for dat, brevet, val in tempo if dat==miniDate and val ==maxVal]
                if len(tempo2)>0:
                    NewFilt.append(tempo2[0])
                    if isinstance(tempo2[0]['equivalents'], list):
                        for eq in tempo2[0]['equivalents']:
                            DejaVus.append(eq)
                    elif tempo2[0]['equivalents'] != 'empty':
                        DejaVus.append(tempo2[0]['equivalents'])
                else:
                    tempo2 = [bre for dat, brevet, val in tempo if val ==maxVal]
                    if len(tempo2)>0:
                         NewFilt.append(tempo2[0])
                         if isinstance(tempo2[0]['equivalents'], list):
                            for eq in tempo2[0]['equivalents']:
                                DejaVus.append(eq)
                         elif tempo2[0]['equivalents'] != 'empty':
                                DejaVus.append(tempo2[0]['equivalents'])
                         
                         else:
                             pass
                    else:                    
                         NewFilt.append(bre)
    
            else:
                NewFilt.append(bre)
            if isinstance(bre['label'], str):
                DejaVus .append(bre['label'])
            else:
                for lab in bre['label']:
                    DejaVus .append(lab)
            if isinstance(bre['equivalents'], list):
                 for eq in bre['equivalents']:
                     DejaVus.append(eq)
            elif bre['equivalents'] != 'empty':
                DejaVus.append(bre['equivalents'])
        else:
            pass
        
    EquivFiltered = []
    cpFilt = copy.copy(Filtres)
    cpt = 0
    for bre in Filtres:
        AnnonceProgres (Appli = 'p2n_filtering', valMax = 100, valActu = 80+ cpt*10/len(Filtres))   
        cpt+=1
        if not isinstance(bre['label'], str):
            if len(bre ['label'])>0:
                bre ['label'] = bre['label'][0]
            else:
                print ("no label !!!!")
        else:
            pass
    toRemove = []
    cpt = 0
    for bre in Filtres:
        AnnonceProgres (Appli = 'p2n_filtering', valMax = 100, valActu = 90+ cpt*10/len(Filtres))   
        cpt+=1
        if not isinstance(bre ['equivalents'], list):
            if len(bre ['equivalents']) and bre ['equivalents'] != 'empty':
                bre ['equivalents'] = [bre ['equivalents']]
            else:
                bre ['equivalents'] =[]
        for pat in bre ['equivalents']:
            if pat != bre['label']:
                if pat not in EquivFiltered:
                    EquivFiltered.append(pat)
                else:
                    cpFilt = [brev for brev in cpFilt if brev ['label'] != bre['label']]
                    toRemove.append((bre ['label'], bre))
    exclude = [truc for truc, muche in toRemove]
    Resultat = []
    for bre in Filtres:
        if bre['label'] not in exclude: 
            Resultat.append(bre)
            
    EquivFiltered2 = []
    for bre in Resultat:
        for pat in bre ['equivalents']:
            EquivFiltered2.append(pat)     
    AnnonceProgres (Appli = 'p2n_filtering', valMax = 100, valActu = 100)
    print("net set of equivalent covered: ",len(EquivFiltered2))
    print(len(LstBrevet), '  --> ', len (Filtres), ' --> ', len(Resultat)) 
    print  ("Good, ", len(Resultat + complement), " patents filterd from equivalent unicity exrtracted from ", fic)
    #Saving file
    
    for brev in Resultat:

        with open(ResultBiblioPath + '//tempo' + fic,  'ab') as ficRes:
            pickle.dump(brev, ficRes)
    
    os.rename(ResultBiblioPath + '//' + fic, ResultBiblioPath + '//Old' + fic)
    os.rename(ResultBiblioPath + '//tempo' + fic, ResultBiblioPath + '//' + fic)


    # cleaning  abstracts files
    cpt = 0
    Exclusions = [pat ['label'] for pat in LstBrevet if pat not in Resultat]
    for fichier in os.listdir(ResultPathContent+'/PatentContents/Abstract'):
        if fichier.split('.')[0] in Exclusions or fichier.split('.')[0].split('-') [1] in Exclusions:
            os.remove(ResultPathContent+'/PatentContents/Abstract/'+fichier)
            cpt+=1
    DataBrevets = dict()
    with open(ResultBiblioPath + '//Description' + ndf, 'wb') as ficRes:
        DataBrevets['ficBrevets'] = fic
        DataBrevets['requete'] = requete
        DataBrevets["YetGathered"] = [bre ["label"] for bre in Resultat]
        DataBrevets["number"] = len(Resultat)
        pickle.dump(DataBrevets, ficRes)            
    
    

    print ('deleted ', cpt, ' abstracts')
fic = 'Families' + ndf
if 'Description' + fic in os.listdir(ResultBiblioPath):
    with open(ListBiblioPath + '//' + fic, 'r', encoding ="utf8") as data:
        dico = LoadBiblioFile(ListBiblioPath, fic)    
    os.rename(ResultBiblioPath + '//' + fic, ResultBiblioPath + '//Old' + fic)
    
    #the following should be done by GatherFamilies process. 
    # just in case...
    dat = dico['brevets']
    labs = [bre ['label'] for bre in dat]
    labs = flatten(labs)  # some patents have multiples labels
    cpt1, cpt2 = 0,0
    if len(labs) != len(set(labs)):
        DejaVus = []
        with open(ResultBiblioPath+'//Families'+ ndf, 'wb') as ndfLstBrev:
            for bre in dat:
                for cle in bre.keys():
                    if isinstance(bre[cle], list): #cleaning
                        bre[cle] = list(set(bre[cle]))
                if isinstance(bre['label'], str):
                    if bre['label'] not in DejaVus:
                        pickle.dump(bre , ndfLstBrev)
                        DejaVus.append(bre['label'])
                        cpt1 +=1
                    else:
                        pass
                else:
                    for lab in set(bre['label']):
                        if lab not in DejaVus:
                            pickle.dump(bre , ndfLstBrev)
                            DejaVus.append(lab)
                            cpt2 +=1
                        else:
                            pass
    print(cpt1, cpt2)
    print (len(set(labs)))
    with open(ResultBiblioPath + '//' + 'Description' + fic, 'wb') as ficRes:
        DataBrevets['ficBrevets'] = 'Families'+ ndf
        DataBrevets['requete'] = "Families of: " + requete
        DataBrevets["number"] = len(set(labs))
        pickle.dump(DataBrevets, ficRes)           
