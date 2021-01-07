# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 07:41:54 2019

@author: dreymond
"""


import codecs
import os, sys
import pickle
import copy
from pymed import PubMed
import shutil
from Patent2Net.P2N_Lib import LoadBiblioFile
from Patent2Net.P2N_Config import LoadConfig
from Patent2Net.P2N_Lib_Acad import  Nettoie, NoPunct, CheckListInclu, CheckListMix, CheckListExclu, UnCheck, Check
from Patent2Net.P2N_Lib_Acad import IPCCategorizer, IPCExtractPredictionBrevet,PubMedCheckNameAndGetAffiliation, OPSChercheAbstractBrevet
from fuzzywuzzy import fuzz


import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
import pandas as pd


#table = string.maketrans("","")

pd.options.display.max_colwidth = 150


    
# Loading the disctionnary for splitting the corpus
# if all aplicant are in : Public corpus
# all out : Indus corpus
# Mix corpora are created

xlsx = pd.ExcelFile('./Resources/EntitésPubliquesNORM4.xlsx')
Public = []
TypeAppl = dict()
ApplType = dict() # reverse table


for sheet in xlsx.sheet_names:
   dicotemp = xlsx.parse(sheet).to_dict(orient='list')
   
   for cle, val in dicotemp.items():
        tempoRes = []
        for appli in val:
            sav = appli
            tempoRes.append(appli)
            if appli not in ApplType.keys():
                ApplType [appli] = cle
            else:
                if cle != ApplType [appli]:
                    print ("ARG:", cle, appli)
                else:
                    pass
        TypeAppl [cle] = tempoRes
        
        Public.extend(tempoRes)
       
configFile = LoadConfig()
# Les champs nécessaires par brevet.
 
# Loading Patents from P2N format

requete = configFile.requete
projectName = configFile.ndf
ndf = projectName
BiblioPath = configFile.ResultBiblioPath
ResultBiblioPath = configFile.ResultBiblioPath
temporPath = configFile.temporPath
ResultPathContent= configFile.ResultContentsPath
ResultAbstractPath = configFile.ResultAbstractPath
ListBiblioPath = configFile.ResultBiblioPath
# special path used with AcadPubMed.py
Auteur = configFile.ResultPath + '/AcadCorpora'
RepDir = configFile.ResultPath + '/AcadCorpora'
project = RepDir
if 'AcadCorpora' not in os.listdir(configFile.ResultPath):
    print ("relancez le script de collecte (AcadPubMed.py 29/06/2019)")
    sys.exit()
# if 'Description'+ndf in os.listdir(BiblioPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
#     print( "loading patent biblio data with all fields.")
#     DataBrevet = LoadBiblioFile(BiblioPath, ndf)
#     print("Hi this is AcadStatsAcad Corpora splitter processor. Bibliographic data of ", ndf, " patent universe found.")
# else:
#     print ("relancez P2n pour collecter les données brevet")
#     sys.exit()

# test de consistance
# with open(Auteur+'//DejaTraites.csv', 'r',) as fic:
#     DejaVus = fic.readlines()

# if len (set(DejaVus)) == len(DataBrevet['brevets']):
#     print ('Youhou, tous les brevets ' + ndf + ' ont été traités.')
#     print ('Nb de brevets : ', len(DataBrevet['brevets']))
    
# else:
#     reste = [bre['label'] for bre in DataBrevet['brevets'] if bre['label'] not in DejaVus ]
#     print ('il reste ', len(reste), ' brevets à traiter')
 
# # Analyse stat des résultats
# print ("""Ceux qui ont changé d'affiliation la première trouvée puis la seconde... 
#        S'il en est plus de deux, ce sera la première puis la 3e....""")
# lstfic = os.listdir(configFile.ResultPath +'//AcadCorpora')
# with codecs.open(configFile.ResultPath +'//AcadCorpora//AuteursAffil.csv', 'r', 'utf8') as fic:
#     data = fic.readlines()
# multiAut = 0  # inventeurs prolixes
# AffilDiff = 0   # les affiliations différentes
# Auteurs = dict()
# for lig in data:
#     col = lig   .strip()
#     col = col.split(';')
#     if col[0] not in Auteurs.keys():
#         Auteurs [col[0]] = col[1]
#     else:
#         if col[1] != Auteurs [col[0]]:
#             print (col[0], " --> ", Auteurs [col[0]])
#             print (col[0], " --> ", col[1])
            
#             AffilDiff +=1
#             multiAut+=1  # non sens, le script peut recollecter plusieurs fois le même
#         else:
#             multiAut+=1
#             pass



# test of subfunctions
# test1 = ['CNRS', 'INSERM', 'CHU Paris'] # tout dans CritFr
# test2 = ['CNRS', 'INSERM', 'Meyrieux'] # Mix
# test3 = ['Truc', 'machin', 'chose'] # rien dans CritFr

# CheckListExclu(test1, CritFr)
# CheckListInclu(test1, CritFr) # --> True
# CheckListMix(test1, CritFr)


# CheckListExclu(test2, CritFr)
# CheckListInclu(test2, CritFr)
# CheckListMix(test2, CritFr) # --> True

# CheckListExclu(test3, CritFr) # --> True
# CheckListInclu(test3, CritFr)
# CheckListMix(test3, CritFr)


import copy

# no good: la sélection des brevets à partir des représentants qui certaines fois ne sont que dans les familles, doit se faire sur la liste 
# des équivalents du corpus initial. Là ce 'nest pas le cas et on a un joyeux mix
for fic in [ndf, 'Families'+ndf]:
    print("\n> Hi! This is corpora splitter used on:", fic)
    if 'Description' + fic in os.listdir(ListBiblioPath):
        with open(ListBiblioPath + '//' + fic, 'r') as data:
            DataBrevet = LoadBiblioFile(ListBiblioPath, fic)
    else:  # Retrocompatibility
        print("please use Comptatibilizer")
        sys.exit()
    LstBrevet = DataBrevet['brevets']

    print("Nice, ", len(DataBrevet["brevets"]), " patents found. Découpage selon le données du tablea EntitésPubliquesNorm.xlsx")


    Inventeurs = []
    Applicants = []
    for bre in DataBrevet['brevets']:
#     temp =Nettoie(bre['inventor'])
         Inventeurs.extend([inv for inv in bre['inventor'] if len(inv.split((' ')))>1])
#     bre['inventor'] = temp
#     temp = Nettoie(bre['applicant'])
         Applicants.extend(bre['applicant'])
#     bre['applicant'] = temp
        
    Inventeurs = set(Inventeurs)
    Applicants = set(Applicants)

    Inventeurs1 = [inv for inv in Inventeurs if len(inv.split(' '))<2]
    Inventeurs2 = [inv for inv in Inventeurs if inv not in Inventeurs1]
    Inventeur_Norm = dict()
    Applicant_Norm = dict()
    BadCasApp = dict()
    InvDejaVus = []
    AppDejaVus = []

    #Applicants = set([app.lower().title() for app in Applicants])
    InventeurSafe = copy.copy(Inventeurs)
    print ("Nombre d'inventeurs :", len(set(Inventeurs)))
                 
    print ("Nombre d'applicants :", len(set(Applicants)))
    TypeBre = dict()
    for bre in LstBrevet:
        # if bre['label'] == 'FR3034554':
        #     print (bre)
        bre['applicant'] = [appli for appli in bre['applicant'] if isinstance(appli, str) and len(appli.strip())>0 and appli.replace(' ', '') != 'empty']
        bre['applicant'] = [appli for appli in bre['applicant'] if appli.title() not in Inventeurs2 and NoPunct(appli.title()) not in Inventeurs2]
        if isinstance(bre['applicant'], list) and len(bre['applicant'])==1:
            if bre['applicant'][0].upper() in Public:
                bre ['type'] = "public"
                bre['typeCollab'] ="NON" # one applicant, no collaboration
            else:
                bre ['type'] = "indus"
                bre['typeCollab'] = "NON" # one applicant, no collaboration
        elif isinstance(bre['applicant'], str):
            if bre['applicant'].upper() in Public:
                bre ['type'] = "public"
                bre['typeCollab'] ="NON" # one applicant public, no collaboration
            else:
                bre ['type'] = "indus"
                bre['typeCollab'] = "NON" # one applicant, no collaboration
        elif isinstance(bre['applicant'], list) and len(bre['applicant'])>1 and CheckListExclu(bre['applicant'], Inventeurs):
            if CheckListInclu(bre['applicant'], Public):  # one public entity
                bre ['type'] = "public"
                bre['c'] = [ApplType[truc] for truc in bre['applicant']]
            elif CheckListExclu(bre['applicant'], Public):  # no public entity
                bre ['type'] = "indus"
                bre['typeCollab'] = "indus"

            else:
                bre ['type'] = "collab"
                bre['typeCollab'] = [ApplType[truc] if truc in ApplType.keys() else 'Indus' for truc in bre['applicant'] ]
                
        elif isinstance(bre['applicant'], list) and len(bre['applicant'])>1 and CheckListExclu(bre['applicant'], Inventeurs):
                bre ['type'] = "Inconnu"
                bre['typeCollab'] = "NON"
        elif isinstance(bre['applicant'], list) and len([app for app in bre['applicant'] if app not in Inventeurs2]) != len (bre['applicant']):
            if len([app for app in bre['applicant'] if app not in Inventeurs2]) >= 1:
                if CheckListInclu([app for app in bre['applicant'] if app not in Inventeurs2], Public):
                    bre ['type'] = "public"
                    bre['typeCollab'] = "public-individu"
                else:
                    bre ['type'] = "indus"
                    bre['typeCollab'] = "indus-individu"
            else: # all applicants are inventors !!
                    bre ['type'] = "individuels"
                    bre['typeCollab'] = "Inconnu"
                    
                    
         # elif len(bre['applicant'])>0: 
        #     bre ['type'] = "collab"
        #     bre['typeCollab'] = [ApplType[truc] if truc in ApplType.keys() else 'Indus' for truc in bre['applicant'] ]
        #     if len(bre['applicant']) ==0 or sum([len(truc)==0 for truc in bre['applicant']]) >0:
        #         print("aille")
        else: #len(bre['applicant']) == 0
            if len(bre['applicant']) != 0:
                print ('wtf ?')
            bre ['type'] = "Inconnu"
            bre['typeCollab'] = "NON"
        if isinstance(bre['applicant'], list) and len(bre['applicant'])>0:
            for aut in bre['applicant']:
                # if 'vetagrosup' in au.lower():t
                #     print("ARGS")
                for coAut in bre['applicant']:
                    if coAut!= aut:
                        # GraphApplicant.add_edge(aut, coAut)
                        if bre ['type'] in TypeBre.keys():
                            TypeBre [bre ['type']]. append((aut, coAut))
                        else:
                            TypeBre [bre ['type']]= [(aut, coAut)]
    
    print ("saving files")
    with open(ListBiblioPath + '//tempo' + fic, 'ab') as ndfLstBrev:
        for pat in LstBrevet:
            pickle.dump(pat , ndfLstBrev)
    os.remove(ListBiblioPath+'//'+ fic)
    os.rename(ListBiblioPath + '//tempo' + fic, ListBiblioPath+'//'+ fic)
    
    
    Mix = [bre for bre in LstBrevet if bre['type'] == 'collab' and bre['typeCollab'] !="NON"]
    Univ = [bre for bre in LstBrevet if bre['type'] == 'public']
    Indus = [bre for bre in LstBrevet if bre['type'] == 'indus']
    AutInvDeposant = [bre for bre in LstBrevet if bre['type'] == 'Inconnu']
    #check consistance
    total = len(Mix) + len(Univ) + len(Indus) + len(AutInvDeposant)
    if total-len(LstBrevet) == 0:
        print (total -len(LstBrevet), " patents left... GOOD")

    projectNameMix=projectName+'Mix'
    projectNameUniv=projectName+'Public'
    projectNameIndus=projectName+'Indus'
    projectNameAutres = projectName + "Autres"
    ficname =fic
    
    ResultBiblioPath = '../DATA/'+projectNameMix+'/'+'PatentBiblios'
    ResultPath = '../DATA/'+projectNameMix
    if projectNameMix not in os.listdir('../DATA'):
        os.makedirs(ResultBiblioPath)
    
    # DataBrevet['ficBrevets'] = ficname +'Mix'
    # DataBrevet['brevets'] = Mix
    ndf = ficname+'Mix'
    Data = dict()
    with open(ResultBiblioPath+'//Description'+ ndf, 'wb') as ficRes:
        Data['ficBrevets'] = ndf 
        Data['number'] = len(Mix)
        Data['requete'] = DataBrevet['requete'] + " " + " brevets ayant plus de deux déposants, l'un public l'autre non"
        pickle.dump(Data, ficRes)
    
    with open(ResultBiblioPath+'/'+ ndf, 'ab') as ndfLstBrev:
        for pat in Mix:
            pickle.dump(pat , ndfLstBrev)
    
    if "AcadCorpora" not in os.listdir(ResultBiblioPath.replace('/PatentBiblios', '')):
        os.makedirs(ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora')  
    shutil.copy(RepDir + '/'+"AuteursAffil.csv", ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora/')
    shutil.copy(RepDir + '/'+"traceAuct.csv", ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora/')
    shutil.copy(RepDir + '/'+"AuteursPAsMatches.tsv", ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora/')
    shutil.copy(RepDir + '/'+"AuteursMatches.tsv", ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora/')

    if "InventeurNormes.pkl" in os.listdir(BiblioPath):
        shutil.copy(BiblioPath+'/InventeurNormes.pkl', ResultBiblioPath)
        shutil.copy(BiblioPath+'/NormInventeurs.pkl', ResultBiblioPath)                                    
    ResultBiblioPath = '../DATA/'+projectNameUniv+'/'+'PatentBiblios'
    ResultPath = '../DATA/'+projectNameUniv
    

    if projectNameUniv not in os.listdir('../DATA'):
        os.makedirs(ResultBiblioPath)
     
    # DataBrevet['ficBrevets'] = ficname +'Univ'
    # DataBrevet['brevets'] = Univ
    ndf = ficname+'Public'
    Data = dict()
    with open(ResultBiblioPath+'/Description'+ ndf, 'wb') as ficRes:
        Data['ficBrevets'] = ndf
        Data['number'] = len(Univ)
        Data['requete'] = DataBrevet['requete']  + " demandes émanant d'entités publiques"
        pickle.dump(Data, ficRes)
    
    with open(ResultBiblioPath+'/'+ ndf, 'ab') as ndfLstBrev:
        for pat in Univ:
            pickle.dump(pat , ndfLstBrev)
            
    if "AcadCorpora" not in os.listdir(ResultBiblioPath.replace('/PatentBiblios', '')):
        os.makedirs(ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora')  
    shutil.copy(RepDir + '/'+"AuteursAffil.csv", ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora/')
    shutil.copy(RepDir + '/'+"traceAuct.csv", ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora/')
    shutil.copy(RepDir + '/'+"AuteursPAsMatches.tsv", ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora/')
    shutil.copy(RepDir + '/'+"AuteursMatches.tsv", ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora/')
    
    if "InventeurNormes.pkl" in os.listdir(BiblioPath):
        shutil.copy(BiblioPath+'/InventeurNormes.pkl', ResultBiblioPath)  
        shutil.copy(BiblioPath+'/NormInventeurs.pkl', ResultBiblioPath)  
    
    
    
    ResultBiblioPath = '../DATA/'+projectNameIndus+'/'+'PatentBiblios'
    ResultPath = '../DATA/'+projectNameIndus
    # DataBrevet['brevets'] = Indus
    if projectNameIndus not in os.listdir('../DATA'):
        os.makedirs(ResultBiblioPath)
    ndf = ficname+'Indus'
    Data = dict()
    with open(ResultBiblioPath+'/Description'+ ndf, 'wb') as ficRes:
        Data['ficBrevets'] = ndf 
        Data['number'] = len(Indus)
        Data['requete'] = DataBrevet['requete'] + " déposants hors dictionnaire d'entités publiques"
        pickle.dump(Data, ficRes)
    
    with open(ResultBiblioPath+'/'+ ndf, 'ab') as ndfLstBrev:
        for pat in Indus:
            pickle.dump(pat , ndfLstBrev)
    if "AcadCorpora" not in os.listdir(ResultBiblioPath.replace('/PatentBiblios', '')):
        os.makedirs(ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora')  
    #copy of author affiliation in each directory of splitted corpora
    shutil.copy(RepDir + '/'+"AuteursAffil.csv", ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora/')
    shutil.copy(RepDir + '/'+"traceAuct.csv", ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora/')
    shutil.copy(RepDir + '/'+"AuteursPAsMatches.tsv", ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora/')
    shutil.copy(RepDir + '/'+"AuteursMatches.tsv", ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora/')

    if "InventeurNormes.pkl" in os.listdir(BiblioPath):
        shutil.copy(BiblioPath+'/InventeurNormes.pkl', ResultBiblioPath)   
        shutil.copy(BiblioPath+'/NormInventeurs.pkl', ResultBiblioPath) 


    ResultBiblioPath = '../DATA/'+projectNameAutres+'/'+'PatentBiblios'
    ResultPath = '../DATA/'+projectNameAutres
    # DataBrevet['brevets'] = Indus
    if projectNameAutres not in os.listdir('../DATA'):
        os.makedirs(ResultBiblioPath)
    ndf = ficname+'Autres'
    Data = dict()
    with open(ResultBiblioPath+'/Description'+ ndf, 'wb') as ficRes:
        Data['ficBrevets'] = ndf 
        Data['number'] = len(AutInvDeposant)
        Data['requete'] = DataBrevet['requete'] + " sans déposants (brevets d'inventeurs ) "
        pickle.dump(Data, ficRes)
    
    with open(ResultBiblioPath+'/'+ ndf, 'ab') as ndfLstBrev:
        for pat in AutInvDeposant:
            pickle.dump(pat , ndfLstBrev)
    if "AcadCorpora" not in os.listdir(ResultBiblioPath.replace('/PatentBiblios', '')):
        os.makedirs(ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora')  
    #copy of author affiliation in each directory of splitted corpora
    shutil.copy(RepDir + '/'+"AuteursAffil.csv", ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora/')
    shutil.copy(RepDir + '/'+"traceAuct.csv", ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora/')
    shutil.copy(RepDir + '/'+"AuteursPAsMatches.tsv", ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora/')
    shutil.copy(RepDir + '/'+"AuteursMatches.tsv", ResultBiblioPath.replace('/PatentBiblios', '') + '/AcadCorpora/')

    if "InventeurNormes.pkl" in os.listdir(BiblioPath):
        shutil.copy(BiblioPath+'/InventeurNormes.pkl', ResultBiblioPath)   
        shutil.copy(BiblioPath+'/NormInventeurs.pkl', ResultBiblioPath) 
# NoeudAut = list(iter(GraphAuteurs))
# NoeudApplicant = list(iter(GraphApplicant))
# EdgesAut = list(iter(GraphAuteurs.edges()))
# EdgesAut2 = [orig + ' ' + dest for orig, dest in EdgesAut]
# EdgesApplicant = list(iter(GraphApplicant.edges()))
# EdgesApplicant2 = [orig + ' ' + dest for orig, dest in EdgesApplicant]


# Autnode_sizes = [sum([truc.count(aut) for truc in EdgesAut2]) for aut in NoeudAut]
# Applicantnode_sizes = [sum([truc.count(aut) for truc in EdgesApplicant2]) for aut in NoeudApplicant]
  
# # nodes
# nx.draw_networkx_nodes(GraphAuteurs, pos,
#                        nodelist=[0, 1, 2, 3],
#                        node_color='r',
#                        node_size=500,
#                        alpha=0.8)
# nx.draw_networkx_nodes(GraphAuteurs, pos,
#                        nodelist=[4, 5, 6, 7],
#                        node_color='b',
#                        node_size=500,
#                        alpha=0.8)

# # edges
# nx.draw_networkx_edges(GraphAuteurs, pos, width=1.0, alpha=0.5)
# nx.draw_networkx_edges(GraphAuteurs, pos,
#                        edgelist=[(0, 1), (1, 2), (2, 3), (3, 0)],
#                        width=8, alpha=0.5, edge_color='r')
# nx.draw_networkx_edges(GraphAuteurs, pos,
#                        edgelist=[(4, 5), (5, 6), (6, 7), (7, 4)],
#                        width=8, alpha=0.5, edge_color='b')

# nx.draw_networkx_edges(GraphAuteurs, pos,
#                        edgelist=[(4, 5), (5, 6), (6, 7), (7, 4)],
#                        width=8, alpha=0.5, edge_color='g')             
             
# for node in iter(GraphAuteurs):
#     if node in AuteursFr:
#         node ['color'] = 'blue'
#     elif node in AuteursNotFr:
#         node ['color'] = 'red'
#     else:
#         print (node)
# print("radius: %d" % nx.radius(GraphAuteurs))
# print("diameter: %d" % nx.diameter(GraphAuteurs))
# print("eccentricity: %s" % nx.eccentricity(GraphAuteurs))
# print("center: %s" % nx.center(GraphAuteurs))
# print("periphery: %s" % nx.periphery(GraphAuteurs))
# print("density: %s" % nx.density(GraphAuteurs))        

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

