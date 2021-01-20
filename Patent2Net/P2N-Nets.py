# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 07:41:54 2019

@author: (c) 2020 The Patent2Net Developers
"""


import codecs
import os
import sys
import shutil
import pickle

from pymed import PubMed

from Patent2Net.P2N_Lib import LoadBiblioFile
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
       
configFile = LoadConfig()
# Les champs nécessaires par brevet.
NeededInfo = ['label', 'date', 'inventor', 'title', 'abstract']

requete = configFile.requete
projectName = configFile.ndf
ndf = projectName
BiblioPath = configFile.ResultBiblioPath
ResultBiblioPath = configFile.ResultBiblioPath
temporPath = configFile.temporPath
ResultGephiPath = configFile.ResultGephiPath

ResultPathContent= configFile.ResultContentsPath
ResultAbstractPath = configFile.ResultAbstractPath
Auteur = configFile.ResultPath + '//AcadCorpora'
RepDir = configFile.ResultPath + '//AcadCorpora'
project = RepDir
if 'AcadCorpora' not in os.listdir(configFile.ResultPath):
    print ("relancez le script de collecte (AcadPubMed.py 29/06/2019)")
    sys.exit()
if 'Description'+ndf in os.listdir(BiblioPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
    print( "loading patent biblio data with ", " and ".join(NeededInfo), " fields.")
    DataBrevet = LoadBiblioFile(BiblioPath, ndf)
    print("Hi this is AcadStats processor. Bibliographic data of ", ndf, " patent universe found.")
else:
    print ("relancez P2n pour collecter les données brevet")
    sys.exit()

print("Nice, ", len(DataBrevet["brevets"]), " patents found. On calcule les auteurs identifiés...")

# def Nettoie(Liste):
#     indesirables = ['', u'', None, False, [], ' ', "?", "Empty", "empty"]
#     Liste = [' '.join([truc.lower().title() for truc in nom.split(' ')]) for nom in Liste ] 
#     return list(filter(lambda x: x not in indesirables, Liste))



lstfic = os.listdir(configFile.ResultPath +'//AcadCorpora')
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

# with codecs.open(configFile.ResultPath +'//AcadCorpora//AuteursAffil.csv', 'r', 'utf8') as fic:
#     data = fic.readlines()
# multiAut = 0  # inventeurs prolixes
# AffilDiff = 0   # les affiliations différentes
# Auteurs = dict()
# for lig in data:
#     col = lig   .strip()
#     col = col.split(';')
#     if col[0].title() in InvNormes:
#         if col[0].title() in Inventeur_Norm.keys():
#             Auteurs [ col[0].title()] = col[1]
#         elif NoPunct(col[0].title()) in Inventeur_Norm.keys():
#             Auteurs [NoPunct(col[0].title())] = col[1]
            
#         else:
#             Auteurs [[cle.title() for cle in Inventeur_Norm.keys() if col[0].title() in Inventeur_Norm[cle]][0].title()] = col[1]
#     if col[0].title() not in Auteurs.keys():
#         Auteurs [col[0].title()] = col[1]
#     elif NoPunct(col[0].title()) not in Auteurs.keys():
#         Auteurs [NoPunct(col[0].title())] = col[1]
#     else:
#         if col[1] != Auteurs [col[0].title()] and '???' not in col[1]:
#             print (col[0], " --> ", Auteurs [col[0]])
#             print (col[0], " --> ", col[1])
            
#             AffilDiff +=1
#             multiAut+=1  # non sens, le script peut recollecter plusieurs fois le même
#         else:
#             multiAut+=1
#             pass
Auteurs = dict()
with open(RepDir + "//AuteursMatches.tsv", "r", encoding = 'utf8') as ficMatch:
    DataMatch = ficMatch.readlines()[1:]
PubMedAuct = []

for lig in DataMatch:
    col = lig.strip().split("\t")
    if col[0] not in Auteurs.keys():
        Auteurs [col[0]] = dict()
    else:
        print ("pb here")
    Auteurs [col[0]]["publisMatch"] = int(col [1])
    Auteurs [col[0]]["publis"] = int(col [2])
    Auteurs [col[0]]["Score moyen"] = float(col [3])
    PubMedAuct.append(col[0])
    

with open(RepDir + "//AuteursPAsMatches.tsv", "r", encoding = 'utf8') as ficMatch:
    DataPasMatch = ficMatch.readlines()[1:]

for lig in DataPasMatch:
    col = lig.strip().split("\t")
    if col[0] not in Auteurs.keys():
        Auteurs [col[0]] = dict()
    else:
        print ("big pb here")
    Auteurs [col[0]]["publisMatch"] = 0
    Auteurs [col[0]]["publis"] = 0
    Auteurs [col[0]]["Score moyen"] = 0
    PubMedAuct.append(col[0])
    
with open(Auteur+'//traceAuct.csv', 'r',) as fic:
    dataAuct = fic.readlines()
    if 'Nombre publications' in dataAuct [0]:
        dataAuct = dataAuct [1:]

for lig in dataAuct:
    lig = lig.strip()
    col= lig.split(';')
    if col[0] not in Auteurs.keys():
        Auteurs [col[0]] = dict()
        Auteurs [col[0]]['publis'] =  int(col [1])
        Auteurs [col[0]]['publisMatch'] = int(col [2])
        Auteurs [col[0]]['affilFr'] = col [3]
    else: # merging
        Auteurs [col[0]]['publis'] += int(col [1])
        Auteurs [col[0]]['publisMatch'] += int(col [2])
        Auteurs [col[0]]['affilFr'] = col [3]


for fic in [ndf, 'Families'+ndf]:
    print("\n> Hi! This is Net processor used on:", fic)
    if 'Description' + fic in os.listdir(ResultBiblioPath):
        with open(ResultBiblioPath + '//' + fic, 'r') as data:
            dico = LoadBiblioFile(ResultBiblioPath, fic)
    else:  # Retrocompatibility
        print("please use Comptatibilizer")
        sys.exit()
    LstBrevet = dico['brevets']

    for bre in LstBrevet:
        Auctorial = []
        if isinstance(bre['inventor'], list):
            tempoinv = []
            for inv in bre['inventor']:
                if ''.join(bre['inventor']).strip().lower() == 'empty':
                    bre['inventor'] = []
                    bre['inventor-nice'] = []
                elif inv.title() in Inventeur_Norm.values():
                    inv = [cle for cle in  Inventeur_Norm.keys() if inv in Inventeur_Norm [cle]][0].title()
                    tempoinv.append(inv.title())
                else:
                    tempoinv.append(inv.title())
            bre['inventor'] = tempoinv
            Auctorial = [aut.title() in Auteurs.keys() for aut in bre['inventor']]
            
        elif bre['inventor'].strip().lower() == 'empty' or len(bre['inventor'].strip().lower()) ==0:
            bre['inventor'] = []
            bre['inventor-nice'] = []
        else:
            pass
        bre ['auct'] = Auctorial
        if isinstance(bre['applicant'], list):
            
            
            if ''.join(bre['applicant']).strip().lower() == 'empty':
                bre['applicant'] = []
                bre['applicant-nice'] = []
            Auctorial = [aut.title() in Auteurs.keys() for aut in bre['applicant']]
            if len(bre['applicant'])>0:
                tempoAppl = []
                for appl in bre['applicant']:
                    if appl.title() in bre ['inventor']:
                        pass
                    else:
                        tempoAppl.append(appl)
                bre['applicant'] = tempoAppl
        elif bre['applicant'].strip().lower() == 'empty':
            bre['applicant'] = []
            bre['applicant-nice'] = []
        else:
            pass
        
        bre ['auctAppli'] = Auctorial
        with open(ResultBiblioPath + '//tempo' + fic,  'ab') as ficRes:
            pickle.dump(bre, ficRes)
    os.remove(ResultBiblioPath + '//' + fic)
    shutil.move(ResultBiblioPath + '//tempo' + fic, ResultBiblioPath + '//' + fic)
    if 'Families' in fic:
        df_Fam = pd.DataFrame(LstBrevet)
    else:
        df = pd.DataFrame(LstBrevet)

for aut in Auteurs.keys():
    if 'affilFr' not in Auteurs [aut].keys():
        Auteurs [aut]['affilFr'] = False
AuteursFr = [cle for cle in Auteurs.keys() if Auteurs[cle]['affilFr'] == 'True']#{cle for cle, val in Auteurs.items() if "france" in val.lower()}
AuteursNotFr = [cle for cle in Auteurs.keys() if Auteurs[cle]['affilFr'] == 'False']

Applis = []
Techno = dict()

df ['family lenght'] = 0
df ['AutorFr'] = 0
df ['IPCR11-range'] = df ['IPCR11'].apply(len)
df ['IPCR4-range'] = df ['IPCR4'].apply(len)
df ['IPCR7-range'] = df ['IPCR7'].apply(len)
def cycle (liste):
    tempo = []
    if len(liste) < 1:
        return None
    else:
        taille = len(liste)-1
        for indice in range(taille):
            tempo.append((liste [indice], liste[indice+1]))
        return tempo
AuteursFr2 = []
for aut in AuteursFr:
    AuteursFr2.extend(aut.split(' '))

for bre in df['label']:
    try:
        df['family lenght'].loc[df.index[df['label'] == bre]] =  df_Fam['family lenght'].loc[df_Fam.index[df_Fam['label'] == bre]].values[0]
    except:
        df['family lenght'].loc[df.index[df['label'] == bre]] =  0 #df_Fam['family lenght'].loc[df_Fam.index[bre in df_Fam['equivalents']]].values[0]
#        print (df_Fam['family lenght'].loc[df_Fam.index[df_Fam['label'] == bre]])
    if len(df['inventor'].loc[df.index[df['label'] == bre]])>0:
        for inv in df['inventor'].loc[df.index[df['label'] == bre]].values[0]:
            if len(inv)>0:
                if inv in AuteursFr :
                    df .loc[df.index[df['label'] == bre], ['AutorFr']] += 1

Inventeurs = set()
for bre in DataBrevet  ['brevets']:
    for appl in  bre['applicant']:
        if len(appl) ==1:
            print("encore des données pas bonnes !")
        appl=appl.upper()
        if appl in Techno.keys():
            for cib in bre ['IPCR11']:
                Techno[appl].append(cib)
        else:
            Techno[appl] =  [cib for cib in bre ['IPCR11']]  
    if not isinstance(bre ['inventor'], list):
        bre ['inventor'] = [bre ['inventor']]
    for inv in bre ['inventor']:
        if len(inv) ==1:
            print("ARFFFFF")
        Inventeurs.add(inv.title())
        Techno[inv.title()] =  [cib for cib in bre ['IPCR11']] 
        if inv not in Auteurs.keys() and inv.title() not in Auteurs.keys():
            #authors coming from "families sets"
            print ('GRRR: ', inv)
            Auteurs [inv] = {'publis': -1, 'publisMatch': 0, 'affilFr': 'False'}
GraphAuteurs = nx.DiGraph()
GraphApplicant = nx.DiGraph()
GraphBrevets = nx.DiGraph()
GraphAuteursAppli = nx.DiGraph()
# TypeBre = dict()
dicoAttrs = dict()
dicoAttrsAut = dict()
for bre in DataBrevet['brevets']:
    # if len(df['family lenght'].loc[df.index[df['label'] == bre['label']]])>0:
    #     famille = df['family lenght'].loc[df.index[df['label'] == bre['label']]].values[0]
    # else:
    #     famille = 0
    

    dicoAttrs [bre['label']] = {'famille': df['family lenght'].loc[df.index[df['label'] == bre['label']]].values[0],
                                'IPC11-range': df['IPCR11-range'].loc[df.index[df['label'] == bre['label']]].values[0],
                                'IPC7-range': df['IPCR7-range'].loc[df.index[df['label'] == bre['label']]].values[0],
                                'IPC4-range': df['IPCR4-range'].loc[df.index[df['label'] == bre['label']]].values[0],
                                'Citations' : bre['Citations'],
                                "type" : 'brevet',
                                'NbBrevets' : 1
                                }
    GraphBrevets.add_node(bre ['label'])
    bre['applicant'] = list(set( bre['applicant']))
    for appl in  bre['applicant']:
        if len(appl)>0 and appl.title() not in Inventeurs and NoPunct(appl).title() not in Inventeurs:
             appl=appl.upper()
             Applis.append(appl)
             if isinstance( bre['applicant'], str):
                 pass
             else:
                 for coAut in bre['applicant']:
                     if coAut.title() not in Inventeurs and NoPunct(coAut).title() not in Inventeurs: 
                         GraphApplicant.add_node(appl, attrs={'public': appl in Public})
                         GraphAuteursAppli.add_node(appl)
                         coAut = coAut.upper()
                         if coAut!= appl and len(coAut)>1:
                              GraphApplicant.add_edge(appl, coAut)
                              GraphAuteursAppli.add_edge(appl, coAut, label = 'ApplicantCollaboration')
                              # is this necessary ??? (up to line 319 ?)
                               
                              GraphAuteursAppli.add_node(coAut)
                              if coAut in Public:
                                 typeAppl = 'Public'
                              else:
                                 typeAppl = 'Privé'
                              
                              
                              if coAut in dicoAttrs.keys():
                                  dicoAttrs [coAut] = {"type" : typeAppl,
                                         'famille': dicoAttrs [coAut]['famille']+ df['family lenght'].loc[df.index[df['label'] == bre['label']]].values[0],
                                         'IPC11-range': dicoAttrs [coAut]['IPC11-range']+ df['IPCR11-range'].loc[df.index[df['label'] == bre['label']]].values[0],
                                         'IPC7-range': dicoAttrs [coAut]['IPC7-range']+ df['IPCR7-range'].loc[df.index[df['label'] == bre['label']]].values[0],
                                         'IPC4-range': dicoAttrs [coAut]['IPC4-range']+ df['IPCR4-range'].loc[df.index[df['label'] == bre['label']]].values[0],
                                         'IPCDiversity': len(set(Techno [coAut])),
                                         'IPCForce' : len(Techno [coAut]) / (dicoAttrs [coAut]['NbBrevets'] + 1),
                                         #'isPublic': appl in Public,
                                         #'isAuthor':    appl.title() in Auteurs.keys(),
                                         'Citations' : dicoAttrs [coAut]['Citations'] + bre['Citations'],
                                         'NbBrevets' : dicoAttrs [coAut]['NbBrevets'] + 1}
                              else:
                                 dicoAttrs [coAut] = {"type" : typeAppl,
                                         'famille': df['family lenght'].loc[df.index[df['label'] == bre['label']]].values[0],
                                         'IPC11-range': df['IPCR11-range'].loc[df.index[df['label'] == bre['label']]].values[0],
                                         'IPC7-range': df['IPCR7-range'].loc[df.index[df['label'] == bre['label']]].values[0],
                                         'IPC4-range': df['IPCR4-range'].loc[df.index[df['label'] == bre['label']]].values[0],
                                         'IPCDiversity': len(set(Techno [coAut])),
                                         'IPCForce' : len(Techno [coAut]),
                                        # 'isPublic': appl in Public,
                                        # 'isAuthor':    appl.title() in Auteurs.keys(),
                                         'Citations' : bre['Citations'],
                                         'NbBrevets' : 1}
                 
             GraphBrevets.add_node(appl)
             if appl in Public:
                 typeAppl = 'Public'
             else:
                 typeAppl = 'Privé'
             if appl in dicoAttrs.keys():
                 dicoAttrs [appl] = {"type" : typeAppl,
                                     'famille': dicoAttrs [appl]['famille']+ df['family lenght'].loc[df.index[df['label'] == bre['label']]].values[0],
                                     'IPC11-range': dicoAttrs [appl]['IPC11-range']+ df['IPCR11-range'].loc[df.index[df['label'] == bre['label']]].values[0],
                                     'IPC7-range': dicoAttrs [appl]['IPC7-range']+ df['IPCR7-range'].loc[df.index[df['label'] == bre['label']]].values[0],
                                     'IPC4-range': dicoAttrs [appl]['IPC4-range']+ df['IPCR4-range'].loc[df.index[df['label'] == bre['label']]].values[0],
                                     'IPCDiversity': len(set(Techno [appl])),
                                     'IPCForce' : len(Techno [appl]) / (dicoAttrs [appl]['NbBrevets'] + 1),
                                     #'isPublic': appl in Public,
                                     #'isAuthor':    appl.title() in Auteurs.keys(),
                                     'Citations' : dicoAttrs [appl]['Citations'] + bre['Citations'],
                                     'NbBrevets' : dicoAttrs [appl]['NbBrevets'] + 1}
             else:
                 dicoAttrs [appl] = {"type" : typeAppl,
                                     'famille': df['family lenght'].loc[df.index[df['label'] == bre['label']]].values[0],
                                     'IPC11-range': df['IPCR11-range'].loc[df.index[df['label'] == bre['label']]].values[0],
                                     'IPC7-range': df['IPCR7-range'].loc[df.index[df['label'] == bre['label']]].values[0],
                                     'IPC4-range': df['IPCR4-range'].loc[df.index[df['label'] == bre['label']]].values[0],
                                     'IPCDiversity': len(set(Techno [appl])),
                                     'IPCForce' : len(Techno [appl]),
                                    # 'isPublic': appl in Public,
                                    # 'isAuthor':    appl.title() in Auteurs.keys(),
                                     'Citations' : bre['Citations'],
                                     'NbBrevets' : 1}
             
             GraphBrevets.add_edge(appl, bre ['label'])
             
        if appl in Techno.keys():
            for cib in bre ['IPCR11']:
                Techno[appl].append(cib)
        else:
            Techno[appl] =  [cib for cib in bre ['IPCR11']]        
        
            
    for aut in bre['inventor']:
        aut= aut.title()
        GraphAuteurs.add_node(aut, attrs={'AutFr': aut.title() in AuteursFr})
        if aut in dicoAttrsAut.keys():
            if dicoAttrsAut [aut]['AutFr']:
                typeAut = 'AutFr'
            elif not dicoAttrsAut [aut]['AutFr']:
                typeAut = 'AutEtr'
            else:
                typeAut = 'PasSurPubMed'
            dicoAttrsAut [aut] = {'AutFr': dicoAttrsAut [aut]['AutFr'],
                                  'Citations' : dicoAttrsAut [aut]['Citations'] + bre['Citations'],
                                  'Famille' : df['family lenght'].loc[df.index[df['label'] == bre['label']]].values[0],
                                  'type' : typeAut,
                                  'NbBrevets' : dicoAttrsAut [aut]['NbBrevets'] +1,
                                  'IPC11-range' :Techno[aut],
                                  'IPC7-range' : Techno[aut],
                                  'IPC4-range' : Techno[aut],
                                  'IPCDiversity': len(set(Techno [aut])),
                                  'IPCForce' : len(Techno [aut])
                                }
        else:
                
                dicoAttrsAut [aut] = {'AutFr': aut.title() in AuteursFr,
                          'Citations' : bre['Citations'],
                          'Famille' : df['family lenght'].loc[df.index[df['label'] == bre['label']]].values[0],
                          'NbBrevets' : 1,
                          'IPC11-range' : Techno[aut],
                          'IPC7-range' : Techno[aut],
                          'IPC4-range' : Techno[aut],
                          'IPCDiversity': len(set(Techno [aut])),
                          'IPCForce' : len(Techno [aut])
                        }
                if dicoAttrsAut [aut]['AutFr']:
                    typeAut = 'AutFr'
                elif not dicoAttrsAut [aut]['AutFr']:
                    typeAut = 'AutEtr'
                else:
                    typeAut = 'PasSurPubMed'
                dicoAttrsAut [aut] ['type'] = typeAut


    # chaining collaborations
    
    if isinstance(bre['inventor'], list) and len( bre['inventor'])>1:
        for aut, coAut in cycle(bre['inventor']):
            aut= aut.title()
            coAut= coAut.title()
            
            GraphAuteurs.add_edge(aut, coAut, label = 'AuthorCollaboration')        
            GraphAuteursAppli.add_edge(aut, coAut, label = 'AuthorCollaboration') 
                
    if isinstance(bre['applicant'], list) and len( bre['applicant'])>1:
        #cycling collaborations
        for aut, coAut in cycle(bre['applicant']):
            aut = aut.strip()
            coAut = coAut.strip()
            regles = [aut.title() not in Inventeurs,
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
        for appl in bre['applicant']:
                        
            appl= appl.upper()
            regles= [len(appl)>0,
                      appl.title() not in Inventeurs,
                      NoPunct(appl).title() not in Inventeurs, 
                      ]
            if all(regles):
                for aut in bre['inventor']:
                    aut= aut.title()
                    GraphAuteursAppli.add_edge( aut, appl, label = 'workfor')
    elif len( bre['applicant'])>1:
        appl= bre['applicant'].upper()
        regles= [len(appl)>0,
                      appl.title() not in Inventeurs,
                      NoPunct(appl).title() not in Inventeurs, 
                      ]
        if all(regles):
                for aut in bre['inventor']:
                    aut= aut.title()
                    GraphAuteursAppli.add_edge( aut, appl, label = 'workfor')
    else:
        pass
#     if CheckListInclu(bre['applicant'], Public):
#         bre ['type'] = "univ"
#     elif CheckListExclu(bre['applicant'], Public):  
#         bre ['type'] = "indus"
#     else:
#         bre ['type'] = "collab"

# create median values for appl attributes
TailleFamiile = 0
NbBrevets = 0
nbCitations = 0
IPC11 =0
IPC7 = 0
IPC4 = 0
IPCForce = []
for appl in set(Applis):
    Techno [appl] = list(filter(lambda x: x !='', Techno [appl]))
    dicoAttrs [appl] = {"type" : dicoAttrs [appl]["type"] ,
                        'famille': dicoAttrs [appl]['famille'],
                        'IPC11-range': dicoAttrs [appl]['IPC11-range'],
                        'IPC7-range': dicoAttrs [appl]['IPC7-range'],
                        'IPC4-range': dicoAttrs [appl]['IPC4-range'],
                        'IPCDiversity': len(set(Techno [appl])),
                        'IPCForce' : len(Techno [appl]),
                        'Citations' : dicoAttrs [appl]['Citations'],
                        'NbBrevets' : dicoAttrs [appl]['NbBrevets'],
                        'MedFamille': dicoAttrs [appl]['famille']/ dicoAttrs [appl]['NbBrevets'],
                        'MedIPC11-range': dicoAttrs [appl]['IPC11-range']/ dicoAttrs [appl]['NbBrevets'],
                        'MedIPC7-range': dicoAttrs [appl]['IPC7-range']/ dicoAttrs [appl]['NbBrevets'],
                        'MedIPC4-range': dicoAttrs [appl]['IPC4-range']/ dicoAttrs [appl]['NbBrevets'],
                        'MedIPCDiversity': len(set(Techno [appl]))/ dicoAttrs [appl]['NbBrevets'],
                        'MedIPCForce' : len(Techno [appl]) / dicoAttrs [appl]['NbBrevets'],
                        'MedCitations' : dicoAttrs [appl]['Citations']/ dicoAttrs [appl]['NbBrevets'],
                        'MedNbBrevets' : dicoAttrs [appl]['NbBrevets']/ dicoAttrs [appl]['NbBrevets']
                                     }

    TailleFamiile += dicoAttrs [appl]['famille']
    NbBrevets += dicoAttrs [appl]['NbBrevets']
    nbCitations += dicoAttrs [appl]['Citations']
    IPC11 +=dicoAttrs [appl]['IPC11-range']
    IPC7 += dicoAttrs [appl]['IPC7-range']
    IPC4 +=dicoAttrs [appl]['IPC4-range']
    IPCForce += Techno [appl]

lstFr= [truc.split('-')[1] for truc in os.listdir(configFile.ResultPath +'//AcadCorpora/Fr')]
lstEtr= [truc.split('-')[1] for truc in os.listdir(configFile.ResultPath +'//AcadCorpora/NoFr')]
for appl in Inventeurs:
        Techno [appl] = list(filter(lambda x: x !='', Techno [appl]))
        appl=appl.title()
        TailleFamiileAut = dicoAttrsAut [appl]['Famille']
        NbBrevetsAut = dicoAttrsAut [appl]['NbBrevets']
        nbCitationsAut = dicoAttrsAut [appl]['Citations']
        IPC11Aut = len(dicoAttrsAut [appl]['IPC11-range'])
        IPC7Aut = len(dicoAttrsAut [appl]['IPC7-range'])
        IPC4Aut = len(dicoAttrsAut [appl]['IPC4-range'])
        IPCForceAut = len(Techno [appl])
        dicoAttrsAut [appl] = {'AutFr': appl.title() in AuteursFr,
                      'Citations' : nbCitationsAut,
                      'Famille' : TailleFamiileAut,
                      'type' : dicoAttrsAut [appl]['type'],
                      'NbBrevets' : 1,
                      'IPC11-range' : IPC11Aut,
                      'IPC7-range' : IPC7Aut,
                      'IPC4-range' : IPC4Aut,
                      'IPCDiversity': len(set(Techno [appl])),
                      'IPCForce' : IPCForceAut
                    }
    
for aut in Auteurs.keys():
    #if aut in PubMedAuct:
   # pas forcément vrai j'ai dû zapper cette info dans le traitement
    # on retrouve les étrangers dans le dossier et fait un check par leur nom... tordu
       if aut.replace(' ','') in lstFr and aut.replace(' ','') not in lstEtr:
           typeAut = 'AutFr'
       elif aut.replace(' ','') in lstEtr and aut.replace(' ','') not in lstFr:
           typeAut = 'AutEtr'


       elif aut.replace(' ','') not in lstFr and aut.replace(' ','') not in lstEtr:    
           typeAut = 'PasSurPubMed'    
       
       elif aut in AuteursFr:
           typeAut = 'AutFr'
       else:
           typeAut = 'AutEtr'
    
           
       if aut in  dicoAttrsAut.keys():
           dicoAttrsAut [aut] ['type'] = typeAut

        
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


tailleCrp = len(DataBrevet  ['brevets'])
ligne = str(tailleCrp) +';'
if tailleCrp ==0:
    tailleCrp =1
# [aut for aut in dicoAttrsAut.keys() if dicoAttrsAut[aut]["type"]=="PasSurPubMed"]
ligne +=    str(NbBrevets) +';'+\
        str(len(set(Applis)))+';'+\
        str(len(dicoAttrsAut.keys())) +';'+\
        str(len([aut for aut in dicoAttrsAut.keys() if dicoAttrsAut[aut]["type"] =="AutFr"]))  +';'+\
        str(len([aut for aut in dicoAttrsAut.keys() if dicoAttrsAut[aut]["type"]=="AutEtr"])) +';'+\
        str(len([aut for aut in dicoAttrsAut.keys() if dicoAttrsAut[aut]["type"]=="PasSurPubMed"]))+ ';'+\
        str(TailleFamiile) +';'+\
        str(nbCitations) +';'+\
        str(IPC11) +';'+\
        str(IPC7) +';'+\
        str(IPC4) +';'+\
        str(IPCForce) +';'+\
        str(IPCDiversity) +';' +\
        str(NbBrevets/tailleCrp)+';' +\
        str(len(set(Applis))/tailleCrp)+';'+\
        str(len(dicoAttrsAut.keys())/tailleCrp) +';'+\
        str(len([aut for aut in dicoAttrsAut.keys() if dicoAttrsAut[aut]["type"] =="AutFr"])/tailleCrp)  +';'+\
        str(len([aut for aut in dicoAttrsAut.keys() if dicoAttrsAut[aut]["type"]=="AutEtr"])/tailleCrp) +';'+\
        str(len([aut for aut in dicoAttrsAut.keys() if dicoAttrsAut[aut]["type"]=="PasSurPubMed"])/tailleCrp)+ ';'+\
        str(TailleFamiile/tailleCrp) +';'+\
        str(nbCitations/tailleCrp) +';'+\
        str(IPC11/tailleCrp) +';'+\
        str(IPC7/tailleCrp) +';'+\
        str(IPC4/tailleCrp) + ';\n'
        
        
        

        
            
with open(ResultGephiPath+ '/'+ndf + 'stats.csv', "w") as ficStats:
    ficStats.write('Taille;NbBrevetsAppl;Nb Appl;NbInventeurs;NbAuteursAffilFr;NbInvAuteurNot Fr;Nb Inv pas sur PubMed;Taille Famille;nbCitations;IPC11;IPC7;IPC4;IPCForce;IPC diversity;NbBrevetAppliNorm;Nb ApplNorm;NbInventeursNorm;NbAuteursAffilFrNorm;NbInvAuteurNot FrNorm;Nb Inv pas sur PubMedNorm;Taille FamilleNorm;nbCitationsNorm;IPC11Norm;IPC7Norm;IPC4Norm;\n')
    ficStats.write(ligne)



with open('../DATA/'+ndf + 'stats.csv', "w") as ficStats:
    ficStats.write('Taille;NbBrevetsAppl;Nb Appl;NbInventeurs;NbAuteursAffilFr;NbInvAuteurNot Fr;Nb Inv pas sur PubMed;Taille Famille;nbCitations;IPC11;IPC7;IPC4;IPCForce;IPC diversity;NbBrevetAppliNorm;Nb ApplNorm;NbInventeursNorm;NbAuteursAffilFrNorm;NbInvAuteurNot FrNorm;Nb Inv pas sur PubMedNorm;Taille FamilleNorm;nbCitationsNorm;IPC11Norm;IPC7Norm;IPC4Norm;\n')
    ficStats.write(ligne)



NoeudAut = list(iter(GraphAuteurs))
NoeudApplicant = list(iter(GraphApplicant))
EdgesAut = list(iter(GraphAuteurs.edges()))
EdgesAut2 = [orig + ' ' + dest for orig, dest in EdgesAut]
EdgesApplicant = list(iter(GraphApplicant.edges()))
EdgesApplicant2 = [orig + ' ' + dest for orig, dest in EdgesApplicant]
Autnode_sizes = {aut:sum([truc.count(aut) for truc in EdgesAut2]) for aut in set(NoeudAut)}
Applicantnode_sizes = { appl: sum([truc.count(appl) for truc in EdgesApplicant2]) for appl in set(NoeudApplicant)}

nx.set_node_attributes(GraphApplicant,Applicantnode_sizes, 'size')
nx.set_node_attributes(GraphAuteurs,Autnode_sizes, 'size')


nx.set_node_attributes(GraphBrevets,dicoAttrs)
nx.set_node_attributes(GraphApplicant,dicoAttrs)
nx.set_node_attributes(GraphAuteurs,dicoAttrsAut)
nx.set_node_attributes(GraphAuteursAppli,dicoAttrsAut)
nx.set_node_attributes(GraphAuteursAppli,dicoAttrs)


try:
    nx.write_gexf(GraphAuteurs, ResultGephiPath+"/"+ndf+"-GraphAuteurs.gexf")
    nx.write_gexf(GraphApplicant, ResultGephiPath+"/"+ndf+"-GraphApplicant.gexf")
    nx.write_gexf(GraphBrevets, ResultGephiPath+"/"+ndf+"-GraphBrevets.gexf")
    nx.write_gexf(GraphAuteursAppli, ResultGephiPath+"/"+ndf+"-GraphAppliAuteurs.gexf")
except:
    pass

nx.write_gexf(GraphAuteurs, "../DATA/"+ndf+"-GraphAuteurs.gexf")
nx.write_gexf(GraphApplicant, "../DATA/"+ndf+"-GraphApplicant.gexf")
nx.write_gexf(GraphBrevets, "../DATA/"+ndf+"-GraphBrevets.gexf")
nx.write_gexf(GraphAuteursAppli, "../DATA/"+ndf+"-GraphAppliAuteurs.gexf")





# normalisation du jeu de brevets sur les noms d'inventeurs
# BrevNorm = []
# for bre in DataBrevet  ['brevets']:
#     tempoAut = []
#     for aut in bre['inventor']:
#         normAut = aut.upper()
#        # normAut = normAut.title()
#         if normAut in BadCasInv.keys():
#             tempoAut.append(BadCasInv [normAut])
#         else:
#             tempoAut.append(normAut)
            
#         if aut in bre ['applicant']:
#             bre ['applicant'].remove (aut)
#     bre['inventor'] = tempoAut
#     tempoApp = []
    # for app in bre['applicant']:
    #     normApp = app.upper()
    #     #normApp = normApp.title()
    #     if normApp in BadCasApp.keys():
    #         tempoApp.append(BadCasApp [normApp])
    #     else:
#     #         tempoApp.append(normApp)
#     # bre['applicant'] = tempoApp
# GraphAuteurs = nx.Graph()
# GraphApplicant = nx.Graph()
# # TypeBre = dict()
# for bre in DataBrevet  ['brevets']:
#     for aut in bre['inventor']:
#         for coAut in bre['inventor']:
#             if coAut!= aut:
#                 GraphAuteurs.add_edge(aut, coAut)        
    
# #     if CheckListInclu(bre['applicant'], Public):
# #         bre ['type'] = "univ"
# #     elif CheckListExclu(bre['applicant'], Public):  
# #         bre ['type'] = "indus"
# #     else:
# #         bre ['type'] = "collab"
#     for aut in bre['applicant']:
#         for coAut in bre['applicant']:
#             if coAut!= aut:
#                 GraphApplicant.add_edge(aut, coAut)
# #                 if bre ['type'] in TypeBre.keys():
# #                     TypeBre [bre ['type']]. append((aut, coAut))
# #                 else:
# #                     TypeBre [bre ['type']]= [(aut, coAut)]


# Mix = [bre for bre in DataBrevet['brevets'] if bre['type'] == 'collab']
# Univ = [bre for bre in DataBrevet['brevets'] if bre['type'] == 'univ']
# Indus = [bre for bre in DataBrevet['brevets'] if bre['type'] == 'indus']
#check consistance
# total = len(Mix) + len(Univ) + len(Indus)

# print (total -len(DataBrevet['brevets']))

# projectNameMix=projectName+'Mix'
# projectNameUniv=projectName+'Univ'
# projectNameIndus=projectName+'Indus'
# ficname =projectName

# ResultBiblioPath = '../DATA/'+projectNameMix+'/'+'PatentBiblios'
# ResultPath = '../DATA/'+projectNameMix
# if projectNameMix not in os.listdir('../DATA'):
#     os.makedirs(ResultBiblioPath)

# DataBrevet['ficBrevets'] = ficname +'Mix'
# DataBrevet['brevets'] = Mix
# ndf = ficname+'Mix'
# Data = dict()
# with open(ResultBiblioPath+'//Description'+ ndf, 'wb') as ficRes:
#     Data['ficBrevets'] = ndf 
#     Data['number'] = len(Mix)
#     Data['requete'] = DataBrevet['requete'] 
#     pickle.dump(Data, ficRes)

# with open(ResultBiblioPath+'/'+ ndf, 'ab') as ndfLstBrev:
#     for pat in Mix:
#         pickle.dump(pat , ndfLstBrev)
  

# ResultBiblioPath = '../DATA/'+projectNameUniv+'/'+'PatentBiblios'
# ResultPath = '../DATA/'+projectNameUniv
# if projectNameUniv not in os.listdir('../DATA'):
#     os.makedirs(ResultBiblioPath)

# # DataBrevet['ficBrevets'] = ficname +'Univ'
# # DataBrevet['brevets'] = Univ
# ndf = ficname+'Univ'
# Data = dict()
# with open(ResultBiblioPath+'/Description'+ ndf, 'wb') as ficRes:
#     Data['ficBrevets'] = ndf
#     Data['number'] = len(Univ)
#     Data['requete'] = DataBrevet['requete'] 
#     pickle.dump(Data, ficRes)

# with open(ResultBiblioPath+'/'+ ndf, 'ab') as ndfLstBrev:
#     for pat in Univ:
#         pickle.dump(pat , ndfLstBrev)
  
# ResultBiblioPath = '../DATA/'+projectNameIndus+'/'+'PatentBiblios'
# ResultPath = '../DATA/'+projectNameIndus
# # DataBrevet['ficBrevets'] = ficname +'Indus'
# # DataBrevet['brevets'] = Indus
# if projectNameIndus not in os.listdir('../DATA'):
#     os.makedirs(ResultBiblioPath)
    
# ndf = ficname+'Indus'
# Data = dict()
# with open(ResultBiblioPath+'/Description'+ ndf, 'wb') as ficRes:
#     Data['ficBrevets'] = ndf 
#     Data['number'] = len(Indus)
#     Data['requete'] = DataBrevet['requete'] 
#     pickle.dump(Data, ficRes)

# with open(ResultBiblioPath+'/'+ ndf, 'ab') as ndfLstBrev:
#     for pat in Indus:
#         pickle.dump(pat , ndfLstBrev)
  




# creating nets for Gephi inmport

# # node files (authors and applicants)
# cpt = 0
# Ids = dict()
# with open(ResultGephiPath+"/noeudAut.csv", "w", encoding='utf8') as fic:
#     fic .write( "Ids;label;isAuthor+\n")
#     for noeud in NoeudAut:
#         Ids[noeud] = cpt

#         # node ; node lab ; is Author
#         ligne= str(cpt) +";" + noeud  +";" + str(noeud.title()  in AuteursFr) +'\n'
#         fic .write(ligne)
#         cpt+=1

# with open(ResultGephiPath+"/LiensAut.csv", "w", encoding='utf8') as fic:
#     fic .write("Source;Target\n")
#     for orig, dest in EdgesAut:
#         # node ; node lab ; is Author
#         ligne=  str(Ids[orig]) +";" + str(Ids[dest])  +'\n'
#         fic .write(ligne)


# cpt = 0
# Ids = dict()
# NoeudOk = [] # check whether applicant name is not and author or not Public
# with open(ResultGephiPath+"/NoeudApplicant.csv", "w", encoding='utf8') as fic:
#     fic .write( "Id;Label;isPublic;NoeudAut+\n")
#     for noeud in NoeudApplicant:
        
#         #if noeud not in NoeudAut:
#             NoeudOk.append(noeud)
#             Ids[noeud] = cpt
#             # node ; node lab ; is Author
#             ligne= str(cpt) +";" + noeud  +";" + str(noeud in Public) + ";" + str(noeud in NoeudAut) + '\n'
#             fic .write(ligne)
#             cpt+=1
#         # elif noeud in Public:
#         #     Ids[noeud] = cpt
#         #     NoeudOk.append(noeud)
#         #         # node ; node lab ; is Author
#         #     ligne= str(cpt) +";" + noeud  +";" + str(noeud in Public) +'\n'
#         #     fic .write(ligne)
#         #     cpt+=1
#         # else:
#         #     cpt+=1 # should we ?
#         #     pass
                        
# with open(ResultGephiPath+"/LiensApplicant.csv", "w", encoding='utf8') as fic:
#     fic .write("Source;Target\n")
#     for orig, dest in EdgesApplicant:
#         # node ; node lab ; isAuthor
#         #if orig in NoeudOk and dest in NoeudOk:
#         ligne=  str(Ids[orig]) +";" + str(Ids[dest])  +'\n'
#         fic .write(ligne)






# pos = nx.spring_layout(GraphAuteurs)  
# # nodes
# # nx.draw_networkx_nodes(GraphAuteurs, pos,
# #                         nodelist=[0, 1, 2, 3],
# #                         node_color='r',
# #                         node_size=500,
# #                         alpha=0.8)
# # nx.draw_networkx_nodes(GraphAuteurs, pos,
# #                         nodelist=[4, 5, 6, 7],
# #                         node_color='b',
# #                         node_size=500,
# #                         alpha=0.8)

# # edges
# nx.draw_networkx_edges(GraphAuteurs, pos, width=1.0, alpha=0.5)
# # nx.draw_networkx_edges(GraphAuteurs, pos,
# #                         edgelist=[(0, 1), (1, 2), (2, 3), (3, 0)],
# #                         width=8, alpha=0.5, edge_color='r')
# # nx.draw_networkx_edges(GraphAuteurs, pos,
# #                         edgelist=[(4, 5), (5, 6), (6, 7), (7, 4)],
# #                         width=8, alpha=0.5, edge_color='b')

# # nx.draw_networkx_edges(GraphAuteurs, pos,
# #                         edgelist=[(4, 5), (5, 6), (6, 7), (7, 4)],
# #                         width=8, alpha=0.5, edge_color='g')             

# attrs = dict()
# for noeud in GraphAuteurs.nodes():
#     attrs [noeud ] = {'color':{'r' : 0, 'g' : 0, 'b' : 0}}
    
# nx.set_node_attributes(GraphAuteurs, attrs, 'viz')           
# for node in GraphAuteurs.nodes():
    
#     if node in AuteursFr:
#         GraphAuteurs [node]['viz']['color'] = {'r' : 0, 'g' : 0, 'b' : 255}
#     elif node in AuteursNotFr:
#         GraphAuteurs [node] ['viz']['color'] = {'r' : 255, 'g' : 0, 'b' : 0}
#     else:
#         GraphAuteurs [node] ['viz']['color'] = {'r' : 0, 'g' : 255, 'b' : 0}
# attrs = dict()
# for noeud in GraphApplicant.nodes():
#     attrs = {noeud: {'viz': {'color':{'r' : 0, 'g' : 0, 'b' : 0}}}}
    
# nx.set_node_attributes(GraphAGraphApplicantuteurs, attrs)         
# for node in iter(GraphApplicant):
# #    GraphApplicant  ["viz"] =dict()
     

#     if node in Public:

#         GraphApplicant [node] ['viz'] ['color'] = {'r' : 0, 'g' : 0, 'b' : 255}
#     else:
#         GraphApplicant [node] ['viz']['color'] = {'r' : 255, 'g' : 0, 'b' : 0}


# print("radius: %d" % nx.radius(GraphAuteurs))
# print("diameter: %d" % nx.diameter(GraphAuteurs))
# print("eccentricity: %s" % nx.eccentricity(GraphAuteurs))
# print("center: %s" % nx.center(GraphAuteurs))
# print("periphery: %s" % nx.periphery(GraphAuteurs))
# print("density: %s" % nx.density(GraphAuteurs))        


# nx.write_gexf(GraphAuteurs, "GraphAuteurs.gexf")
# nx.write_gexf(GraphApplicant, "GraphAuteurs.gexf")

# def GenereListeFichiers(rep):
#     """ prend un dossier en paramètre (chemin absolu) et génère la liste
#     complète des fichiers TXT et CSV de l'arborescence"""
#     import os
#     listeFicCSV = []
#     listeFicTXT = []

#     for ficOuRep in os.listdir(rep):

#         if "." not in ficOuRep:
#             for fic in os.listdir(rep+'//'+ficOuRep):
#                 #for fic in os.listdir(root+"//"+sousRep):
#                # temporar = GenereListeFichiers(rep+'//'+sousRep)

#                          if fic.endswith('.csv'):
#                              listeFicCSV.append(rep+"//"+ficOuRep+'//'+fic)
#                          elif fic.endswith('.txt'):
#                              listeFicTXT.append(rep+"//"+ficOuRep+'//'+fic)
#                          else:
#                              pass

# #                listeFicCSV.extend(temporar[0])
# #                listeFicTXT.extend(temporar[1])
# #                listeFicUNK.extend(temporar[2])
#         else:
#            pass
# #                if ficOuRep.endswith('.csv'):
# #                    listeFicCSV.append(root+'//'+fichier)
# #                elif ficOuRep.endswith('.txt'):
# #                    listeFicTXT.append(root+'//'+fichier)
# #                else:
# #                    pass
                
#     return (list(set(listeFicCSV)), list(set(listeFicTXT)))


# # Csv, IRams = GenereListeFichiers(Auteur)
# # matches, NotFound, CountBadNomMatches, CountBadNomPubMed = 0, 0,0, 0
# # Scores = []     # la liste des scores de chaque IPCat
# # Matches = dict()
# # PasMatches=dict()
# # cptPubli = 0
# # for ficCsv in Csv:
# #     with open(ficCsv, "r", encoding='utf8') as ficcsv:
# #         Datacsv=ficcsv.readlines()
    
# #     if len(Datacsv) >1:
# #         enTete = [Datacsv[0]]
# #         enTete.extend(list(set(Datacsv[1:])))
# #         Datacsv = enTete
        
# #         with open(ficCsv, "w", encoding='utf8') as ficcsvNet:
# #            ficcsvNet.write("".join(Datacsv))
        
    
# #     temp = ficcsv.name.split('//')[2]
# #     #Nom=temp.split('-')[1]
# #     First = False
# #     VraiNom = ''
# #     Numro = ''
# #     for lettre in temp:
# #         if not lettre.isnumeric():
# #             if lettre.lower() != lettre and not First:
# #                 VraiNom += ' ' + lettre
# #             else:
# #                 VraiNom +=lettre
# #                 if lettre.lower() != lettre:
# #                     First = True
# #         else:
# #             Numro += lettre
# #     #decodage
# #     VraiNom = VraiNom.replace('- ', '-')
# #     if VraiNom[1:].strip() in Auteurs.keys():
# #         if VraiNom[1:].strip() in BadCasInv.keys():
# #             CountBadNomPubMed +=1
# # #            if VraiNom[1:].strip() in BadCasInv.keys():
# # #                BadCasInv [VraiNom[1:].strip()] 
# # #            #☻ on pourrait rassembler ici toutes lesprod d'un même gugusse
# #         else:
# #             GoodException = []
# #             for nom in BadCasInv.keys():
# #                 if fuzz.token_set_ratio(nom, VraiNom[1:].strip()) >85:
# #                     GoodException.append(nom)
# #             if len(GoodException) == 1:
# #                 VraiNom = ' '+GoodException [0] #on l'a retrouvé
# #             elif len(GoodException) == 0:
# #                 pass
# #             else:
                
# #                 VraiNom = ' '+GoodException [0]
# # #        else:
# # #            with open(ficCsv, "w", encoding='utf8') as ficcsvNet:
# # #                ficcsvNet.write("".join(Datacsv))
# #     else:
        
# #         pass
        
# # #        print(VraiNom)        
# #     #denombrement

# #     #sauvegarde de la version nettoyée


# #     if len(Datacsv)>1:
# #         matches+=1 # Mauvais compteurs si le processe de collecte n'a pas été correctement aboutit (en une fois)
        
# #         for lig in Datacsv:
# #             if not lig.startswith('Label Brevet'):
# #                 cptPubli += 1
# #                 dat = lig.split(';')
# #                 if len(dat)>9:
# #                     if dat[9].isnumeric():
# #                         Scores.append(int(dat[9]))
# #                     else: #quelquefois le champs score est décalé... un ";" dans les données ???
# #                         Scores.append(int(dat[10]))
# #         ScoreMoy = sum(Scores)*1.0/len(Scores)
# #         Matches [VraiNom[1:].strip()] = [Numro, str(len(Datacsv)-1), str(ScoreMoy)]
# #         if VraiNom[1:].strip() in BadCasInv:
# #             CountBadNomMatches +=1
# #     else:
# #         PasMatches [VraiNom[1:].strip()] = Numro
# #         NotFound+=1 # Mauvais compteurs si le processe de collecte n'a pas été correctement aboutit

# # print("Nombre d'auteurs identifiés (le même auteur dans plusieurs brevets) ", matches)
# # print("Nombre d'auteurs identifiés sans publi", NotFound)
# # print("Nombre d'auteurs (uniques) identifiés avec publi  pubmed matchées IPCCat", len(Matches.keys()) )
# # print("Nombre d'auteurs (uniques) identifiés sans publi matchées IPCCat", len(PasMatches.keys()) )

# # print("Nombre d'auteurs identifiés (mal orthogr) sans publi matchées IPCCat", CountBadNomPubMed)
# # print("Nombre d'auteurs identifiés (mal orthogr) avec publi matchées IPCCat", CountBadNomMatches )
# # print ("nombre de publications traitées ", cptPubli )
# # # Normalisation sur Mauvaise orthogrphes
# # pasGrave = 0 #les cas où c'est pas si grave (pas un vrai auteur puisque mal ortho et pas de publi)
# # MatchMalOrtho = dict()
# # for aut in Matches.keys():
# #     if aut in BadCasInv.keys():
# #         if BadCasInv [aut] in Matches.keys():
# #             MatchMalOrtho [aut] = [Matches [aut]]
            
# #             if Matches[BadCasInv [aut]] == Matches [aut]:
# #                 print ("remove key ?")
# #             else:
# #                 MatchMalOrtho [aut].append( Matches [BadCasInv [aut]])
                
# #         elif BadCasInv [aut] in PasMatches.keys():
# #             #La cas où un inventeur est un auteur mais sa version mal orthographiée non
# #             pass # faudrait virer de ce côté la ligne
# #         else:
            
# #             pasGrave += 1 # 
# #             #print ('wtf')
# #     else:
# #         pass

# # # with open(RepDir + "//AuteursMatches.tsv", "w", encoding = 'utf8') as ficMatch:
    
# # #     ficMatch.write('Auteur \t Numéro \t  Nombre Articles \t Score \t\n')
# # #     for aut in Matches.keys():
# # #         ficMatch.write(aut + '\t' +  Matches[aut][0]+ '\t' +  str(Matches[aut][1]) +'\t' +  str(Matches[aut][2]) +'\t\n')
        

# # # with open(RepDir + "//AuteursPAsMatches.tsv", "w", encoding = 'utf8') as ficMatch:
# # #     ficMatch.write('Auteur \t Numéro \t\n')
# # #     for aut in PasMatches.keys():
# # #         ficMatch.write(aut + '\t' +  PasMatches[aut]+ '\t\n')

# # # with open(RepDir + "//MalNommes.tsv", "w", encoding = 'utf8') as ficMatch:
# # #     ficMatch.write('Auteur \t Déclinaisons \t\n')
# # #     for aut in Inventeur_Norm.keys():
# # #         Ligne = aut + '\t' 
# # #         for Badaut in Inventeur_Norm [aut]:
# # #             Ligne+= Badaut +'\t'
            
            
# # #         ficMatch.write(Ligne + '\n')
        
# # #echantillonga

# # import random
# # from pathlib import Path, PureWindowsPath
# # LstAuteurs= list(Matches.keys())
# #Liste = random.sample(range(0, 10, 1),5) #round(len(LstAuteurs)/9))) #len(LstAuteurs)-1)
# # Liste = random.sample(range(0,len(LstAuteurs)-1), round(len(LstAuteurs)/9))
# # loupes=0
# # DossierDestination = "EchantillonMatches"
# # os.mkdir(configFile.ResultPath +'//AcadCorpora//' + DossierDestination)
# # with open (configFile.ResultPath +'//AcadCorpora//'+DossierDestination+'//QualificationMatch.csv', "w", encoding = 'utf8') as ficRes:
# #     ficRes.write('Auteur;OK;Commentaires;URL;Résume brevet;Résumé Article;CIB Match;score Max IPCCat;Affiliation\n')
# #     for num in Liste:
# #         if LstAuteurs[num] not in BadCasInv.keys():
# #             rep =[truc for truc in lstfic if truc.count(LstAuteurs[num].replace(' ', ''))>0]
# #             if len(rep) >0:
# #                 filename = PureWindowsPath(Path(configFile.ResultPath.replace('/', '\\') +'\\AcadCorpora\\'+rep[0]))
# #                 dest = PureWindowsPath(Path(configFile.ResultPath.replace('/', '\\') +'\\AcadCorpora\\'+DossierDestination+'\\Echantillon\\'))
# #                 Auteur =  LstAuteurs[num]
# #                 ficCsvAut = Auteur.title().replace(' ', '').replace('"', '') + 'Match.csv'
# #                 ficCsvAut2 ='-'.join(rep[0].split('-')[1:])+ 'Match.csv'
# #                 filename2 = PureWindowsPath(Path(configFile.ResultPath.replace('/', '\\') +'\\AcadCorpora\\'+rep[0]+'\\'+ficCsvAut))
# #                 filename3 = PureWindowsPath(Path(configFile.ResultPath.replace('/', '\\') +'\\AcadCorpora\\'+rep[0]+'\\'+ficCsvAut2))
# #                 os.system('xcopy /I %s %s' % (filename, dest))
# #                 try:
# #                     with open(filename2, 'r', encoding = 'utf8') as ficSrc:
# #                         lignes = ficSrc.readlines()
# #                 except: #les noms composés
# #                     with open(filename3, 'r', encoding = 'utf8') as ficSrc:
# #                         lignes = ficSrc.readlines()

# #                 Entete= enTete[0]
                
# #                 for lig in lignes[1:]:
# #                     col = lig.split(';')
# #                     # label URL\#Résumé# Résumé article# CIB Match# Score Max # Affiliation
# #                     contenu = ';;;https://worldwide.espacenet.com/patent/search?q=pn %3D '+ col [0] +\
# #                                  ';' + col [1] + ';' + col [6] + ';'+ col [8] + ';' + col [9] + ';' + col [11] +"\n"   
# #                     ficRes.write(Auteur+ contenu)                      
# #             else:
# #                 loupes+=1
# #                 print(LstAuteurs[num])
# #         else:
# #             loupes+=1
# #             print(LstAuteurs[num])
# # print("Loupés des matchés", loupes)    

# # loupes=0
# # LstAuteurs= list(PasMatches.keys())
# # Liste = random.sample(range(0,len(LstAuteurs)-1), round(len(LstAuteurs)/9))
# # with open (configFile.ResultPath +'//AcadCorpora//'+DossierDestination+'//QualificationMatch2.csv', "w", encoding = 'utf8') as ficRes:
# #     with open (configFile.ResultPath +'//AcadCorpora//'+DossierDestination+'//QualificationMatch.csv', "r", encoding = 'utf8') as ficSrc:
# #         for lig in ficSrc.readlines():
# #             if len(lig.strip().replace(' ','')) >0:
# #                 ficRes.write(lig)
# #             else:
# #                 pass
    

# # DossierDestination = "EchantillonNONMatches"
# # os.mkdir(configFile.ResultPath +'//AcadCorpora//' + DossierDestination)
# # with open (configFile.ResultPath +'//AcadCorpora//'+DossierDestination+'//QualificationPasMatch.csv', "w", encoding = 'utf8') as ficRes:
# #     ficRes.write('Auteur;OK;Commentaires;URL;Résume brevet;Résumé Article;CIB Match;score Max IPCCat;Affiliation\n')
# #     for num in Liste:
# #         if LstAuteurs[num] not in BadCasInv.keys():
# #             rep =[truc for truc in lstfic if truc.count(LstAuteurs[num].replace(' ', ''))>0]
# #             if len(rep) >0:
# #                 filename = PureWindowsPath(Path(configFile.ResultPath.replace('/', '\\') +'\\AcadCorpora\\'+rep[0]))
# #                 dest = PureWindowsPath(Path(configFile.ResultPath.replace('/', '\\') +'\\AcadCorpora\\'+DossierDestination+'\\Echantillon\\'))
# #                 Auteur =  LstAuteurs[num]
# #                 ficCsvAut = Auteur.title().replace(' ', '').replace('"', '') + 'Match.csv'
# #                 filename2 = PureWindowsPath(Path(configFile.ResultPath.replace('/', '\\') +'\\AcadCorpora\\'+rep[0]+'\\'+ficCsvAut))
# #                 os.system('xcopy /I %s %s' % (filename, dest))
# #                 ficCsvAut2 ='-'.join(rep[0].split('-')[1:])+ 'Match.csv'
# #                 filename3 = PureWindowsPath(Path(configFile.ResultPath.replace('/', '\\') +'\\AcadCorpora\\'+rep[0]+'\\'+ficCsvAut2))
# #                 try:
# #                     with open(filename2, 'r', encoding = 'utf8') as ficSrc:
# #                         lignes = ficSrc.readlines()
# #                 except: #les noms composés
# #                     with open(filename3, 'r', encoding = 'utf8') as ficSrc:
# #                         lignes = ficSrc.readlines()

# #                 Entete= enTete[0]
# #                 if len(lignes)==1:
# #                     ficRes.write(Auteur +';;;\n') 
                    
# #                 for lig in lignes[1:]:
# #                     col = lig.split(';')
                    
# #                     # label URL\#Résumé# Résumé article# CIB Match# Score Max # Affiliation
# #                     contenu = ';;;https://worldwide.espacenet.com/patent/search?q=pn %3D '+ col [0] +\
# #                                  ';' + col [1] + ';' + col [6] + ';' + col [8] + ';'+ col [9] + ';' + col [11] +"\n"   
# #                     ficRes.write(Auteur+ contenu)                      
# #             else:
# #                 loupes+=1
# #                 print(LstAuteurs[num])
# #         else:
# #             loupes+=1
# #             print(LstAuteurs[num])
# # print("Loupés des NON matchés", loupes)      

# # with open (configFile.ResultPath +'//AcadCorpora//'+DossierDestination+'//QualificationPasMatch2.csv', "w", encoding = 'utf8') as ficRes:
# #     with open (configFile.ResultPath +'//AcadCorpora//'+DossierDestination+'//QualificationPasMatch.csv', "r", encoding = 'utf8') as ficSrc:
# #         for lig in ficSrc.readlines():
# #             if len(lig.strip().replace(' ','')) >0:
# #                 ficRes.write(lig)
# #             else:
# #                 pass

