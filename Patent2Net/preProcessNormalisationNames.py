# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 12:05:05 2020
This script attemps normalizing names:
    Inventors: name and surname permutation tests and Levensthein distance using fuzzy-wuzzy library
    Applicants: Using the EPO List of standardised applicant names (fro 03/02/2020) but with 1400 (approx) rows added 
                using prévious method and manual check
    
@author: dreymond
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
from Patent2Net.P2N_Lib import LoadBiblioFile
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
    
     # https://github.com/pandas-dev/pandas/issues/9784
#df = pd.read_csv('../Patent2Net/Resources/StanNORM2.csv', dtype=str, sep=';', encoding='utf-8', low_memory=False)

# using excel reader seem to avoid to BOM problem

df = pd.read_excel('../Patent2Net/Resources/StanNORM2.xlsx', dtype=str, encoding='utf-8')

# import csv
# line = []
# with open("../Patent2Net/Resources/StanNORM.csv", encoding="utf8") as csvfile:
    
#     reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
#     for row in reader:
#         line.append([row['Norm'], row ["Variation Name"]])


lstApplic = []

Inventeurs = []
Applicants = []
nbAppliAvant = dict()
nbInvAvant = dict()
# traitement des fichiers + familles 
for fic in [ndf, 'Families'+ndf]:
    cptInv, cptAppl = 0,0

            
    
    print("\n> Hi! This is Pre Process for normalizing applicant names: used on:", fic)
    if 'Description' + fic in os.listdir(ListBiblioPath):
        with open(ListBiblioPath + '//' + fic, 'r', encoding ="utf8") as data:
            dico = LoadBiblioFile(ListBiblioPath, fic)
    else:  # Retrocompatibility
        print("please use Comptatibilizer")
        sys.exit()
    LstBrevet = dico['brevets']
    print  ("Good, ", len(LstBrevet), " patents found filterd from equivalent unicity")
    # patent filtering process
    Filtres = []
    dejaVus = []
    for bre in LstBrevet:
        if bre['label'] not in dejaVus:
            dejaVus.append(bre['label'])
            Filtres.append(bre)
            if isinstance(bre ['equivalents'], list):
                for eq in bre ['equivalents'] :
                    dejaVus.append(eq)
            elif len(bre ['equivalents'])>0:
                dejaVus.append(bre ['equivalents'] )
            else:
                pass
    
    
    
    for bre in LstBrevet:#[:alpha]:
        memo = copy.copy(bre['inventor'])
        
        bre['inventor'] = Nettoie(bre['inventor'])
        if isinstance(bre['inventor'], list) and len(bre['inventor'])>1 and ''.join(memo).lower() != 'empty':
            for inv in bre['inventor']:
                cptInv +=1
                temp = NoPunct(inv)
                if len(temp) == 1: # in some cases words are splitted in list of caracters somewhere... ignoring them

                    if ''.join(memo).lower() != 'empty':
                        Inventeurs.append(''.join(memo).title())

                else:
                    Inventeurs.append(temp.title())
        elif isinstance(bre['inventor'], list) and len(bre['inventor']) == 1:
            if len(bre['inventor'][0])>1:
                Inventeurs.append (bre['inventor'][0])
            else:
                bre['inventor'] = []
        elif isinstance(bre['inventor'], str) and ''.join(memo).lower() != 'empty':
            cptInv +=1
            temp = NoPunct(bre['inventor']).title()
            if len(temp)>0 and temp.lower() != 'empty':
                Inventeurs.append(temp)
               
            else:
                bre['inventor'] = []
        else:
            bre['inventor'] = []        
        memo =copy.copy(bre['applicant'])
        bre['applicant'] = Nettoie(bre['applicant'])
        if isinstance(bre['applicant'], list) and ''.join(memo).lower() != 'empty':
            for inv in bre['applicant']:
                cptAppl +=1
                temp = NoPunct(inv).upper()
                if len(temp) == 1:
                       #print (inv, ' --> ', temp)
                       if ''.join(memo).lower() != 'empty':
                           Applicants.append(''.join(memo).upper())
                else:
                    Applicants.append(temp)
                    
        elif ''.join(memo).lower() != 'empty':
            cptAppl +=1
            temp = NoPunct(bre['applicant'])
            if temp.lower() != 'empty' and len(temp) >0:
                Applicants.append(temp.upper())
            else:
                bre['applicant'] = []
        else:
            bre['applicant'] = []
    nbAppliAvant [fic]= cptAppl
    nbInvAvant [fic] = cptInv
###    
    
Inventeurs1 = [inv for inv in Inventeurs if len(inv.split(' '))<2]
Inventeurs2 = [inv for inv in Inventeurs if inv not in Inventeurs1]

Applicant_Norm = dict()
BadCasApp = dict()
InvDejaVus = []
AppDejaVus = []

Inventeurs = set(Inventeurs)
Applicants = set(Applicants)
#Applicants = set([app.lower().title() for app in Applicants])
InventeurSafe = copy.copy(Inventeurs)
AppliAvant =  len(set(Applicants))
InvAvant = len(set(Inventeurs))
#print ("Nombre de formes d'inventeurs différentes avant traitement :", InvAvant)

if "InventeurNormes.pkl" in os.listdir(ResultBiblioPath):

    with open(ResultBiblioPath + '//InventeurNormes.pkl', 'rb' ) as fic:
       Inventeur_Norm= pickle.load(fic)
        
    with open(ResultBiblioPath + '//NormInventeurs.pkl', 'rb' ) as fic:
       Norm_Inventeurs=  pickle.load(fic)
else:   
    Inventeur_Norm = dict()
    Norm_Inventeurs = dict()

for inv in Inventeurs:
    inv = inv.title()
    
    if inv not in InvDejaVus and inv not in Norm_Inventeurs.keys() and len(inv.split())>1:
        InvDejaVus.append(inv)
        reste = Inventeurs- set(InvDejaVus)
        
        
        for inv2 in reste:
            inv2 = inv2.title()
            if len(inv2.split())>1:
                
                if fuzz.token_sort_ratio(inv, inv2)>89:
                    if abs(len(inv) - len(inv2) )<10:
                        if inv in Inventeur_Norm .keys():
                            Inventeur_Norm [inv].append(inv2) 
                            
                        else:
                            Inventeur_Norm [inv] = [inv2]
                        Norm_Inventeurs [inv2] = inv
                        InvDejaVus.append(inv2)
                        
                    else:
                        print ('suspects : ', inv, " --> ", inv2)
                      
print ("Nombre d'inventeurs 'normés' (corpus + families) :", len(Inventeur_Norm.keys()), " pour ", len(Norm_Inventeurs.keys())), " sur ", cptInv, " formes au total"
#print ("Nombre de formes d'applicants différentes avant traitement :", AppliAvant)

             
cpt = 0
appliCpt = 0
inconnus = []                
lstApp = dict()     
Applicants = list(set(Applicants))  

with tqdm(total=len(Applicants), desc="computing", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
    for appli in Applicants:
        pbar.update(1)
        sav = copy.copy(appli)
        
        # appli = appli.replace('  ', ' ')
        # appli = appli.replace('  ', ' ')
        appliCpt +=1
        #try
        indx = df.index[df['Variation Name'].str.strip() == appli]  | df.index[df['Norm'].str.strip() == appli] | df.index[df['Variation Name'].str.strip() == NoPunct(appli)]
        
        if len(indx)>0:
            joliNom = df['Norm'].iloc[indx].to_list()[0]
            lstApp [appli] = joliNom
            cpt +=1

        else: # check in upper case
            indx = df.index[df['Variation Name'].str.upper().str.strip() == appli.upper()]  | df.index[df['Norm'].str.strip().str.upper() == appli.upper()]
            if len(indx)>0:
                joliNom = df['Norm'].iloc[indx].to_list()[0]
                lstApp [appli.upper()] = joliNom
                cpt +=1
            else: # checking a cleaning process juste in case
                appli = unidecode.unidecode(appli)
                appli = NoPunct(appli)
                appli= appli.upper()
                indx = df.index[df['Variation Name'].str.upper().str.strip() == appli]  | df.index[df['Norm'].str.upper().str.strip() == appli]

                if len(indx)>0:
                    joliNom = df['Norm'].iloc[indx].to_list()[0]
                    lstApp [appli] = joliNom
                    cpt +=1
                else:  # no way... Saving to see if the dictionnairy STAN has to be revised
                   appli = NoPunct(appli).title()
                   if appli in Norm_Inventeurs.keys():
                       lstApp [appli] = Norm_Inventeurs [appli]
                   inconnus.append((sav, appli))
    #            print ('match : ', appli, '  --> ', joliNom)

print ('Good, ', cpt, ' normalisations done among ', appliCpt, " applicant names")
print ('Normalizing biblio files')

InvNormes = [aut for cle in Inventeur_Norm.keys() for aut in Inventeur_Norm [cle]]

Inventors, Applicants = dict(), dict()
for fic in [ndf, 'Families'+ndf]:
    print("\n> Hi! This is Pre Process for normalizing applicant names: used on:", fic)
    if 'Description' + fic in os.listdir(ListBiblioPath):
        with open(ListBiblioPath + '//' + fic, 'r', encoding='utf8') as data:
            dico = LoadBiblioFile(ListBiblioPath, fic)
    else:  # Retrocompatibility
        print("please use Comptatibilizer")
        sys.exit()
    LstBrevet = dico['brevets']
    cpt = 0
    invCpt =0
    appliCpt= 0
    Inventors [fic] = [[],0]
    Applicants [fic] = [[],0]
    for brev in LstBrevet:
       memo = copy.copy(brev['applicant']) 
       temp = brev['applicant']
       tempoRes = []
       if not isinstance(temp, list):
           temp = [temp]
        
       for appli in temp:
           Applicants [fic][1] += 1
           Applicants [fic][0].append(appli)
           appliCpt +=1
           for inv in  brev['inventor']:
               inv = inv.title()
               if len(inv.split())>1:
                    
                    if fuzz.token_sort_ratio(inv, appli)>89:
                        if abs(len(inv) - len(appli) )<10:
                            if inv in Inventeur_Norm .keys():
                                Inventeur_Norm [inv].append(appli.title()) 
                                
                            else:
                                Inventeur_Norm [inv] = [appli.title()]
                            Norm_Inventeurs [appli.title()] = inv
                            InvDejaVus.append(appli)
                            appli=None
                        else:
                            print ('suspects : ', inv, " --> ", inv2)
           if appli and appli.lower() !='empty' and appli.title() not in Inventeurs and NoPunct(appli).title() not in Inventeurs and appli.title() not in Norm_Inventeurs.keys(): 
               if appli in lstApp.keys():
                   tempoRes.append(lstApp[appli])
                   cpt += 1
               elif appli.upper() in lstApp.keys():
                   cpt += 1
                   tempoRes.append(lstApp[appli.upper()])
               else:
                   sav = copy.copy(appli)
                   appli = unidecode.unidecode(appli)
                   appli = NoPunct(appli)
                   appli= appli.upper()
                   appli = NoPunct(appli)
                   if appli in lstApp.keys():
                       tempoRes.append(lstApp[appli])
                       cpt += 1
                
                   else:
                       tempoRes.append(sav)
           else:
                pass
                   
    # saving 
       brev['applicant'] = tempoRes
       brev['applicant-nice'] = tempoRes
       brev['applicant-old'] = memo
       tempoInv = []
       memo = copy.copy(brev['inventor'])
       if not isinstance(brev["inventor"], list):
           brev["inventor"] = [brev["inventor"]]
       for inv in brev["inventor"]:
           
           invCpt +=1
           inv = NoPunct(inv)
           inv=inv.strip().title()
           if inv in Norm_Inventeurs.keys():
               cpt+=1
               tempoInv.append(Norm_Inventeurs [inv])
               #tempoInv.append([cle for cle in Inventeur_Norm.keys() if inv in Inventeur_Norm[cle]][0].title())
           # elif NoPunct(inv) in InvNormes:
           #     tempoInv.append([cle for cle in Inventeur_Norm.keys() if NoPunct(inv) in Inventeur_Norm[cle]][0].title())
           #     cpt+=1
           else:
               tempoInv.append (inv.title())
    # saving inventor names
       brev["inventor"] = tempoInv
       brev["inventor-old"] = memo 
       for inv in tempoInv: #wht for ?
           Inventors [fic] [0].append(inv)
           Inventors [fic] [1] +=1
       
       brev['inventor-nice'] = [truc.replace(' ', '') for truc in tempoInv]
     # saving file
       with open(ResultBiblioPath + '//tempo' + fic,  'ab') as ficRes:
           pickle.dump(brev, ficRes)
        
    print ('Good, ', cpt, ' normalisations done on ', fic, ' among ', appliCpt, " applicant names")
    
                # sauvegarde dans un fichier tempo

    
    # remplacement de la source par le résultat
    # à n'activer que quand çà marche ^_^
    os.remove(ResultBiblioPath + '//' + fic)
    shutil.move(ResultBiblioPath + '//tempo' + fic, ResultBiblioPath + '//' + fic)
inconnus = set(inconnus)
with open(ResultBiblioPath + '//InventeurNormes.pkl', 'wb' ) as fic:
    pickle.dump(Inventeur_Norm, fic)
    
with open(ResultBiblioPath + '//NormInventeurs.pkl', 'wb' ) as fic:
    pickle.dump(Norm_Inventeurs, fic)
            
for fic in [ndf, 'Families'+ndf]:
    print ("Number of Inventors differents in ", fic, " : ", len(set(Inventors [fic] [0])), " from ", Inventors [fic] [1], "inventors processed in total. Before there was: ", nbInvAvant [fic])
    print ("Number of Applicants differents in ", fic, " : ", len(set(Applicants [fic] [0])), " from ", Applicants [fic] [1], "applicants processed in total. Before there was: ", nbAppliAvant [fic])
with open(ResultBiblioPath + '//tempoInconnus', 'wb') as ficRes:
    pickle.dump(inconnus, ficRes)
        

