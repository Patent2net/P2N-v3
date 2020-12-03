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


from Patent2Net.P2N_Lib import LoadBiblioFile, AnnonceProgres, AnnonceLog
from Patent2Net.P2N_Config import LoadConfig
#from Patent2Net.P2N_Lib_Acad import IPCCategorizer, IPCExtractPredictionBrevet,PubMedCheckNameAndGetAffiliation, OPSChercheAbstractBrevet
from Patent2Net.P2N_Lib_Acad import  NoPunct #, CheckListInclu, CheckListMix, CheckListExclu, UnCheck, Check
#from fuzzywuzzy import fuzz

#from dateutil.relativedelta import relativedelta
import networkx as nx
#import matplotlib.pyplot as plt
#from networkx.readwrite import json_graph
import pandas as pd
#import string
#import re
#import unidecode

                               
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
                          'type' : 'Inventor',
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
                          'type' : 'Applicant',
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
                                    "type" : 'brevet'
                                    #'NbBrevets' : 1
                                    }
        for lab in bre.CitP:
            dicoAttrsCitP [lab] = {"type" : 'citing'
                }
        for lab in bre.CitedBy:
            dicoAttrsCitedBy [lab] = {"type" : 'cited by'
                }
        for lab in bre.equivalents:
            dicoAttrsEquiv [lab] = {"type" : 'equivalent'
                }
        for lab in bre.CitO: # we may get in trouble here
            dicoAttrsOut [lab] = {"type" : 'citing ref other than patents'
                }
        for ipc in bre.IPCR1:
            if len(ipc)>0 and ipc not in dicoAttrsTechno.keys():
                dicoAttrsTechno [ipc] = {'type' : "IPC1"}
        for ipc in bre.IPCR4:
            if len(ipc)>0 and ipc not in dicoAttrsTechno.keys():
                dicoAttrsTechno [ipc] = {'type' : "IPC4"}
        for ipc in bre.IPCR7:
            if len(ipc)>0 and ipc not in dicoAttrsTechno.keys():
                dicoAttrsTechno [ipc] = {'type' : "IPC7"}
        for ipc in bre.IPCR11:
            ipc = ipc.replace('/', '-')
            if len(ipc)>0 and ipc not in dicoAttrsTechno.keys():
                dicoAttrsTechno [ipc] = {'type' : "IPC11"}
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
            GraphBrevetsCitations.add_node(lab)
            GraphBrevetsCitations.add_edge(lab, bre.label)
        
                
        for lab in bre.CitP:
            GraphBrevetsReferences.add_node(lab)
            GraphBrevetsReferences.add_edge(bre.label, lab)
        for lab in bre.CitO:
            GraphBrevetsReferences.add_node(lab)
            GraphBrevetsReferences.add_edge(bre.label, lab)
        for lab in bre.equivalents:
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
    
    
    nx.write_gexf(GraphAuteurs, ResultGephiPath+"/"+ndf+"-GraphAuteurs.gexf")
    nx.write_gexf(GraphApplicant, ResultGephiPath+"/"+ndf+"-GraphApplicant.gexf")
    nx.write_gexf(GraphBrevets, ResultGephiPath+"/"+ndf+"-GraphBrevets.gexf")
    nx.write_gexf(GraphAuteursAppli, ResultGephiPath+"/"+ndf+"-GraphAppliAuteurs.gexf")
    nx.write_gexf(GraphBrevetsEquivalents, ResultGephiPath+"/"+ndf+"-GraphEquivalents.gexf")
    nx.write_gexf(GraphBrevetsReferences, ResultGephiPath+"/"+ndf+"-GraphReferences.gexf")
    nx.write_gexf(GraphBrevetsCitations, ResultGephiPath+"/"+ndf+"-GraphCitations.gexf")
    nx.write_gexf (GraphTechnos, ResultGephiPath+"/"+ndf+"-GraphIPCs.gexf")
    nx.write_gexf (GraphTechnosAppli, ResultGephiPath+"/"+ndf+"-GraphIPCsApplicants.gexf")
    nx.write_gexf (GraphTechnosAuthor, ResultGephiPath+"/"+ndf+"-GraphIPCsInventors.gexf")
secondes = time.time() - start_time

heures, secondes = divmod(secondes, 3600)
minutes, secondes = divmod(secondes, 60)
print ('Duree : ', heures, " h ", minutes, " m et ", secondes, " sec")
AnnonceLog (Appli = 'p2n_network', texte='All patents processed ' + str(total) +" in " + str(heures) + " h" +  str(minutes) + " min and " +str(secondes) + " sec")
