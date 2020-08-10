# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

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
# import bs4
from Patent2Net.P2N_Lib import LoadBiblioFile
import re
import unidecode

import copy
#table = string.maketrans("","")
regex = re.compile('[%s]' % re.escape(string.punctuation))


def NoPunct(s):  # From Vinko's solution, with fix.
    temp = regex.sub(' ', s)
    temp = temp.replace('  ', ' ')
    temp = temp.replace('  ', ' ')
    temp = temp.strip()
    return temp

def Nettoie(Liste):
    indesirables = ['', u'', None, False, [], ' ', "?", "Empty", "empty"]
    Liste = [' '.join([truc.lower().title() for truc in nom.split(' ')]) for nom in Liste ] 
    return list(filter(lambda x: x not in indesirables, Liste))

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
df = pd.read_csv('../Patent2Net/Resources/StanNORM.csv', dtype=str, sep=';', encoding='utf-8')

# traitement des fichiers + familles 
for fic in [ndf, 'Families'+ndf]:
    print("\n> Hi! This is Pre Process for normalizing applicant names: used on:", fic)
    if 'Description' + fic in os.listdir(ListBiblioPath):
        with open(ListBiblioPath + '//' + fic, 'r') as data:
            dico = LoadBiblioFile(ListBiblioPath, fic)
    else:  # Retrocompatibility
        print("please use Comptatibilizer")
        sys.exit()
    LstBrevet = dico['brevets']
    

    
    cpt = 0
    appliCpt = 0
    inconnus = []
    
    with tqdm(total=len(LstBrevet), desc="computing", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
    
        for brev in LstBrevet:
            pbar.update(1)
            # ici tu as accès au contenu d'un brevet.
            # le champ qui interesse c'est ['applicant']
            temp = brev['applicant']
            tempoRes = []
            if not isinstance(temp, list):
                temp = [temp]
            for appli in temp:
                sav = copy.copy(appli)
                appli = unidecode.unidecode(appli)
                appli = NoPunct(appli)
                # appli= appli.upper()
                # appli = NoPunct(appli)
                
                # appli = appli.replace('  ', ' ')
                # appli = appli.replace('  ', ' ')
                appliCpt +=1
                #try
                indx = df.index[df['Variation Name'].str.strip() == appli]  | df.index[df['Norm'].str.strip() == appli]
                if len(indx)>0:
                    joliNom = df['Norm'].iloc[indx].to_list()[0]
                    tempoRes.append(joliNom)
                    cpt +=1
                else: # check in upper case
                    indx = df.index[df['Variation Name'].str.upper().str.strip() == appli.upper()]  | df.index[df['Norm'].str.strip().str.upper() == appli.upper()]
                    if len(indx)>0:
                        joliNom = df['Norm'].iloc[indx].to_list()[0]
                        tempoRes.append(joliNom)
                        cpt +=1
                    else:
                        tempoRes.append(sav)
                        inconnus.append((sav, appli))
        #            print ('match : ', appli, '  --> ', joliNom)
                #except:
        
            brev['applicant'] = tempoRes
            # sauvegarde dans un fichier tempo
            with open(ResultBiblioPath + '//tempo' + fic, 'ab') as ficRes:
                pickle.dump(brev, ficRes)
    
    print ('Good, ', cpt, ' normalisations done among ', appliCpt, " applicant names")
    # remplacement de la source par le résultat
    # à n'activer que quand çà marche ^_^
    os.remove(ResultBiblioPath + '//' + fic)
    shutil.move(ResultBiblioPath + '//tempo' + fic, ResultBiblioPath + '//' + fic)

    with open(ResultBiblioPath + '//tempoInconnus' + fic, 'wb') as ficRes:
            pickle.dump(inconnus, ficRes)
            

            