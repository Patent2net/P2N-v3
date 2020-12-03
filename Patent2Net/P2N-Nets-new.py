# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 07:41:54 2019

@author: (c) 2020 The Patent2Net Developers
"""


#import codecs
import os
import sys
#import shutil
#import pickle

import matplotlib.cm
from Patent2Net.P2N_Lib import LoadBiblioFile, AnnonceProgres, AnnonceLog
from Patent2Net.P2N_Config import LoadConfig
#from Patent2Net.P2N_Lib_Acad import IPCCategorizer, IPCExtractPredictionBrevet,PubMedCheckNameAndGetAffiliation, OPSChercheAbstractBrevet
from Patent2Net.P2N_Lib_Acad import  NoPunct #, CheckListInclu, CheckListMix, CheckListExclu, UnCheck, Check
#from fuzzywuzzy import fuzz
from P2N_Lib import UrlPatent,UrlApplicantBuild,UrlInventorBuild,UrlIPCRBuild, cmap_discretize, RenderTemplate
#from dateutil.relativedelta import relativedelta
import networkx as nx
#import matplotlib.pyplot as plt
#from networkx.readwrite import json_graph
import pandas as pd
#import string
#import re
#import unidecode
from networkx_functs import calculate_degree, calculate_betweenness, calculate_degree_centrality
from networkx.drawing.nx_agraph import graphviz_layout                           


screenX = 800
screenY = 600

AnnonceProgres (Appli = 'p2n_network', valMax = 100, valActu = 0)       
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
                                                
import time 

start_time = time.time()
                
def cycle (liste):
    tempo = []
    if len(liste) < 1:
        return None
    else:
        taille = len(liste)-1
        for indice in range(taille):
            tempo.append((liste [indice], liste[indice+1]))
        return tempo
                                                                                                                                      
                                                                                    
                                                
                                                                                                   
     
Inventeurs= set()
Applicants = set()                                                       
              
AnnonceLog (Appli = 'p2n_network', texte='Net processing is starting ')
if configFile.GatherFamilly:
    PU = [ndf, 'Families'+ndf]
else:
    PU = [ndf]
for fic in PU:
                               
    print("\n> Hi! This is Net processor used on:", fic)
    if 'Description' + fic in os.listdir(ResultBiblioPath):
        with open(ResultBiblioPath + '//' + fic, 'r') as data:
            dico = LoadBiblioFile(ResultBiblioPath, fic)
    else:  # Retrocompatibility
        print("please use Comptatibilizer")
        sys.exit()
    LstBrevet = dico['brevets']

    for bre in LstBrevet:
        if isinstance(bre['label'], list):
            # if len(bre['label']) >1:
                if len(bre['label']) != len( set(bre['label'])):
                    print ("two labels for same patent fixing to first one" , bre ["label"] )
                    bre ["label"] = bre ["label"] [0]
                else:
                    bre ["label"] = bre ["label"] [0]
            
        if isinstance(bre['inventor'], list):
            if ''.join(bre['inventor']).strip().lower() == 'empty':
                    bre['inventor'] = []
                    bre['inventor-nice'] = []
            else:
            
                tempoinv = []
                for inv in bre['inventor']:
                    if inv.lower() != 'empty':
                        tempoinv.append(inv.title())
                        Inventeurs.add(inv.title())
                bre['inventor'] = tempoinv

            
        elif bre['inventor'].strip().lower() == 'empty' or len(bre['inventor'].strip().lower()) ==0:
            bre['inventor'] = []
            bre['inventor-nice'] = []
        else:
            bre['inventor'] = bre['inventor'].title()
            Inventeurs.add(bre['inventor'])
        

        if isinstance(bre['applicant'], list):
            
            
            if ''.join(bre['applicant']).strip().lower() == 'empty':
                bre['applicant'] = []
                bre['applicant-nice'] = []
            else:
                tempoappl = []
                for inv in bre['applicant']:
                    if inv.lower() != 'empty' and len(inv) >0:
                        tempoappl.append(inv.upper())
                        Applicants.add(inv.upper())
                bre['applicant'] = tempoappl
        else:
            bre['applicant'] =  bre['applicant'] .upper ()
            Applicants.add(bre['applicant'])

    if 'Families' in fic:
        df_Fam = pd.DataFrame(LstBrevet)
    else:
        df = pd.DataFrame(LstBrevet)

total = len(df) + len(df_Fam)                
AnnonceLog (Appli = 'p2n_network', texte='Good, processing '+ str(total) +' patents ')

AnnonceProgres (Appli = 'p2n_network', valMax = 100, valActu = 20)  

for ndf in PU:
    
    if 'Families' not in ndf:
        dataf = df
        dataf ['family lenght'] = [1] * len(dataf.index)
    else:
        dataf = df_Fam
        
    for bre in dataf.itertuples():
        # cleaning
        if not isinstance(bre.label, str):
           dataf.at [bre.Index, 'label' ] = bre.label [0]

        else:
           pass
        if not isinstance(bre.Citations, str) and not isinstance(bre.Citations, int):
           dataf.at [bre.Index, 'Citations' ] = bre.Citations [0]

        else:
           pass   
        if not isinstance(bre.applicant, list):
           dataf.at [bre.Index, 'applicant' ] = list(set([inf for inf in bre.applicant if inf.lower() not in ['empty', '', 'none']]))
        else:
           dataf.at [bre.Index, 'applicant' ] = list(set(bre.applicant))
        if not isinstance(bre.inventor, list):
           dataf.at [bre.Index, 'inventor' ] = [bre.inventor]
        else:
           dataf.at [bre.Index, 'inventor' ] = list(set([inf for inf in bre.inventor if inf.lower() not in ['empty', '', 'none']]))
        if not isinstance(bre.IPCR1, list):
            dataf.at [bre.Index, 'IPCR1' ] = [bre.IPCR1]
        else:
            dataf.at [bre.Index, 'IPCR1' ] = list(set([ipc for ipc in bre.IPCR1 if ipc.lower() not in ['empty', '', 'none']]))
        if not isinstance(bre.IPCR3, list):
            dataf.at [bre.Index, 'IPCR3' ] = [bre.IPCR3]
        else:
            dataf.at [bre.Index, 'IPCR3' ] = list (set([ipc for ipc in bre.IPCR3 if ipc.lower() not in ['empty', '', 'none']]))
        if not isinstance(bre.IPCR4, list):
            dataf.at [bre.Index, 'IPCR4' ] = [bre.IPCR4]
        else:
            dataf.at [bre.Index, 'IPCR4' ] = list (set([ipc for ipc in bre.IPCR4 if ipc.lower() not in ['empty', '', 'none']]))
        if not isinstance(bre.IPCR7, list):
            dataf.at [bre.Index, 'IPCR7' ] = [bre.IPCR7]
        else:
            dataf.at [bre.Index, 'IPCR7' ] = list (set([ipc for ipc in bre.IPCR7 if ipc.lower() not in ['empty', '', 'none']]))
        if not isinstance(bre.IPCR11, list):
            dataf.at [bre.Index, 'IPCR11' ] = [bre.IPCR11]
        else:
            dataf.at [bre.Index, 'IPCR11' ] = list (set([ipc for ipc in bre.IPCR11 if ipc.lower() not in ['empty', '', 'none']]))
        
        if not isinstance(bre.equivalents, list):
            dataf.at [bre.Index, 'equivalents' ] = [bre.equivalents]
        else:
            dataf.at [bre.Index, 'equivalents' ] = list (set([ipc for ipc in bre.equivalents if ipc.lower() not in ['empty', '', 'none']]))
        if not isinstance(bre.CitedBy, list):
            dataf.at [bre.Index, 'CitedBy' ] = [bre.CitedBy]
        else:
            dataf.at [bre.Index, 'CitedBy' ] = list (set([ipc for ipc in bre.CitedBy if ipc.lower() not in ['empty', '', 'none']]))            
        if not isinstance(bre.CitP, list):
            dataf.at [bre.Index, 'CitP' ] = [bre.CitP]
        else:
            dataf.at [bre.Index, 'CitP' ] = list (set([ipc for ipc in bre.CitP if ipc.lower() not in ['empty', '', 'none']]))            
        if not isinstance(bre.CitO, list):
            dataf.at [bre.Index, 'CitO' ] = [bre.CitO]
        else:
            dataf.at [bre.Index, 'CitO' ] = list (set([ipc for ipc in bre.CitO if ipc.lower() not in ['empty', '', 'none']]))     

AnnonceProgres (Appli = 'p2n_network', valMax = 100, valActu = 40)            
dicoAttrsAut = dict() # attributes for author nodes
for aut in Inventeurs:
    # node attributes for an author
    if len(aut) >0:
        IPC11_range = []
        IPC7_range = []
        IPC4_range = []
        [IPC4_range.extend(bre.IPCR4) for bre in  dataf.itertuples() if aut in bre.inventor]
        [IPC7_range.extend(bre.IPCR7) for bre in  dataf.itertuples() if aut in bre.inventor]
        [IPC11_range.extend(bre.IPCR11) for bre in  dataf.itertuples() if aut in bre.inventor]
        
        dicoAttrsAut [aut] = {#'AutFr': dicoAttrsAut [aut]['AutFr'],
                          'Citations' : sum ( [bre.Citations for bre in  dataf.itertuples() if aut in bre.inventor]),
                          'Famille' : sum( [aut in truc for truc in df_Fam ['inventor']]), #.loc[dataf .index[dataf ['label'] ==bre.label ]].values[0],
                          'category' : 'Inventor',
                          'NbBrevets' : sum( [aut in truc for truc in dataf ['inventor']]),
                          'IPC11-range' : len(set(IPC11_range)), # variety of IPC level 11
                          'IPC7-range' : len(set(IPC7_range)),
                          'IPC4-range' : len(set(IPC4_range)),
                          'IPCDiversity': len(set(IPC11_range)), # number of variety
                          'IPCForce' : len(IPC11_range) # same as previous but with occurences
                                        }


dicoAttrsAppli = dict() # attributes for applicant nodes
for aut in Applicants:
    # node attributes for an author
    if len(aut) >0:
        IPC11_range = []
        IPC7_range = []
        IPC4_range = []
        [IPC4_range.extend(bre.IPCR4) for bre in  dataf.itertuples() if aut in bre.applicant]
        [IPC7_range.extend(bre.IPCR7) for bre in  dataf.itertuples() if aut in bre.applicant]
        [IPC11_range.extend(bre.IPCR11) for bre in  dataf.itertuples() if aut in bre.applicant]
        
        dicoAttrsAppli [aut] = {#'AutFr': dicoAttrsAut [aut]['AutFr'],
                          'Citations' : sum ( [bre.Citations for bre in  dataf.itertuples() if aut in bre.applicant]), # sum of citations of each patent 
                          'Famille' : sum( [aut in truc for truc in df_Fam ['applicant']]), # sum of family lenght for each patent of this applicant
                          'category' : 'Applicant',
                          'NbBrevets' : sum( [aut in truc for truc in dataf ['applicant']]), # number of patents
                          'IPC11-range' : len(set(IPC11_range)), # variety of IPC level 11
                          'IPC7-range' : len(set(IPC7_range)),
                          'IPC4-range' : len(set(IPC4_range)),
                          'IPCDiversity': len(set(IPC11_range)), # number of variety
                          'IPCForce' : len(IPC11_range) # same as previous but with occurences
                          
    }                      
dicoAttrs  = dict() # attributes for patent nodes
dicoAttrsCitP = dict()
dicoAttrsCitedBy = dict()
dicoAttrsEquiv  = dict()
dicoAttrsOut = dict()
dicoAttrsTechno = dict()
AnnonceProgres (Appli = 'p2n_network', valMax = 100, valActu = 50)

compt = 0
for ndf in PU:
    
    if 'Families' not in ndf:
        dataf = df
        dataf ['family lenght'] = [1] * len(dataf.index)
    else:
        dataf = df_Fam 
    for bre in dataf.itertuples():
        compt+=1
        AnnonceProgres (Appli = 'p2n_network', valMax = 100, valActu = 50+(50*compt/total))
        dicoAttrs [bre.label] = {'Famille': sum( [bre.label in truc for truc in df_Fam ['equivalents']]),
                                    'IPC11-range': len(set(bre.IPCR11)),
                                    'IPC7-range': len(set(bre.IPCR7)),
                                    'IPC4-range': len(set(bre.IPCR4)),
                                    'Citations' : bre.Citations,
                                    "category" : 'label'
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
                
Networks = dict()
#next lines are here to avoid the changing scheme lecture of requete.cql
Networks["_CountryCrossTech"] =  [configFile.CountryCrossTechNetwork, [ 'IPCR7', "country"]] # not finished yet
Networks["_CrossTech"] =  [configFile.CrossTechNetwork, ['label','IPCR7','IPCR1', 'IPCR4', 'IPCR11']] # GraphTechnos
Networks["_Inventors_CrossTech"] =  [configFile.InventorCrossTechNetwork, ['IPCR11','IPCR7','IPCR4','IPCR1',"Inventor"]] # GraphTechnosAuthor
Networks["_Applicants_CrossTech"] =  [configFile.ApplicantCrossTechNetwork, ['IPCR11','IPCR7','IPCR4','IPCR1', "Applicant"]] # GraphTechnosAppli
Networks["_ApplicantInventor"] = [configFile.ApplicantInventorNetwork, ["Applicant", "Inventor"]] # GraphAuteursAppli
Networks["_Applicants"] =  [configFile.ApplicantNetwork, ["Applicant"]] # GraphApplicant
Networks["_Inventors"] =  [configFile.InventorNetwork, ["Inventor"]] # GraphAuteurs
Networks["_References"] =  [configFile.References, [ 'label', 'CitP', "CitO"]] # GraphBrevetsReferences
Networks["_Citations"] =  [configFile.Citations, [ 'label', "CitedBy"]] # GraphBrevetsCitations
Networks["_Equivalents"] =  [configFile.Equivalents, [ 'label', "equivalent"]] # GraphBrevetsEquivalents
Networks["_LabelApplicants"] =  [configFile.Equivalents, [ 'label', "Applicant"]] # GraphBrevetsEquivalents#GraphBrevets

for ndf in PU:
    
    if 'Families' not in ndf:
        dataf = df
        dataf ['family lenght'] = [1] * len(dataf.index)
    else:
        dataf = df_Fam    
    

    
    Inventeurs = set()
    Applis = []
    Techno = dict()
        # graph init    
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

    for bre in dataf.itertuples():


        GraphBrevets.add_node(bre .label)
        GraphBrevetsCitations.add_node(bre .label)
        GraphBrevetsReferences.add_node(bre .label)
        GraphBrevetsEquivalents.add_node(bre .label)
        GraphTechnos .add_node(bre .label)
        for lab in bre.CitedBy:
            if len(lab)>0:
                GraphBrevetsCitations.add_node(lab)
                GraphBrevetsCitations.add_edge(lab, bre.label)
        
                
        for lab in bre.CitP:
            if len(lab)>0:
            
                GraphBrevetsReferences.add_node(lab)
                GraphBrevetsReferences.add_edge(bre.label, lab)
        for lab in bre.CitO:
            if len(lab)>0:
            
                GraphBrevetsReferences.add_node(lab)
                GraphBrevetsReferences.add_edge(bre.label, lab)
        for lab in bre.equivalents:
            if len(lab)>0:
            
                GraphBrevetsEquivalents.add_node(lab)
                GraphBrevetsEquivalents.add_edge(bre.label, lab)
        joliTecno = list(set([ipc.replace('/', '-') for ipc in bre.IPCR11 if len(ipc)>0]))
        for ipc in bre.IPCR1 + bre.IPCR4 + bre.IPCR7 + joliTecno:
            if ipc in dicoAttrsTechno:
                if 'size' in dicoAttrsTechno [ipc].keys():
                    dicoAttrsTechno [ipc] ['size'] +=1
                else:
                    dicoAttrsTechno [ipc] ['size'] = 1
            GraphTechnos .add_node(ipc)
            GraphTechnosAppli.add_node(ipc)
            GraphTechnosAuthor.add_node(ipc)
        for ipc in joliTecno:
            for ipcUp in bre.IPCR7:
                if ipc.startswith (ipcUp):
                    GraphTechnos .add_edge(ipcUp, ipc)
            
        for ipc in bre.IPCR7:
            for ipcUp in bre.IPCR4:
                if ipc.startswith (ipcUp):
                    GraphTechnos .add_edge(ipcUp, ipc)
        for ipc in bre.IPCR4:
            for ipcUp in bre.IPCR1:
                if ipc.startswith (ipcUp):
                    GraphTechnos .add_edge(ipcUp, ipc)
        
        # for ipcUp in bre.IPCR1:    
        #     GraphTechnos .add_edge(bre .label,ipcUp)
        # chainning technlogy from most precise if existing
        if len(joliTecno)>0:
            for ipc in joliTecno:
                GraphTechnos .add_edge(bre .label,ipc)
        elif len(bre.IPCR7) >0:
            for ipc in bre.IPCR7:
                GraphTechnos .add_edge(bre .label,ipc)
        elif len(bre.IPCR4) >0:
            for ipc in bre.IPCR4:
                GraphTechnos .add_edge(bre .label,ipc)
        else:
            for ipc in bre.IPCR1:
                GraphTechnos .add_edge(bre .label,ipc)         
        
        if not isinstance( bre .applicant, str) and len( bre.applicant)>1:
             for appl in bre .applicant:
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
             for appl, coAut in cycle(bre.applicant):
                 if len(appl)>0 and appl.title() not in Inventeurs and NoPunct(appl).title() not in Inventeurs and appl.lower() != 'empty':
                     GraphBrevets.add_node(appl)
                     GraphBrevets.add_edge(appl, bre .label)
                     GraphApplicant.add_node(appl)
                     GraphTechnosAppli.add_node(appl)
                 if len(coAut)>0 and coAut.title() not in Inventeurs and NoPunct(coAut).title() not in Inventeurs and coAut.lower() != 'empty':
                     GraphBrevets.add_node(coAut)
                     GraphBrevets.add_edge(coAut, bre .label)
                     GraphBrevets.add_edge( appl, coAut)
                     GraphApplicant.add_node(coAut)
                     GraphTechnosAppli.add_node(coAut)
        elif len( bre.applicant)>0:
            appl= bre.applicant [0]
            if len(appl)>0 and appl.title() not in Inventeurs and NoPunct(appl).title() not in Inventeurs and appl.lower() != 'empty':
                GraphBrevets.add_node(appl)
                GraphBrevets.add_edge(appl, bre .label)
                # GraphApplicant.add_node(appl)
                GraphTechnosAppli.add_node(appl)
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
                            
                appl= appl.upper()
                regles= [len(appl)>0,
                          appl.title() not in Inventeurs,
                          NoPunct(appl).title() not in Inventeurs, 
                          ]
                if all(regles):
                    for aut in bre .inventor:
                        aut= aut.title()
                        GraphAuteursAppli.add_edge( aut, appl, label = 'workfor')
        elif len( bre.applicant)>1: # only one applicant
            appl= bre.applicant.upper()
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
    Autnode_sizes = {aut:sum([truc.count(aut) for truc in EdgesAut2]) for aut in set(NoeudAut)}
    Applicantnode_sizes = { appl: sum([truc.count(appl) for truc in EdgesApplicant2]) for appl in set(NoeudApplicant)}
    
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
    
    
    nx.write_gexf(GraphAuteurs, ResultGephiPath+"/"+ndf+"_Inventors.gexf") # GraphAuteurs
    nx.write_gexf(GraphApplicant, ResultGephiPath+"/"+ndf+"_Applicant.gexf") # 
    nx.write_gexf(GraphBrevets, ResultGephiPath+"/"+ndf+"-GraphBrevets.gexf")
    nx.write_gexf(GraphAuteursAppli, ResultGephiPath+"/"+ndf+"_ApplicantInventor.gexf")
    nx.write_gexf(GraphBrevetsEquivalents, ResultGephiPath+"/"+ndf+"_Equivalents.gexf")
    nx.write_gexf(GraphBrevetsReferences, ResultGephiPath+"/"+ndf+"_References.gexf")
    nx.write_gexf(GraphBrevetsCitations, ResultGephiPath+"/"+ndf+"_Citations.gexf")
    nx.write_gexf (GraphTechnos, ResultGephiPath+"/"+ndf+"_CrossTech.gexf")
    nx.write_gexf (GraphTechnosAppli, ResultGephiPath+"/"+ndf+"_Applicants_CrossTech.gexf") 
    nx.write_gexf (GraphTechnosAuthor, ResultGephiPath+"/"+ndf+"_Inventors_CrossTech.gexf")
    
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
        Maxdegs = max([G.degree[node] for node in G.nodes()])
        zoom = len(G) / Maxdegs
        arguDot='-Goverlap="0:prism" -Gsize="1000,800" -GLT=550 -GKsep='+str(zoom)
        pos = nx.spring_layout(G,k=3,iterations=20)
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
            if G.node[k]['category'] == 'label':
                G.node[k]['url'] =UrlPatent(k)[0]
                Visu['color']['a'] = 1
                Visu['color']['r']= int(254)
                Visu['color']['g']= int(0)
                Visu['color']['b']= int(0)
                Visu['shape'] ="diamond"
            elif G.node[k]['category'] =='CitP':
                    Visu['color']['a'] = 1
                    Visu['color']['r']= int(0)
                    Visu['color']['g']= int(254)
                    Visu['color']['b']= int(0)
                    Visu['shape'] ="ellipse"

            elif G.node[k]['category'] == 'CitO':
                # a hack here, trying to find out content in scholar
                #https:/scholar.google.fr/scholar?hl=fr&q=pipo+test&btnG=&lr=
                Visu['color']['r']= int(0)
                Visu['color']['g']= int(0)
                Visu['color']['b']= int(254)
                Visu['color']['a'] =1
                Visu['shape'] ="disc"
                #UrlTemp = "https:/scholar.google.com/scholar?q=" + quot(Nodes.keys()[k])
                #G.node[k]['url'] = UrlTemp
            elif G.node[k]['category'] == 'CitedBy':
                Visu['color']['a'] = 1
                Visu['color']['r']= int(0)
                Visu['color']['g']= int(127)
                Visu['color']['b']= int(127)
                Visu['shape'] ="square"
                G.node[k]['url'] =UrlPatent(k)[0]

            elif G.node[k]['category'] == "equivalents":
                Visu['color']['a'] = 1
                Visu['color']['r']= int(127)
                Visu['color']['g']= int(127)
                Visu['color']['b']= int(0)
                Visu['shape'] ="ellipse"
                G.node[k]['url'] =UrlPatent(k)[0]
            elif G.node[k]['category'] == 'Applicant':
                #G.node[k]['category'] = 'Applicant'# for readable facility
                G.node[k]['url'] = UrlApplicantBuild(k)[0]
                Visu['color']['a'] = 1
                Visu['color']['r']= int(127)
                Visu['color']['g']= int(0)
                Visu['color']['b']= int(127)
                Visu['shape'] ="star"
            elif G.node[k]['category'] == 'IPCR1' or G.node[k]['category'] == 'IPCR3' or G.node[k]['category'] == 'IPCR4' or G.node[k]['category'] == 'IPCR7' or G.node[k]['category'] == 'IPCR7' or G.node[k]['category'] == 'CPC':
                G.node[k]['url'] = UrlIPCRBuild(k)[0]
                Visu['color']['a'] = 1
                Visu['color']['r']= int(127)
                Visu['color']['g']= int(254)
                Visu['color']['b']= int(127)
                Visu['shape'] ="database"
            elif G.node[k]['category'] == 'Inventor':
                #G.node[k]['category'] = 'inventor'# for readable facility
                G.node[k]['url'] = UrlInventorBuild(k)[0]
                Visu['color']['a'] = 1
                Visu['color']['r']= int(127)
                Visu['color']['g']= int(127)
                Visu['color']['b']= int(254)
                Visu['shape'] ="triangleDown"
            else:
                Visu['color']['a'] = 1
                Visu['color']['r']= int(254)
                Visu['color']['g']= int(254)
                Visu['color']['b']= int(0)
            # if "label" not in mixNet:
            #     mixNet.append('label')
            #factx, facty = 500, 400
            # if 'inventor' in G.node[k]['category'] or 'applicant' in G.node[k]['category']:
            #     categ = G.node[k]['category']+'-nice' # for readable facility
            #     count = mixNet.index(categ)
            # else:
            #     count = mixNet.index(G.node[k]['category'])
            count = Networks [network][1].index(G.node[k]['category'])
            Visu['position']= {'x':(int(pos[k][0]*factx)+posx), 'y':(int(pos[k][1]*facty)+posy), 'z':0.0}
            # Visu['size'] = np.log(int(G.node[k]["weight"])+1)+4#
            Visu['color']['a']= count
            G.node[k]['viz'] =dict()


        #            Visu['color']['a']= count

        #        Visu['size'] = (G.node[k]["degree"]*1.0)#(G.node[k]["degree"]*1.0/Maxdegs)*150#(G.node[k]["weight"]) /MaxWeight #addd 1 for viewiong all...
            #Visu['size'] = (G.node[k]["degree"]*zoom) +1 #(G.node[k]["weight"]) /MaxWeight #addd 1 for viewiong all...
            
            Visu['size'] = G.degree [k]*10.0/Maxdegs +4
        #        Visu['size'] = np.log(int(G.node[k]["weight"])+1)*zoom+1#
            for cle in list(Visu.keys()):
                G.node[k]['viz'][cle] = Visu[cle]

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
        fic = open(ResultGephiPath+'/'+outputFile, 'r')

        # Next is a hack to correct the bad writing of the header of the gexf file
        # with dynamics properties
        fictemp=open(ResultGephiPath+'/'+"Good"+outputFile, 'w')


        ecrit = True
        data = fic.read()
        # VERY UGLY Hack here !!!!
        data = data.replace('ns0:', 'viz:') # may be someone knows how to set namespace in networkx...
        data = data.replace('a="None"', '') # may be someone knows why network set the "a" attribute...

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
        print("Network file writen in ",  ResultGephiPath+' directory.\n See file: '+outputFile)
        print()
        print()
        #making the html from model
        RenderTemplate(
            "Graphe.html",
            ResultGephiPath + '/'+outputFile.replace('.gexf','.html'),
            TitleNet=network[1:]+' Network for ' + requete,
            fichierConfigJS=outputFile.replace('.gexf','') +'Conf.js',
            mediaStyle='../../../Patent2Net/media/styles',
            mediaJs='../../../Patent2Net/media/js',
        )

        # making the js from model
        # maybe we could adjust node size and other parameters here
        RenderTemplate(
            "gephiConfig.js",
            ResultGephiPath + '/'+outputFile.replace('.gexf','') +'Conf.js',
            FicRezo=outputFile,
        )

    
    
    
    
    
secondes = time.time() - start_time

heures, secondes = divmod(secondes, 3600)
minutes, secondes = divmod(secondes, 60)
print ('Duree : ', heures, " h ", minutes, " m et ", secondes, " sec")
AnnonceLog (Appli = 'p2n_network', texte='All patents processed ' + str(total) +" in " + str(heures) + " h" +  str(minutes) + " min and " +str(secondes) + " sec")
