# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 06:55:02 2021

@author: david
"""



import codecs
import os
import sys
import shutil
import pickle
import matplotlib.cm
from pymed import PubMed

from Patent2Net.P2N_Lib import LoadBiblioFile,  UrlPatent,UrlApplicantBuild,UrlInventorBuild,UrlIPCRBuild, cmap_discretize, RenderTemplate
from Patent2Net.P2N_Config import LoadConfig
#from Patent2Net.P2N_Lib_Acad import IPCCategorizer, IPCExtractPredictionBrevet,PubMedCheckNameAndGetAffiliation, OPSChercheAbstractBrevet
from Patent2Net.P2N_Lib_Acad import  Nettoie, NoPunct, CheckListInclu, CheckListMix, CheckListExclu, UnCheck, Check
from fuzzywuzzy import fuzz


import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
import pandas as pd
import string
import re
import unidecode
import pandas as pd
import itertools


def swap(x,y):
  return y,x 

def swapList(liste):
    assert(len(liste) == 2)
    return [liste[1], liste[0]] 

def cycle (liste):
    tempo = []
    if len(liste) < 1:
        return None
    else:
        taille = len(liste)-1
        for indice in range(taille):
            tempo.append((liste [indice], liste[indice+1]))
        return tempo

# les trucs à virer des différents champs
Exclus = ['', ' ', 'empty', None, "none"]
#####

# CHARGEMENT DU DICO ENTITES PUBLIQUES
##############


xlsx = pd.ExcelFile('./Resources/EntitésPubliquesNORM4.xlsx')
Public = []
TypeAppl = dict()
# df = pd.read_csv('../Patent2Net/Resources/STANNorm.csv', dtype=str, sep=';', encoding='utf-8')


for sheet in xlsx.sheet_names:
   dicotemp = xlsx.parse(sheet).to_dict(orient='list')
   
   for cle, val in dicotemp.items():
        tempoRes = []
        for appli in val:
            sav = appli
            tempoRes.append(appli)
        TypeAppl [cle] = tempoRes
        Public.extend(tempoRes)

# =============================================================================
# 
# # CHARGEMENT des données brevet
# 
# 
# =============================================================================

configFile = LoadConfig()
# Les champs nécessaires par brevet.
NeededInfo = ['label', 'date', 'inventor', 'title', 'abstract']

requete = configFile.requete
projectName = configFile.ndf
ndf = "Families"+ projectName
BiblioPath = configFile.ResultBiblioPath
ResultBiblioPath = configFile.ResultBiblioPath
temporPath = configFile.temporPath
ResultGephiPath = configFile.ResultGephiPath

ResultPathContent= configFile.ResultContentsPath
ResultAbstractPath = configFile.ResultAbstractPath
Auteur = configFile.ResultPath + '//AcadCorpora'
RepDir = configFile.ResultPath + '//AcadCorpora'
project = RepDir
for ndf in [projectName,  "Families"+ projectName]:
    if 'Description'+ndf in os.listdir(BiblioPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
        print( "loading patent biblio data with ", " and ".join(NeededInfo), " fields.")
        DataBrevet = LoadBiblioFile(BiblioPath, ndf)
        print("Hi this is AcadStats processor. Bibliographic data of ", ndf, " patent universe found.")
    
    
    print("Nice, ", len(DataBrevet["brevets"]), " patents found. On calcule les auteurs identifiés...")
    
    
    # loading file from preProcessNormalisationNames
    # inventors names are normalised there
    if "InventeurNormes.pkl" in os.listdir(ResultBiblioPath + '//'):
        with open(ResultBiblioPath + '//InventeurNormes.pkl', 'rb' ) as fic:
            Inventeur_Norm = pickle.load(fic)
    else:
        Inventeur_Norm = dict()
    for cle in Inventeur_Norm.keys():
        Inventeur_Norm [cle] = [truc.title() for truc in Inventeur_Norm [cle]]
        
    InvNormes = [aut.title() for cle in Inventeur_Norm.keys() for aut in Inventeur_Norm [cle]]
    InvNormes = list(set(InvNormes))
    
    
    # =============================================================================
    # Paramètres 
    # =============================================================================
    
    
    
    screenX = 1500  # taille des canevas de graphe par défaut
    screenY = 1000
    
    dicoAttrs  = dict() # attributes for patent nodes
    dicoAttrsAppli = dict() # attributes for applicant nodes..
    dicoAttrsAut = dict() # attributes for author nodes
    dicoAttrsCitP = dict()
    dicoAttrsCitedBy = dict()
    dicoAttrsEquiv  = dict()
    dicoAttrsOut = dict()
    dicoAttrsTechno = dict()
    Applicants = set ()
    Techno = dict()
    Inventeurs = set()
   


    # =============================================================================
    # 
    # Cleaning stuff and dataframe loading 
    # 
    # =============================================================================
    
    df = pd.DataFrame(DataBrevet["brevets"])
    # Rajout de colonne au df
    
    df ['family lenght'] = 0
    df ['IPCR11-range'] = df ['IPCR11'].apply(len)
    df ['IPCR4-range'] = df ['IPCR4'].apply(len)
    df ['IPCR7-range'] = df ['IPCR7'].apply(len)
    
    
    # chargement du fichier famille puis calcul des tailles de famille par brevet
    if ndf.startswith('Families'):
        switch=''
    else:
        switch='Families'
    print("\n> Hi! This is Net processor used on:", ndf)
    if 'Description' + switch+ndf in os.listdir(ResultBiblioPath):
        with open(ResultBiblioPath + '//' + switch+ndf, 'r') as data:
            dico = LoadBiblioFile(ResultBiblioPath, switch +ndf)
    else:  # Retrocompatibility
        print("please use Comptatibilizer")
        sys.exit()
    
    if 'Families' not in ndf:
        df_Fam = pd.DataFrame(dico ["brevets"])
        for bre in df['label']:
            try:
                df['family lenght'].loc[df.index[df['label'] == bre]] =  df_Fam['family lenght'].loc[df_Fam.index[df_Fam['label'] == bre]].values[0]
            except:
                df['family lenght'].loc[df.index[df['label'] == bre]] =  0 #df_Fam['family lenght'].loc[df_Fam.index[bre in df_Fam['equivalents']]].values[0]
    #        print (df_Fam['family lenght'].loc[df_Fam.index[df_Fam['label'] == bre]])

    
    #cleaning df. These steps should be place in preProcessNames
    
    for bre in df.itertuples():
        if isinstance(bre.label, list):
            df.at [bre.Index, 'label' ] = bre.label[0] 
        if isinstance(bre.Citations, list):
        
            df.at [bre.Index, 'Citations' ] = bre.Citations[0] 
        if isinstance(bre.equivalents, str):
            if bre.equivalents not in Exclus:
                 df.at [bre.Index, 'equivalents' ] = [bre.equivalents]
            else:
                df.at [bre.Index, 'equivalents' ] = []
        
        # normalising and cleaning
        if not isinstance(bre.inventor, list):
            if bre.inventor.strip() not in Exclus:   
                if ''.join(bre.inventor).strip().lower() != 'empty':
                    temp  = bre.inventor.replace('-', ' ')
                    df.at [bre.Index, 'inventor' ] = [temp.title()]
                else:
                    df.at [bre.Index, 'inventor' ] = []
            else:
                df.at [bre.Index, 'inventor' ] = []    
        
        else:
            tempoinv = []
            for inv in bre.inventor:
                if ''.join(inv).strip().lower() != 'empty':
                    inv = inv.replace('-', ' ')
                    if inv.strip() not in Exclus:
                        tempoinv.append(inv.title())
            df.at [bre.Index, 'inventor' ] = tempoinv
        
    
        
        if not isinstance(bre.applicant, list):
            if bre.applicant not in Exclus and bre.applicant not in bre.inventor:   
                if ''.join(bre.applicant).strip().lower() != 'empty':
                    df.at [bre.Index, 'applicant' ] = [bre.applicant.upper()]
                else:
                    df.at [bre.Index, 'applicant' ] = []
            else:
                df.at [bre.Index, 'applicant' ] = []
        else:
            tempoappl = []
            for appl in bre.applicant:
                if ''.join(appl).strip().lower() != 'empty' and appl not in bre.inventor:
                    tempoappl.append(appl.upper())
            df.at [bre.Index, 'applicant' ] = tempoappl
        
        for appl in bre.applicant:
            if appl not in bre.inventor:
                Applicants. add(appl.upper())
        
        # special clean qu'on sait pas d'où çà sort        
        if isinstance(bre.IPCR11, list):
            if len(bre.IPCR11) == 1:
                df.at [bre.Index, 'IPCR11' ] = [''.join (bre.IPCR11)]
                
        if isinstance(bre.IPCR7, list):
            if len(bre.IPCR7) == 1:
                df.at [bre.Index, 'IPCR7' ] = [''.join (bre.IPCR7)]

        if isinstance(bre.IPCR4, list):
            if len(bre.IPCR4) == 1:
                df.at [bre.Index, 'IPCR4' ] = [''.join (bre.IPCR4)]

        if isinstance(bre.IPCR3, list):
            if len(bre.IPCR3) == 1:
                df.at [bre.Index, 'IPCR3' ] = [''.join (bre.IPCR3)]

        if not isinstance(bre.IPCR11, list):
    
            if bre.IPCR11 not in Exclus:   
                if ''.join(bre.IPCR11).strip().lower() != 'empty':
                    
                    df.at [bre.Index, 'IPCR11' ] = [bre.IPCR11.replace('/', '-')]
                else:
                    df.at [bre.Index, 'IPCR11' ] = []
            else:
                df.at [bre.Index, 'IPCR11' ] = []    
        
        else:
            tempoinv = []
            for inv in bre.IPCR11:
                inv = inv.replace('/', '-')
                if ''.join(inv).strip().lower() != 'empty':
                    if inv not in Exclus:
                        tempoinv.append(inv.upper())
            df.at [bre.Index, 'IPCR11' ] = tempoinv
    
        if not isinstance(bre.IPCR7, list):
            if bre.IPCR7 not in Exclus:   
                if ''.join(bre.IPCR7).strip().lower() != 'empty':
                    if bre.IPCR7.strip() not in Exclus:
                        if len(bre.IPCR7)<5:
                            print("7")
                        else:
                            df.at [bre.Index, 'IPCR7' ] = [bre.IPCR7]
                else:
                    df.at [bre.Index, 'IPCR7' ] = []
            else:
                df.at [bre.Index, 'IPCR7' ] = []    
        
        else:
            tempoinv = []
            for inv in bre.IPCR7:
                if ''.join(inv).strip().lower() != 'empty':
                    if inv not in Exclus:
                        if inv not in Exclus:
                            if len(inv)<5:
                                print("5")
                            else:
                                tempoinv.append(inv.upper())
            df.at [bre.Index, 'IPCR7' ] = tempoinv
        
        if not isinstance(bre.IPCR4, list):
            if bre.IPCR4 not in Exclus:   
                if ''.join(bre.IPCR4).strip().lower() != 'empty':
                    if bre.IPCR4.strip() not in Exclus:
                        if len(bre.IPCR4)<4:
                            print("4")
                        else:
                            df.at [bre.Index, 'IPCR4' ] = [bre.IPCR4]
                else:
                    df.at [bre.Index, 'IPCR4' ] = []
            else:
                df.at [bre.Index, 'IPCR4' ] = []    
        
        else:
            tempoinv = []
            for inv in bre.IPCR4:
                if ''.join(inv).strip().lower() != 'empty':
                    if inv not in Exclus:
                        if len(inv)<4:
                            print("3")
                        else:
                            tempoinv.append(inv.upper())
            df.at [bre.Index, 'IPCR4' ] = tempoinv
        
        if not isinstance(bre.IPCR3, list):
            if bre.IPCR3 not in Exclus:   
                if ''.join(bre.IPCR3).strip().lower() != 'empty':
                    if bre.IPCR3.strip() not in Exclus:
                        df.at [bre.Index, 'IPCR3' ] = [bre.IPCR3]
                else:
                    df.at [bre.Index, 'IPCR3' ] = []
            else:
                df.at [bre.Index, 'IPCR3' ] = []    
        
        else:
            tempoinv = []
            for inv in bre.IPCR3:
                if inv.strip() not in Exclus:
                    if ''.join(inv).strip().lower() != 'empty':
                        if len(inv)<3:
                            print()
                        else:
                            tempoinv.append(inv.upper())
            df.at [bre.Index, 'IPCR3' ] = tempoinv
        
        if not isinstance(bre.IPCR1, list):
            
            if bre.IPCR1 not in Exclus:   
                if ''.join(bre.IPCR1).strip().lower() != 'empty':
                    df.at [bre.Index, 'IPCR1' ] = [bre.IPCR1]
                else:
                    df.at [bre.Index, 'IPCR1' ] = []
            else:
                df.at [bre.Index, 'IPCR1' ] = []    
        
        else:
            tempoinv = []
            for inv in bre.IPCR1:
                if ''.join(inv).strip().lower() != 'empty':
                    tempoinv.append(inv.upper())
            df.at [bre.Index, 'IPCR1' ] = tempoinv
        
        if not isinstance(bre.equivalents, list):
            if bre.equivalents.strip() not in Exclus:
                df.at [bre.Index, 'equivalents' ] = [bre.equivalents]
        else:
            df.at [bre.Index, 'equivalents' ] = list (set([ipc for ipc in bre.equivalents if ipc.lower() not in Exclus]))
        if not isinstance(bre.CitedBy, list):
            if bre.CitedBy.strip() not in Exclus:
                df.at [bre.Index, 'CitedBy' ] = [bre.CitedBy]
        else:
            df.at [bre.Index, 'CitedBy' ] = list (set([ipc for ipc in bre.CitedBy if ipc.lower() not in Exclus]))            
        if not isinstance(bre.CitP, list):
            if bre.CitP.strip() not in Exclus:
                df.at [bre.Index, 'CitP' ] = [bre.CitP]
        else:
            df.at [bre.Index, 'CitP' ] = list (set([ipc for ipc in bre.CitP if ipc.lower() not in Exclus]))            
        if not isinstance(bre.CitO, list):
            if bre.CitO.strip() not in Exclus:
                df.at [bre.Index, 'CitO' ] = [bre.CitO]
        else:
            df.at [bre.Index, 'CitO' ] = list (set([ipc for ipc in bre.CitO if ipc.lower() not in Exclus]))     

        assert(isinstance(df.at [bre.Index, 'IPCR1' ], list))

        assert(isinstance(df.at [bre.Index, 'IPCR11' ], list))
        assert(isinstance(df.at [bre.Index, 'IPCR3' ], list))
        assert(isinstance(df.at [bre.Index, 'IPCR7' ], list))
        assert(isinstance(df.at [bre.Index, 'IPCR4' ], list))
        # df.at [bre.Index, 'IPCR1' ] = [truc for truc in bre.IPCR1 if truc.strip() not in Exclus] 
        # df.at [bre.Index, 'IPCR3' ] = [truc for truc in bre.IPCR3 if truc.strip() not in Exclus] 
        # df.at [bre.Index, 'IPCR4' ] = [truc for truc in bre.IPCR4 if truc.strip() not in Exclus] 
        # df.at [bre.Index, 'IPCR7' ] = [truc for truc in bre.IPCR7 if truc.strip() not in Exclus] 
        # df.at [bre.Index, 'IPCR11' ] = [truc for truc in bre.IPCR11 if truc.strip() not in Exclus] 
    # c'est parti !
    # On parcours le jeu de brevet pour stocker les noms et trucs
    # Inventeurs = set() # la liste des inventeurs
    # Applicants = set()
    # Techno = dict()
    for bre in df.itertuples():

                
        for truc in bre.applicant:
            Applicants. add(truc)
            if len(bre .IPCR11 )>0:
                Techno[truc] =  [cib for cib in bre .IPCR11] 
            elif len(bre .IPCR7 )>0:
                Techno[truc] =  [cib for cib in bre .IPCR7]
            elif len(bre .IPCR4 )>0:
                Techno[truc] =  [cib for cib in bre .IPCR4]
            elif len(bre .IPCR1 )>0:
                Techno[truc] =  [cib for cib in bre .IPCR1]
            else:
                Techno[truc] = []
        for truc in bre .inventor:
            
            Inventeurs.add(truc)
            if len(bre .IPCR11 )>0:
                Techno[truc] =  [cib for cib in bre .IPCR11] 
            elif len(bre .IPCR7 )>0:
                Techno[truc] =  [cib for cib in bre .IPCR7]
            elif len(bre .IPCR4 )>0:
                Techno[truc] =  [cib for cib in bre .IPCR4]
            elif len(bre .IPCR1 )>0:
                Techno[truc] =  [cib for cib in bre .IPCR1]
            else:
                Techno[truc] = []
                
                
        dicoAttrs [bre.label] = {'Famille': sum( [bre.label in truc for truc in df_Fam ['equivalents']]),
                                    'IPC11-range': len(set(bre.IPCR11)),
                                    'IPC7-range': len(set(bre.IPCR7)),
                                    'IPC4-range': len(set(bre.IPCR4)),
                                    'Citations' : bre.Citations,
                                    "category" : 'label', 
                                    "url" : UrlPatent(bre.label)[0],
                                    "size" : sum( [bre.label in truc for truc in df_Fam ['equivalents']])
                                    #'NbBrevets' : 1
                                    }
        for lab in bre.CitP:
            dicoAttrsCitP [lab] = {"category" : 'CitP'
                }
        for lab in bre.CitedBy:
            dicoAttrsCitedBy [lab] = {"category" : 'CitedBy'
                }
        for lab in bre.equivalents:
            dicoAttrsEquiv [lab] = {"category" : 'equivalent'
                }
        for lab in bre.CitO: # we may get in trouble here
            if len(lab)>0:
                dicoAttrsOut [lab] = {"category" : 'CitO'
                }
        for ipc in bre.IPCR1:
            if len(ipc)>0 and ipc not in dicoAttrsTechno.keys():
                dicoAttrsTechno [ipc] = {'category' : "IPCR1"}
        for ipc in bre.IPCR4:
            if len(ipc)>0 and ipc not in dicoAttrsTechno.keys():
                dicoAttrsTechno [ipc] = {'category' : "IPCR4"}
        for ipc in bre.IPCR7:
            if len(ipc)>0 and ipc not in dicoAttrsTechno.keys():
                dicoAttrsTechno [ipc] = {'category' : "IPCR7"}
        for ipc in bre.IPCR11:
            ipc = ipc.replace('/', '-')
            if len(ipc)>0 and ipc not in dicoAttrsTechno.keys():
                dicoAttrsTechno [ipc] = {'category' : "IPCR11"}
     
    
    
    
    #• Generating nodes attributes
    for aut in Applicants:
        # node attributes for an applicant
        
        if len(aut) >0:
            IPC11_range = []
            IPC7_range = []
            IPC4_range = []
            [IPC4_range.extend(bre.IPCR4) for bre in  df.itertuples() if aut in bre.applicant]
            [IPC7_range.extend(bre.IPCR7) for bre in  df.itertuples() if aut in bre.applicant]
            [IPC11_range.extend(bre.IPCR11) for bre in  df.itertuples() if aut in bre.applicant]

            dicoAttrsAppli [aut] = {#'AutFr': dicoAttrsAut [aut]['AutFr'],
                              'Citations' : sum ( [bre.Citations for bre in  df.itertuples() if aut in bre.applicant]), # sum of citations of each patent 
                              'Famille' : sum( [aut in truc for truc in df_Fam ['applicant']]), # sum of family lenght for each patent of this applicant
                              'category' : 'Applicant',
                              'size' : sum( [aut in truc for truc in df ['applicant']]), # number of patents
                              'NbBrevets' : sum( [aut in truc for truc in df ['applicant']]), # number of patents
                              'IPC11-range' : len(set(IPC11_range)), # variety of IPC level 11
                              'IPC7-range' : len(set(IPC7_range)),
                              'IPC4-range' : len(set(IPC4_range)),
                              'IPCDiversity': len(set(IPC11_range)), # number of variety
                              'IPCForce' : len(IPC11_range), # same as previous but with occurences
                              'type': 'Applicant',
                              'url': UrlApplicantBuild (aut)[0],
                              
                              }  
    
    
    # create median values for appl attributes
    TailleFamiile = 0
    NbBrevets = 0
    nbCitations = 0
    IPC11 =0
    IPC7 = 0
    IPC4 = 0
    IPCForce = []
    for appl in set(Applicants):
        Techno [appl] = list(filter(lambda x: x !='', Techno [appl]))
        dicoAttrsAppli [appl] = {"category" : dicoAttrsAppli [appl]["category"] ,
                            'Famille': dicoAttrsAppli [appl]['Famille'],
                            'IPC11-range': dicoAttrsAppli [appl]['IPC11-range'],
                            'IPC7-range': dicoAttrsAppli [appl]['IPC7-range'],
                            'IPC4-range': dicoAttrsAppli [appl]['IPC4-range'],
                            'IPCDiversity': dicoAttrsAppli [appl]['IPCDiversity'],
                            'IPCForce' : dicoAttrsAppli [appl]['IPCForce'],
                            'Citations' : dicoAttrsAppli [appl]['Citations'],
                            'NbBrevets' : dicoAttrsAppli [appl]['NbBrevets'],
                            'type':dicoAttrsAppli [appl]['type'],
                            'url': dicoAttrsAppli [appl]['url'],
                            'MedFamille': dicoAttrsAppli [appl]['Famille']/ dicoAttrsAppli [appl]['NbBrevets'],
                            'MedIPC11-range': dicoAttrsAppli [appl]['IPC11-range']/ dicoAttrsAppli [appl]['NbBrevets'],
                            'MedIPC7-range': dicoAttrsAppli [appl]['IPC7-range']/ dicoAttrsAppli [appl]['NbBrevets'],
                            'MedIPC4-range': dicoAttrsAppli [appl]['IPC4-range']/ dicoAttrsAppli [appl]['NbBrevets'],
                            'MedIPCDiversity': len(set(Techno [appl]))/ dicoAttrsAppli [appl]['NbBrevets'],
                            'MedIPCForce' : len(Techno [appl]) / dicoAttrsAppli [appl]['NbBrevets'],
                            'MedCitations' : dicoAttrsAppli [appl]['Citations']/ dicoAttrsAppli [appl]['NbBrevets'],
    
                                         
                            }
    
        TailleFamiile += sum( [appl in truc for truc in df_Fam ['applicant']]) # nombre d'apparition dans les familles
        NbBrevets += sum( [appl in truc for truc in df ['applicant']]) # nombre de brevets
        nbCitations +=  sum ( [bre.Citations for bre in  df.itertuples() if appl in bre.applicant])
        IPC11 +=dicoAttrsAppli [appl]['IPC11-range']
        IPC7 += dicoAttrsAppli [appl]['IPC7-range']
        IPC4 +=dicoAttrsAppli [appl]['IPC4-range']
        IPCForce += Techno [appl]
    
    IPCDiversity = len(set(IPCForce))
    IPCForce = len(IPCForce)
    
    #♦ cas des sous corpus sans applicants
    if TailleFamiile ==0:
        TailleFamiile = sum ([dicoAttrsAut [appl]['Famille'] for appl in dicoAttrsAut.keys()])
    if NbBrevets ==0:
        NbBrevets = sum ([dicoAttrsAut [appl]['NbBrevets'] for appl in dicoAttrsAut.keys()])
    if nbCitations == 0:
        nbCitations = sum ([dicoAttrsAut [appl]['Citations'] for appl in dicoAttrsAut.keys()])
    if IPC11 ==0:
        IPC11 =  sum ([dicoAttrsAut [appl]['IPC11-range'] for appl in dicoAttrsAut.keys()])
    if IPC7 ==0:
        IPC7 =  sum ([dicoAttrsAut [appl]['IPC7-range'] for appl in dicoAttrsAut.keys()])
    if IPC4 ==0:
        IPC4 =  sum ([dicoAttrsAut [appl]['IPC4-range'] for appl in dicoAttrsAut.keys()])
    if IPCDiversity ==0:
        IPCDiversity =  sum ([dicoAttrsAut [appl]['IPCDiversity'] for appl in dicoAttrsAut.keys()])
    if IPCForce ==0:
        IPCForce =  sum ([dicoAttrsAut [appl]['IPCForce'] for appl in dicoAttrsAut.keys()])
    
    
    

    for appl in Inventeurs:
        if len(appl)>0 and appl not in Exclus :
     
            Techno [appl] = list(filter(lambda x: x !='', Techno [appl]))
            
            
            appl=appl.title()
            IPC11_range = []
            IPC7_range = []
            IPC4_range = []
            [IPC4_range.extend(bre.IPCR4) for bre in  df.itertuples() if appl in bre.inventor]
            [IPC7_range.extend(bre.IPCR7) for bre in  df.itertuples() if appl in bre.inventor]
            [IPC11_range.extend(bre.IPCR11) for bre in  df.itertuples() if appl in bre.inventor]
    
            TailleFamiileAut = sum( [appl in truc for truc in df_Fam ['inventor']])
            NbBrevetsAut = sum ( [1 for bre in  df.itertuples() if appl in bre.inventor])
            nbCitationsAut =  sum ( [bre.Citations for bre in  df.itertuples() if appl in bre.inventor]),
            IPC11Aut = sum ( [len(bre.IPCR11) for bre in  df.itertuples() if appl in bre.inventor])
            IPC7Aut = sum ( [len(bre.IPCR7) for bre in  df.itertuples() if appl in bre.inventor])
            IPC4Aut = sum ( [len(bre.IPCR4) for bre in  df.itertuples() if appl in bre.inventor])
            IPCForceAut = len(Techno [appl])
            
            dicoAttrsAut [appl] = {

                          'Citations' : sum ( [bre.Citations for bre in  df.itertuples() if appl in bre.inventor]), # sum of citations of each patent ,
                          'Famille' : sum( [appl in truc for truc in df_Fam ['inventor']]),
                          'category' : "Inventor",
                          'NbBrevets' :sum( [appl in truc for truc in df ['inventor']]),
                          'IPC11-range' : len(set(IPC11_range)), # variety of IPC level 11
                          'IPC7-range' : len(set(IPC7_range)),
                          'IPC4-range' : len(set(IPC4_range)),
                          'IPCDiversity': len(set(IPC11_range)), # number of variety
                          'IPCForce' : len(IPC11_range),
                          'url': UrlInventorBuild (appl)[0],
                          'size' :  sum( [appl in truc for truc in df ['inventor']])
                          }
            dicoAttrsAut [appl] ['MedFamille'] = dicoAttrsAut [appl]['Famille']/ dicoAttrsAut [appl]['NbBrevets']
            dicoAttrsAut [appl] ['MedIPC11-range'] = dicoAttrsAut [appl]['IPC11-range']/ dicoAttrsAut [appl]['NbBrevets']
            dicoAttrsAut [appl] ['MedIPC7-range'] = dicoAttrsAut [appl]['IPC7-range']/ dicoAttrsAut [appl]['NbBrevets']
            dicoAttrsAut [appl] ['MedIPC4-range'] = dicoAttrsAut [appl]['IPC4-range']/ dicoAttrsAut [appl]['NbBrevets']
            dicoAttrsAut [appl] ['MedIPCDiversity'] = len(set(Techno [appl]))/ dicoAttrsAut [appl]['NbBrevets']
            dicoAttrsAut [appl] ['MedIPCForce' ] = len(Techno [appl]) / dicoAttrsAut [appl]['NbBrevets']
            dicoAttrsAut [appl] ['MedCitations' ] =dicoAttrsAut [appl]['Citations']/ dicoAttrsAut [appl]['NbBrevets']
    
    
    
    # TODO 
    # CHECK the stats Using math ans score
    
    # =============================================================================
    # Go fo Nets
    # =============================================================================
    
    Networks = dict()
    #next lines are here to avoid the changing scheme lecture of requete.cql
    
    Networks["_CountryCrossTech"] =  [configFile.CountryCrossTechNetwork, [ 'IPCR7', "country"]] # not finished yet
    Networks["_CrossTech"] =  [configFile.CrossTechNetwork, ['label','IPCR7','IPCR1', 'IPCR4', 'IPCR11']] # GraphTechnos
    Networks["_Inventors_CrossTech"] =  [configFile.InventorCrossTechNetwork, ['IPCR11','IPCR7','IPCR4','IPCR1',"Inventor"]]#, 'AutFr', 'AutEtr', 'PasSurPubMed']] # GraphTechnosAuthor
    Networks["_Applicants_CrossTech"] =  [configFile.ApplicantCrossTechNetwork, ['IPCR11','IPCR7','IPCR4','IPCR1', "Applicant"]] #, "Public", "Private"]] # GraphTechnosAppli
    Networks["_ApplicantInventor"] = [configFile.ApplicantInventorNetwork, ["Applicant","Inventor"]]#, "Public", "Private", 'AutFr', 'AutEtr', 'PasSurPubMed']] # GraphAuteursAppli
    Networks["_Applicants"] =  [configFile.ApplicantNetwork, ["Applicant"]]#, "Public", "Private"]] # GraphApplicant
    Networks["_Inventors"] =  [configFile.InventorNetwork, ["Inventor"]]#, 'AutFr', 'AutEtr', 'PasSurPubMed']] # GraphAuteurs
    Networks["_References"] =  [configFile.References, [ 'label', 'CitP', "CitO"]] # GraphBrevetsReferences
    Networks["_Citations"] =  [configFile.Citations, [ 'label', "CitedBy"]] # GraphBrevetsCitations
    Networks["_Equivalents"] =  [configFile.Equivalents, [ 'label', "equivalent"]] # GraphBrevetsEquivalents
    Networks["_LabelApplicants"] =  [configFile.ApplicantNetwork, [ 'label', "Applicant"]]#, "Public", "Private"]] # GraphBrevetsEquivalents#GraphBrevets
    
    GraphAuteurs = nx.DiGraph()
    GraphApplicant = nx.DiGraph()
    GraphBrevets = nx.DiGraph()
    GraphAuteursAppli = nx.DiGraph()
    GraphBrevetsCitations = nx.DiGraph() # graph of citing patents of patents from PU
    GraphBrevetsReferences = nx.DiGraph() # graph of references from patents from PU includes patents and other references
    GraphBrevetsEquivalents = nx.DiGraph() # graph of equivalents
    GraphTechnos = nx.DiGraph() # IPC graphs
    GraphTechnosAppli = nx.DiGraph() # IPC graphs
    GraphTechnosAuthor = nx.DiGraph() # IPC graphs
    
    # TypeBre = dict()
    
    for bre in df.itertuples():
    
    
        GraphBrevets.add_node(bre .label)
        GraphBrevetsCitations.add_node(bre .label)
        GraphBrevetsReferences.add_node(bre .label)
        GraphBrevetsEquivalents.add_node(bre .label)
        GraphTechnos .add_node(bre .label)
        for lab in bre.CitedBy:
            if len(lab)>0 and bool(lab.strip()):
                GraphBrevetsCitations.add_node(lab)
                GraphBrevetsCitations.add_edge(lab, bre.label)
        
                
        for lab in bre.CitP:
            if len(lab)>0 and bool(lab.strip()):
            
                GraphBrevetsReferences.add_node(lab)
                GraphBrevetsReferences.add_edge(bre.label, lab)
        for lab in bre.CitO:
            if len(lab)>0 and bool(lab.strip()):
            
                GraphBrevetsReferences.add_node(lab)
                GraphBrevetsReferences.add_edge(bre.label, lab)
        for lab in bre.equivalents :
            if len(lab)>0 and bool(lab.strip()):
            
                GraphBrevetsEquivalents.add_node(lab)
                GraphBrevetsEquivalents.add_edge(bre.label, lab)
        joliTecno = list(set([ipc.replace('/', '-') for ipc in bre.IPCR11]))
        for ipc in bre.IPCR1 + bre.IPCR4 + bre.IPCR7 + joliTecno:
            if bool(ipc.strip()):
                if ipc in dicoAttrsTechno:
                    if 'size' in dicoAttrsTechno [ipc].keys():
                        dicoAttrsTechno [ipc] ['size'] +=1
                    else:
                        dicoAttrsTechno [ipc] ['size'] = 1
                GraphTechnos .add_node(ipc)
                GraphTechnosAppli.add_node(ipc)
                GraphTechnosAuthor.add_node(ipc)
            
        for ipc in joliTecno:
            if bool(ipc.strip()):
                for ipcUp in bre.IPCR7:
                    
                    if ipc.startswith (ipcUp) and  bool(ipcUp.strip()):
                        GraphTechnos .add_edge(ipcUp, ipc)
                        GraphTechnosAppli .add_edge(ipcUp, ipc)
                        GraphTechnosAuthor .add_edge(ipcUp, ipc)        
        #for ipc in bre.IPCR7:
             #   if bool(ipc.strip()):
                    for ipcUpUp in bre.IPCR4:
                            if ipcUp.startswith (ipcUpUp) and  bool(ipcUpUp.strip()):
                                GraphTechnos .add_edge(ipcUp, ipcUpUp)
                                GraphTechnosAppli .add_edge(ipcUp, ipcUpUp)
                                GraphTechnosAuthor .add_edge(ipcUp, ipcUpUp)
            
                # for ipc in bre.IPCR4:
                #     if bool(ipc.strip()):
                            for ipcUpUpUp in bre.IPCR1:
                                    if ipcUpUp.startswith (ipcUpUp) and  bool(ipcUpUpUp.strip()):
                                        GraphTechnos .add_edge(ipcUpUp, ipcUpUpUp)
                                        GraphTechnos .add_edge(bre .label,ipcUpUpUp)  
                                        GraphTechnosAppli .add_edge(ipcUpUp, ipcUpUpUp)
                                        GraphTechnosAuthor .add_edge(ipcUpUp, ipcUpUpUp)
    
        if len(joliTecno) ==0:
            for ipcUp in bre.IPCR7:
                    
                    if bool(ipcUp.strip()):
                        GraphTechnos .add_edge(ipcUp, ipc)
                        GraphTechnosAppli .add_edge(ipcUp, ipc)
                        GraphTechnosAuthor .add_edge(ipcUp, ipc)
        #for ipc in bre.IPCR7:
             #   if bool(ipc.strip()):
                    for ipcUpUp in bre.IPCR4:
                            if ipcUp.startswith (ipcUpUp) and  bool(ipcUpUp.strip()):
                                GraphTechnos .add_edge(ipcUp, ipcUpUp)
                                GraphTechnosAppli .add_edge(ipcUp, ipcUpUp)
                                GraphTechnosAuthor .add_edge(ipcUp, ipcUpUp)
                # for ipc in bre.IPCR4:
                #     if bool(ipc.strip()):
                            for ipcUpUpUp in bre.IPCR1:
                                    if ipcUpUp.startswith (ipcUpUpUp) and  bool(ipcUpUpUp.strip()):
                                        GraphTechnos .add_edge(ipcUpUp, ipcUpUpUp)
                                        GraphTechnos .add_edge(bre .label,ipcUpUpUp)  
                                        GraphTechnosAppli .add_edge(ipcUpUp, ipcUpUpUp)
                                        GraphTechnosAuthor .add_edge(ipcUpUp, ipcUpUpUp)
        if len(bre.IPCR7) == 0:
            for ipcUpUp in bre.IPCR4:
                            if bool(ipcUpUp.strip()):
                                GraphTechnos .add_edge(ipcUp, ipcUpUp)
                                GraphTechnosAppli .add_edge(ipcUp, ipcUpUp)
                                GraphTechnosAuthor .add_edge(ipcUp, ipcUpUp)
                # for ipc in bre.IPCR4:
                #     if bool(ipc.strip()):
                            for ipcUpUpUp in bre.IPCR1:
                                    if ipcUpUp.startswith (ipcUpUpUp) and  bool(ipcUpUpUp.strip()):
                                        GraphTechnos .add_edge(ipcUpUp, ipcUpUpUp)
                                        GraphTechnosAppli .add_edge(ipcUpUp, ipcUpUpUp)
                                        GraphTechnosAuthor .add_edge(ipcUpUp, ipcUpUpUp)
                                        GraphTechnos .add_edge(bre .label,ipcUpUpUp)  
        
        # for ipc in bre.IPCR1 + bre.IPCR4 + bre.IPCR7 + joliTecno:
        #     if bool(ipc.strip()):
        #         if ipc in dicoAttrsTechno:
        #             if 'size' in dicoAttrsTechno [ipc].keys():
        #                 dicoAttrsTechno [ipc] ['size'] +=1
        #             else:
        #                 dicoAttrsTechno [ipc] ['size'] = 1
        #         GraphTechnos .add_node(ipc)
        #         GraphTechnosAppli.add_node(ipc)
        #         GraphTechnosAuthor.add_node(ipc)
        # for ipc in joliTecno:
        #     if bool(ipc.strip()):
        #         for ipcUp in bre.IPCR7:
                    
        #             if ipc.startswith (ipcUp) and  bool(ipcUp.strip()):
        #                 GraphTechnos .add_edge(ipcUp, ipc)
            
        # for ipc in bre.IPCR7:
        #     if bool(ipc.strip()):
        #         for ipcUp in bre.IPCR4:
        #             if ipc.startswith (ipcUp) and  bool(ipcUp.strip()):
        #                 GraphTechnos .add_edge(ipcUp, ipc)
        # for ipc in bre.IPCR4:
        #     if bool(ipc.strip()):
        #         for ipcUp in bre.IPCR1:
        #             if ipc.startswith (ipcUp) and  bool(ipcUp.strip()):
        #                 GraphTechnos .add_edge(ipcUp, ipc)
        
        # # for ipcUp in bre.IPCR1:    
        # #     GraphTechnos .add_edge(bre .label,ipcUp)
        # # chainning technlogy from most precise if existing
        # if len(joliTecno)>0:
        #     for ipc in joliTecno:
        #         if bool(ipc.strip()):
        #             GraphTechnos .add_edge(bre .label,ipc)
        # elif len(bre.IPCR7) >0:
        #     for ipc in bre.IPCR7:
        #         if bool(ipc.strip()):
        #             GraphTechnos .add_edge(bre .label,ipc)
        # elif len(bre.IPCR4) >0:
        #     for ipc in bre.IPCR4:
        #         if bool(ipc.strip()):
        #             GraphTechnos .add_edge(bre .label,ipc)
        # else:
        #     for ipc in bre.IPCR1:
        #         if bool(ipc.strip()):
        #             GraphTechnos .add_edge(bre .label,ipc)         
        
        if not isinstance( bre .applicant, str) and len( bre.applicant)>1:
             if sum([len( truc) for truc in bre .applicant]) == len(bre.applicant):
                 df.at [bre.Index, 'applicant' ] = [''.join (bre .applicant)]
             for appl in bre .applicant:
                 appl=appl.strip()
                 if len(appl) >0:
                     if len(joliTecno)>0:
                         for ipc in joliTecno:
                             GraphTechnosAppli .add_edge(appl,ipc)
                     elif len(bre.IPCR7) >0:
                         for ipc in bre.IPCR7:
                             GraphTechnosAppli .add_edge(appl,ipc)
                     elif len(bre.IPCR4) >0:
                         for ipc in bre.IPCR4:
                             GraphTechnosAppli .add_edge(appl,ipc) 
                     else:
                         for ipc in bre.IPCR1:
                             GraphTechnosAppli .add_edge(appl,ipc) 
                             
             if len(bre.applicant) >1:
                 for appl, coAut in cycle(bre.applicant):
                     appl=appl.strip()
                     coAut=coAut.strip()
                     if len(appl)>0 and appl.title() not in Inventeurs and NoPunct(appl).title() not in Inventeurs and appl.lower() != 'empty':
                         GraphBrevets.add_node(appl)
                         GraphBrevets.add_edge(appl, bre .label)
                         GraphApplicant.add_node(appl)
                         #GraphTechnosAppli.add_node(appl)
                         GraphAuteursAppli.add_node(appl)
                     if len(coAut)>0 and coAut.title() not in Inventeurs and NoPunct(coAut).title() not in Inventeurs and coAut.lower() != 'empty':
                         GraphBrevets.add_node(coAut)
                         GraphBrevets.add_edge(coAut, bre .label)
                         GraphBrevets.add_edge( appl, coAut)
                         GraphApplicant.add_node(coAut)
                         #GraphTechnosAppli.add_node(coAut)
                         GraphAuteursAppli.add_node(coAut)
        # elif len( bre.applicant)>0 and isinstance( bre .applicant, list):
        #     appl= bre.applicant [0].strip()
        #     if len(appl)>0 and appl.title() not in Inventeurs and NoPunct(appl).title() not in Inventeurs and appl.lower() != 'empty':
        #         GraphBrevets.add_node(appl)
        #         GraphBrevets.add_edge(appl, bre .label)
        #         # GraphApplicant.add_node(appl)
        #         GraphTechnosAppli.add_node(appl)
        #         GraphAuteursAppli.add_node(appl)
        #         if len(joliTecno)>0:
        #             for ipc in joliTecno:
        #                 GraphTechnosAppli .add_edge(appl,ipc)
        #         elif len(bre.IPCR7) >0:
        #             for ipc in bre.IPCR7:
        #                 GraphTechnosAppli .add_edge(appl,ipc)
        #         elif len(bre.IPCR4) >0:
        #             for ipc in bre.IPCR4:
        #                 GraphTechnosAppli .add_edge(appl,ipc) 
        #         else:
        #             for ipc in bre.IPCR1:
        #                 GraphTechnosAppli .add_edge(appl,ipc) 
        else:
            pass
    
    
        for aut in bre .inventor:
            aut= aut.title()
            GraphAuteurs.add_node(aut)
            GraphTechnosAuthor.add_node(aut)
            for ipc in joliTecno:
                GraphTechnosAuthor .add_edge(aut,ipc)
            if len(joliTecno)>0:
                for ipc in joliTecno:
                    GraphTechnosAuthor .add_edge(aut,ipc)
            elif len(bre.IPCR7) >0:
                for ipc in bre.IPCR7:
                    GraphTechnosAuthor .add_edge(aut,ipc)
            elif len(bre.IPCR4) >0:
                for ipc in bre.IPCR4:
                    GraphTechnosAuthor .add_edge(aut,ipc) 
            else:
                for ipc in bre.IPCR1:
                    GraphTechnosAuthor .add_edge(aut,ipc)             
        # chaining collaborations
        
        if isinstance(bre .inventor, list) and len( bre .inventor)>1:
            for aut, coAut in cycle( bre .inventor):
                aut= aut.title()
                coAut= coAut.title()
                
                GraphAuteurs.add_edge(aut, coAut, label = 'AuthorCollaboration')        
                GraphAuteursAppli.add_edge(aut, coAut, label = 'AuthorCollaboration') 
                    
        if isinstance(bre.applicant, list) and len( bre.applicant)>1: # many applicants
            
            #cycling collaborations
            for aut, coAut in cycle(bre .applicant):
                aut = aut.strip()
                coAut = coAut.strip()
                if len(aut) ==1:
                    print (aut)
                if len(coAut) == 1:
                    print(coAut)
                regles = [len(aut)>0, 
                          len(coAut) >0,
                          aut.title() not in Inventeurs,
                          NoPunct(aut).title() not in Inventeurs,
                          coAut.title() not in Inventeurs, 
                          NoPunct(coAut).title() not in Inventeurs
                    ]
                
                if all(regles):
                    aut= aut.upper()
                    coAut= coAut.upper()
                    GraphAuteursAppli.add_edge(aut, coAut, label = 'ApplicantCollaboration')
                    GraphApplicant.add_edge(aut, coAut)
            #chaining authors
            for appl in bre.applicant:
                if bool(appl.strip()):            
                    appl= appl.upper()
                    regles= [len(appl)>0,
                              appl.title() not in Inventeurs,
                              NoPunct(appl).title() not in Inventeurs, 
                              ]
                    if all(regles):
                        for aut in bre .inventor:
                            aut= aut.title()
                            GraphAuteursAppli.add_edge( aut, appl, label = 'workfor')
        elif len( bre.applicant)>0 and bool(bre.applicant[0].strip()): # only one applicant
            appl= bre.applicant[0].upper()
            regles= [len(appl)>0,
                          appl.title() not in Inventeurs,
                          NoPunct(appl).title() not in Inventeurs, 
                          ]
            if all(regles):
                    for aut in bre .inventor:
                        aut= aut.title()
                        GraphAuteursAppli.add_edge( aut, appl, label = 'workfor')
        else:
            pass
    
    
    
    
    
    NoeudAut = list(iter(GraphAuteurs))
    NoeudApplicant = list(iter(GraphApplicant))
    EdgesAut = list(iter(GraphAuteurs.edges()))
    EdgesAut2 = [orig + ' ' + dest for orig, dest in EdgesAut]
    EdgesApplicant = list(iter(GraphApplicant.edges()))
    EdgesApplicant2 = [orig + ' ' + dest for orig, dest in EdgesApplicant]
    NoeudApplicantInv = list(iter(GraphAuteursAppli))
    EdgeApplicantInv = list(iter(GraphAuteursAppli.edges()))
    EdgeApplicantInv2 = [orig + ' ' + dest for orig, dest in EdgeApplicantInv]
    Autnode_sizes = {aut:sum([1 for truc in EdgesAut if truc [0] == aut or truc [1] == aut]) for aut in dicoAttrsAut.keys()}
    
    Applicantnode_sizes = { appl: sum([1 for truc in EdgesApplicant if \
                                       truc [0] == appl or truc [1] == appl]) for appl in dicoAttrsAppli.keys()}
        
    ApplicantInvnode_sizes = { machin: sum([1 for truc in EdgeApplicantInv if truc [0] == machin or truc [1] == machin]) for machin in list(dicoAttrsAppli.keys())+list(dicoAttrsAut.keys())}
    nx.set_node_attributes(GraphApplicant,Applicantnode_sizes, 'size')
    nx.set_node_attributes(GraphAuteurs,Autnode_sizes, 'size')
    
    nx.set_node_attributes( GraphBrevetsCitations, dicoAttrsCitedBy) # graph of citing patents of patents from PU
    nx.set_node_attributes( GraphBrevetsCitations, dicoAttrs) # graph of citing patents of patents from PU
    nx.set_node_attributes(  GraphBrevetsReferences, dicoAttrsCitP) # graph of references from patents from PU includes patents and other references
    nx.set_node_attributes(  GraphBrevetsReferences, dicoAttrs)
    nx.set_node_attributes(  GraphBrevetsReferences, dicoAttrsOut )
    nx.set_node_attributes( GraphBrevetsEquivalents, dicoAttrsEquiv) # graph of equivalents
    nx.set_node_attributes( GraphBrevetsEquivalents, dicoAttrs)
    nx.set_node_attributes(GraphTechnos, dicoAttrs) # IPC graphs
    nx.set_node_attributes(GraphTechnos, dicoAttrsTechno) # IPC graphs
    nx.set_node_attributes(GraphTechnosAppli, dicoAttrsTechno)
    nx.set_node_attributes(GraphTechnosAppli, dicoAttrsAppli)
    nx.set_node_attributes( GraphTechnosAuthor, dicoAttrsTechno)
    nx.set_node_attributes( GraphTechnosAuthor, dicoAttrsAut)
    nx.set_node_attributes(GraphBrevets,dicoAttrs)
    nx.set_node_attributes(GraphBrevets,dicoAttrsAppli)
    nx.set_node_attributes(GraphApplicant,dicoAttrsAppli)
    nx.set_node_attributes(GraphAuteurs,dicoAttrsAut)
    nx.set_node_attributes(GraphAuteursAppli,dicoAttrsAut)
    nx.set_node_attributes(GraphAuteursAppli,dicoAttrsAppli)
    nx.set_node_attributes(GraphAuteursAppli,Applicantnode_sizes, 'size')
    nx.set_node_attributes(GraphAuteursAppli,Autnode_sizes, 'size')
    
    
    # nx.write_gexf(GraphAuteurs, ResultGephiPath+"/"+ndf+"_Inventors.gexf") # GraphAuteurs
    # nx.write_gexf(GraphApplicant, ResultGephiPath+"/"+ndf+"_Applicant.gexf") # 
    # nx.write_gexf(GraphBrevets, ResultGephiPath+"/"+ndf+"-GraphBrevets.gexf")
    # nx.write_gexf(GraphAuteursAppli, ResultGephiPath+"/"+ndf+"_ApplicantInventor.gexf")
    # nx.write_gexf(GraphBrevetsEquivalents, ResultGephiPath+"/"+ndf+"_Equivalents.gexf")
    # nx.write_gexf(GraphBrevetsReferences, ResultGephiPath+"/"+ndf+"_References.gexf")
    # nx.write_gexf(GraphBrevetsCitations, ResultGephiPath+"/"+ndf+"_Citations.gexf")
    # nx.write_gexf (GraphTechnos, ResultGephiPath+"/"+ndf+"_CrossTech.gexf")
    # nx.write_gexf (GraphTechnosAppli, ResultGephiPath+"/"+ndf+"_Applicants_CrossTech.gexf") 
    # nx.write_gexf (GraphTechnosAuthor, ResultGephiPath+"/"+ndf+"_Inventors_CrossTech.gexf")
    
    visu = 'neato'
    for G, network in [(GraphAuteurs, "_Inventors"),
              (GraphApplicant, "_Applicants"),
              (GraphBrevets, "_LabelApplicants"),
              (GraphAuteursAppli, "_ApplicantInventor"),
              (GraphBrevetsEquivalents, "_Equivalents"),
              (GraphBrevetsReferences, "_References"),
              (GraphBrevetsCitations, "_Citations"),
              (GraphTechnos,  "_CrossTech"),
              (GraphTechnosAppli, "_Applicants_CrossTech"),
              (GraphTechnosAuthor, "_Inventors_CrossTech")  ]:
        if len(G) == 0:
            continue
        # Maxdegs = max([G.degree[node] for node in G.nodes()])
        # # zoom = len(G) / Maxdegs
        # # arguDot='-Goverlap="0:prism" -Gsize="1000,800" -GLT=550 -GKsep='+str(zoom)
        pos = nx.spring_layout(G,k=2,iterations=20)
     #    pos = nx.graphviz_layout(G,prog=visu)
    #      Networks["_CountryCrossTech"] =  [configFile.CountryCrossTechNetwork, [ 'IPCR7', "country"]] # not finished yet
    # Networks[] =  [configFile.CrossTechNetwork, ['IPCR7']] # GraphTechnos
    # Networks[] =  [configFile.InventorCrossTechNetwork, ['IPCR7', "inventor-nice"]] # GraphTechnosAuthor
    # Networks[] =  [configFile.ApplicantCrossTechNetwork, ['IPCR7', "applicant-nice"]] # GraphTechnosAppli
    # Networks[] = [configFile.ApplicantInventorNetwork, ["applicant-nice", "inventor-nice"]] # GraphAuteursAppli
    # Networks[] =  [configFile.ApplicantNetwork, ["applicant-nice"]] # GraphApplicant
    # Networks[] =  [configFile.InventorNetwork, ["inventor-nice"]] # GraphAuteurs
    # Networks[] =  [configFile.References, [ 'label', 'CitP', "CitO"]] # GraphBrevetsReferences
    # Networks[] =  [configFile.Citations, [ 'label', "CitedBy"]] # GraphBrevetsCitations
    # Networks[] =  [configFile.Equivalents, [ 'label', "equivalents"]] # GraphBrevetsEquivalents
    # Networks[] =  [configFile.Equivalents, [ 'label', "applicant-nice"]] # GraphBrevetsEquivalents#GraphBrevets
    
        factx, facty = 1, 1 # neatto
        if len(pos)>0:
            MaxPosX = max([pos[k][0] for k in list(pos.keys())])
            MaxPosY = max([pos[k][1] for k in list(pos.keys())])
            MinPosX = min([pos[k][0] for k in list(pos.keys())])
            MinPosY = min([pos[k][1] for k in list(pos.keys())])
            GvScreenX = MaxPosX-MinPosX
            GvScreenY = MaxPosY-MinPosY
            factx = screenX/GvScreenX
            facty = screenY/GvScreenY
        else: #by the way this is an empty net
            MaxPosX = 200
            MaxPosY = 100
            MinPosX = -200
            MinPosY = -100
            GvScreenX = MaxPosX-MinPosX
            GvScreenY = MaxPosY-MinPosY
            factx = screenX/GvScreenX
            facty = screenY/GvScreenY
        if MinPosY>0:
            posx, posy = 0, -400
        else:
            posx, posy = 0, 0
    
         #one color for one kind of node
        size = len (Networks [network][1])
    
     #                   argu='-Goverlap="9:prism" -Gsize="1000,800" -Gdim=3 -Gdimen=2 -GLT=550 -GKsep='+str(zoom)
     #                   pos=nx.graphviz_layout(G,prog='sfdp', args = argu )
                #pos = nx.graphviz_layout(G, prog='dot', args = arguDot )
    
     #               pos = nx.spring_layout(G, dim=2, k=3, scale =1, iterations = 800)
               # pos = nx.spectral_layout(G, dim=2,scale =1)
    #                newCoord = project_points(pos[k][0], pos[k][1], pos[k][2], 0, 0, 1)
    #                Visu['position']= {'x':newCoord[0][0], 'y':newCoord[0][1], 'z':0}
    #                norme = np.linalg.norm(pos[k])
        cmpe = cmap_discretize(matplotlib.cm.jet, int(size))
        for k in G.nodes():
            #G.node[k]["weight"] = G.node[k]["weight"]['value'] # static net
            #G.node[k]["id"] = G.node[k]["id"]['id']
            Visu = dict()
            Visu['color'] = dict()
            #G.node[k]['label'] =  Nodes.keys()[k]
            #G.node[k]['category'] = Nodes[Nodes.keys()[k]]['category']
            if G.nodes[k]['category'] == 'label':
                G.nodes[k]['url'] =UrlPatent(k)[0]
                Visu['color']['a'] = 1
                Visu['color']['r']= int(254)
                Visu['color']['g']= int(0)
                Visu['color']['b']= int(0)
                Visu['shape'] ="diamond"
            elif G.nodes[k]['category'] =='CitP':
                    Visu['color']['a'] = 1
                    Visu['color']['r']= int(0)
                    Visu['color']['g']= int(254)
                    Visu['color']['b']= int(0)
                    Visu['shape'] ="ellipse"
    
            elif G.nodes[k]['category'] == 'CitO':
                # a hack here, trying to find out content in scholar
                #https:/scholar.google.fr/scholar?hl=fr&q=pipo+test&btnG=&lr=
                Visu['color']['r']= int(0)
                Visu['color']['g']= int(0)
                Visu['color']['b']= int(254)
                Visu['color']['a'] =1
                Visu['shape'] ="disc"
                #UrlTemp = "https:/scholar.google.com/scholar?q=" + quot(Nodes.keys()[k])
                #G.node[k]['url'] = UrlTemp
            elif G.nodes[k]['category'] == 'CitedBy':
                Visu['color']['a'] = 1
                Visu['color']['r']= int(0)
                Visu['color']['g']= int(127)
                Visu['color']['b']= int(127)
                Visu['shape'] ="square"
                G.nodes[k]['url'] =UrlPatent(k)[0]
    
            elif G.nodes[k]['category'] == "equivalents":
                Visu['color']['a'] = 1
                Visu['color']['r']= int(127)
                Visu['color']['g']= int(127)
                Visu['color']['b']= int(0)
                Visu['shape'] ="ellipse"
                G.nodes[k]['url'] =UrlPatent(k)[0]
            elif G.nodes[k]['category'] == 'Applicant':
                #G.node[k]['category'] = 'Applicant'# for readable facility
                if 'type' in G.nodes[k].keys():
                    if  G.nodes[k]['type'] == "Public":
                        
                        Visu['color']['a'] = 1
                        Visu['color']['r']= int(254)
                        Visu['color']['g']= int(60)
                        Visu['color']['b']= int(60)
                        Visu['shape'] ="star"
                    if  G.nodes[k]['type'] == "Private":
                        
                        Visu['color']['a'] = 1
                        Visu['color']['r']= int(60)
                        Visu['color']['g']= int(60)
                        Visu['color']['b']= int(254)
                        Visu['shape'] ="star"   
                else:
                    G.nodes[k]['url'] = UrlApplicantBuild(k)[0]
                    Visu['color']['a'] = 1
                    Visu['color']['r']= int(127)
                    Visu['color']['g']= int(0)
                    Visu['color']['b']= int(127)
                    Visu['shape'] ="disc"
                
                
            elif G.nodes[k]['category'] == 'IPCR1' or G.nodes[k]['category'] == 'IPCR3' or G.nodes[k]['category'] == 'IPCR4' or G.nodes[k]['category'] == 'IPCR7' or G.nodes[k]['category'] == 'IPCR11' or G.nodes[k]['category'] == 'CPC':
                G.nodes[k]['url'] = UrlIPCRBuild(k)[0]
                Visu['color']['a'] = 1
                Visu['color']['r']= int(127)
                Visu['color']['g']= int(254)
                Visu['color']['b']= int(127)
                Visu['shape'] ="database"
            elif G.nodes[k]['category'] == 'Inventor':
                #G.node[k]['category'] = 'inventor'# for readable facility
                G.nodes[k]['url'] = UrlInventorBuild(k)[0]
                Visu['color']['a'] = 1
                Visu['color']['r']= int(127)
                Visu['color']['g']= int(127)
                Visu['color']['b']= int(254)
                Visu['shape'] ="triangleDown"
            elif G.nodes[k]['category'] == 'AutFr':
                #G.node[k]['category'] = 'inventor'# for readable facility
                G.nodes[k]['url'] = UrlInventorBuild(k)[0]
                Visu['color']['a'] = 1
                Visu['color']['r']= int(254)
                Visu['color']['g']= int(127)
                Visu['color']['b']= int(60)
                Visu['shape'] ="triangleDown"
            elif G.nodes[k]['category'] == 'AutEtr':
                #G.node[k]['category'] = 'inventor'# for readable facility
                G.nodes[k]['url'] = UrlInventorBuild(k)[0]
                Visu['color']['a'] = 1
                Visu['color']['r']= int(127)
                Visu['color']['g']= int(60)
                Visu['color']['b']= int(254)
                Visu['shape'] ="triangleDown"            
            elif G.nodes[k]['category'] == 'PasSurPubMed':
                #G.node[k]['category'] = 'inventor'# for readable facility
                G.nodes[k]['url'] = UrlInventorBuild(k)[0]
                Visu['color']['a'] = 1
                Visu['color']['r']= int(127)
                Visu['color']['g']= int(254)
                Visu['color']['b']= int(60)
                Visu['shape'] ="triangleDown"        
            else:
                Visu['color']['a'] = 1
                Visu['color']['r']= int(254)
                Visu['color']['g']= int(254)
                Visu['color']['b']= int(0)
                Visu['shape'] ="image"
            # if "label" not in mixNet:
            #     mixNet.append('label')
            #factx, facty = 500, 400
            # if 'inventor' in G.node[k]['category'] or 'applicant' in G.node[k]['category']:
            #     categ = G.node[k]['category']+'-nice' # for readable facility
            #     count = mixNet.index(categ)
            # else:
            #     count = mixNet.index(G.node[k]['category'])
            count = Networks [network][1].index(G.nodes[k]['category'])
            Visu['position']= {'x':(int(pos[k][0]*factx)+posx), 'y':(int(pos[k][1]*facty)+posy), 'z':0.0}
            # Visu['size'] = np.log(int(G.node[k]["weight"])+1)+4#
            Visu['color']['a']= count
            G.nodes[k]['viz'] =dict()
    
    
        #            Visu['color']['a']= count
    
        #        Visu['size'] = (G.node[k]["degree"]*1.0)#(G.node[k]["degree"]*1.0/Maxdegs)*150#(G.node[k]["weight"]) /MaxWeight #addd 1 for viewiong all...
            #Visu['size'] = (G.node[k]["degree"]*zoom) +1 #(G.node[k]["weight"]) /MaxWeight #addd 1 for viewiong all...
            
    #        Visu['size'] = G.degree [k]*10.0/Maxdegs +4
        #        Visu['size'] = np.log(int(G.node[k]["weight"])+1)*zoom+1#
            for cle in list(Visu.keys()):
                G.nodes[k]['viz'][cle] = Visu[cle]
    
         #               print G.node[k]
         #       nx.set_node_attributes(G, 'weight', attr_dict)
    
        outputFile = ndf+network + 'JS.gexf'
    
        try:
            os.remove(ResultGephiPath+'/'+outputFile)
        except:
            try:
                os.remove(ResultGephiPath+'/'+outputFile)
            except:
                pass
    #
        nx.write_gexf(G, ResultGephiPath+'/'+outputFile, version='1.2draft')
        fic = open(ResultGephiPath+'/'+outputFile, 'r', encoding = 'utf8')
    
        # Next is a hack to correct the bad writing of the header of the gexf file
        # with dynamics properties
        fictemp=open(ResultGephiPath+'/'+"Good"+outputFile, 'w', encoding = 'utf8')
    
    
        ecrit = True
        data = fic.read()
        # VERY UGLY Hack here !!!!
        data = data.replace('ns0:', 'viz:') # may be someone knows how to set namespace in networkx...
        data = data.replace('a="None"', '') # may be someone knows why network set the "a" attribute...
        enTetOk = """<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2" xmlns:viz="http://www.gexf.net/1.2draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd">
    """
        enTetPasOk = """<gexf xmlns:ns0="http://www.gexf.net/1.2draft/viz" version="1.2" xmlns="http://www.gexf.net/1.2draft" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/2001/XMLSchema-instance">"""
        data  = data.replace(enTetPasOk,enTetOk)
        for lig in data.split('\n'):
            if lig.count('<nodes>'):
                ecrit = True
            if ecrit:
                fictemp.write(lig+'\n')
        fictemp.close()
        fic.close()
        try:
            #os.remove(ResultGephiPath+'\\'+ndf+'.gexf')
            os.remove(ResultGephiPath+'/'+outputFile)
        except:
            pass
    
        os.rename(ResultGephiPath+'/'+"Good"+outputFile, ResultGephiPath+'/'+outputFile)

RenderTemplate(
    "GraphIndex.html",
    configFile.ResultPath+"/GraphIndex"+ projectName+ ".html"
)

# making the js from model
# maybe we could adjust node size and other parameters here
RenderTemplate(
    "GraphUploadModel.html",
    configFile.ResultPath+"/GraphUpload.html",
    request=projectName,
    anglOpt = "{{loadingMessage=='' ? 'LOAD GRAPH' : loadingMessage}}"
)    
   
    
    
    
    
# secondes = time.time() - start_time

# heures, secondes = divmod(secondes, 3600)
# minutes, secondes = divmod(secondes, 60)
# print ('Duree : ', heures, " h ", minutes, " m et ", secondes, " sec")

