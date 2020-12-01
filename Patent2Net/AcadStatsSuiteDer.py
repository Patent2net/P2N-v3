# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 07:41:54 2019

Après moficitation de AcadPuMed2, celui-ci prétraite l'autctorialité pour qualifier les Fr à l'aide de l'affiliation

Le fichier traceAut.csv suit l'entete = "Nom Inventeur ; Nombre publications ; Nombre publication matchées; AffilFr \n"

Ce script à l'aide de ce fichier produit quelques statistiques de publication'
@author: dreymond
"""


import codecs
import os, sys


from pymed import PubMed

from Patent2Net.P2N_Lib import LoadBiblioFile
from Patent2Net.P2N_Config import LoadConfig
from Patent2Net.P2N_Lib_Acad import IPCCategorizer, IPCExtractPredictionBrevet,PubMedCheckNameAndGetAffiliation, OPSChercheAbstractBrevet
from fuzzywuzzy import fuzz

configFile = LoadConfig()
# Les champs nécessaires par brevet.
NeededInfo = ['label', 'date', 'inventor', 'title', 'abstract']

requete = configFile.requete
projectName = configFile.ndf
ndf = projectName
BiblioPath = configFile.ResultBiblioPath
ResultBiblioPath = configFile.ResultBiblioPath
temporPath = configFile.temporPath
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

def Nettoie(Liste):
    indesirables = ['', u'', None, False, [], ' ', "?", "Empty", "empty"]
    Liste = [' '.join([truc.lower().title() for truc in nom.split(' ')]) for nom in Liste ] 
    return list(filter(lambda x: x not in indesirables, Liste))

# test de consistance
with open(Auteur+'//traceAuct.csv', 'r',) as fic:
    dataAuct = fic.readlines()
Auteurs = dict()
for lig in dataAuct:
    lig = lig.strip()
    col= lig.split(';')
    if col[0] not in Auteurs.keys():
        Auteurs [col[0]] = dict()
        Auteurs [col[0]]['publis'] = col [1]
        Auteurs [col[0]]['publisMatch'] = col [2]
        Auteurs [col[0]]['affilFr'] = col [3]
    else:
        if Auteurs [col[0]]['publis'] != col [1]:
            print ("aille")
        if Auteurs [col[0]]['publisMatch'] != col [2]:
            print ("aille")
        if Auteurs [col[0]]['affilFr'] != col [3]:
            print ("aille")
        else:
            pass
DejaVus =Auteurs.keys()        
# if len (set(DejaVus)) == len(DataBrevet['brevets']):
#     print ('Youhou, tous les brevets ' + ndf + ' ont été traités.')
#     print ('Nb de brevets : ', len(DataBrevet['brevets']))
    
# else:
#     reste = [bre['label'] for bre in DataBrevet['brevets'] if bre['label'] not in DejaVus ]
#     print ('il reste ', len(reste), ' brevets à traiter')
 
# Analyse stat des résultats
# print ("""Ceux qui ont changé d'affiliation la première trouvée puis la seconde... 
#        S'il en est plus de deux, ce sera la première puis la 3e....""")
lstfic = os.listdir(configFile.ResultPath +'//AcadCorpora')
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

Inventeurs = []
for bre in DataBrevet['brevets']:
    Inventeurs.extend(Nettoie(bre['inventor']))
Inventeurs1 = [inv for inv in Inventeurs if len(inv.split(' '))<2]
Inventeurs2 = [inv for inv in Inventeurs if inv not in Inventeurs1]
print ("nombre d'inventeurs ", len(Inventeurs))
print ("Nombre d'inventeurs uniques :", len(set(Inventeurs)))
print ("nombre d'auteurs", sum([1 for aut in Auteurs.keys() if int(Auteurs [aut]['publis'])>0]))
print ("nombre d'auteurs FR", sum([1 for aut in Auteurs.keys() if Auteurs [aut]['affilFr'] == 'True']))
print ("nombre d'auteurs pas FR", sum([1 for aut in Auteurs.keys() if Auteurs [aut]['affilFr'] == 'False']))
#print ("nombre de publications", sum([int(Auteurs [aut]['publis']) for aut in Auteurs.keys()])) données fausse dans le fichier trace auc. Des publis mathchées alors que publis = 0 pour certains auteurs

print ("nombre de publications matchées ", sum([int(Auteurs [aut]['publisMatch']) for aut in Auteurs.keys()]))
print ("nombre de publications matchées en AffilFr", sum([int(Auteurs [aut]['publisMatch']) for aut in Auteurs.keys() if Auteurs [aut]['affilFr'] == 'True']))
print ("nombre de publications matchées pas en AffilFr", sum([int(Auteurs [aut]['publisMatch']) for aut in Auteurs.keys() if Auteurs [aut]['affilFr'] == 'False']))

Inventeur_Norm = dict()
InvDejaVus = []
import copy
Inventeurs = set(Inventeurs)
InventeurSafe = copy.copy(Inventeurs)

# for inv in Inventeurs:
#     if inv not in DejaVus:
#         reste = Inventeurs- set([inv]+InvDejaVus)
#         InvDejaVus.append(inv)
#         for inv2 in reste:
#             if fuzz.token_sort_ratio(inv, inv2)>89:
#                 if len(inv) == len(inv2) and inv.split()[0] != inv2.split()[1] and '-' not in inv and '-' not in inv2:
#                     print ("Suspects : ", inv, inv2)
#                 InvDejaVus.append(inv2)
#                 if inv in Inventeur_Norm.keys():
#                     Inventeur_Norm [inv].append(inv2)                    
#                 else:
#                     Inventeur_Norm [inv] = [inv2]

# Estrangers = [inv for inv in Inventeurs2 if inv not in Auteurs.keys() and inv.split(' ')[1] + inv.split(' ')[0] not in Auteurs.keys()]
# Estrangers += [inv for inv in Inventeurs1 if inv not in Auteurs.keys()]
# print ("nombre d'inventeurs non affiliés FR", len(Estrangers))
#distFonct = lambda x: { cle: max([fuzz.token_set_ratio( x, aut) for aut in Inventeurs]) for cle in Auteurs}
# print ("Nouvelles stats")
# BadCasInv = dict()
# for inv in Inventeur_Norm.keys():
#     if isinstance(Inventeur_Norm [inv], list):
#         for inv2 in Inventeur_Norm [inv]:
#             BadCasInv [inv2] = inv
#     else:
#         BadCasInv [Inventeur_Norm [inv]] = inv
        
# print ("Nombre d'inventeurs rectifiants les erreurs de saisie :", len(set(Inventeurs))-len(BadCasInv.keys()))

# Traitement des dossiers et des abstracts collectés

def GenereListeFichiers(rep):
    """ prend un auteur en paramètre (chemin absolu) et génère la liste
    complète des fichiers TXT et CSV de l'arborescence"""
    import os
    listeFicCSV = []
    listeFicTXT = []
    for lang in ['Fr', 'NoFr']: # depending the affiliation (France or not) of the author of an article, the directory is one or other
        
        for ficOuRep in os.listdir(rep +'//'+lang):
    
            if "." not in ficOuRep:
                for fic in os.listdir( rep +'//'+lang +'//' +ficOuRep):

                             if fic.endswith('.csv'):
                                 listeFicCSV.append(rep+'//'+lang+"//"+ficOuRep +'//' +fic)
                             elif fic.endswith('.txt'):
                                 listeFicTXT.append(rep+'//'+lang+"//"+ficOuRep+'//'  +fic)
                             else:
                                 pass
    
    #                listeFicCSV.extend(temporar[0])
    #                listeFicTXT.extend(temporar[1])
    #                listeFicUNK.extend(temporar[2])
            else:
               pass
    #                if ficOuRep.endswith('.csv'):
    #                    listeFicCSV.append(root+'//'+fichier)
    #                elif ficOuRep.endswith('.txt'):
    #                    listeFicTXT.append(root+'//'+fichier)
    #                else:
    #                    pass
                    
    return (list(set(listeFicCSV)), list(set(listeFicTXT)))


Csv, IRams = GenereListeFichiers(Auteur)
matches, CountBadNomMatches, CountBadNomPubMed = 0, 0,0, 0
pasMatches =0
Scores = []     # la liste des scores de chaque IPCat
Matches = dict()
PasMatches=dict()
cptPubli = 0
for ficCsv in Csv:
    with open(ficCsv, "r", encoding='utf8') as ficcsv:
        Datacsv=ficcsv.readlines()
    
    if len(Datacsv) >1:
        enTete = [Datacsv[0]]
        enTete.extend(list(set(Datacsv[1:])))
        Datacsv = enTete
        
        with open(ficCsv, "w", encoding='utf8') as ficcsvNet:
           ficcsvNet.write("".join(Datacsv))
        
    
    temp = ficcsv.name.split('//')[3]
    First = False
    VraiNom = ''
    Numro = ''
    for lettre in temp:
        if not lettre.isnumeric():
            if lettre.lower() != lettre and not First:
                VraiNom += ' ' + lettre
            elif lettre != '-':
                VraiNom +=lettre
                if lettre.lower() != lettre:
                    First = True
        else:
            Numro += lettre
    #decodage
    VraiNom = VraiNom.replace('- ', '-')
    if len(Datacsv)>2:
        matches+=1 # publications matchées IPC
        
        for lig in Datacsv:
            if not lig.startswith('Label Brevet'):
                cptPubli += 1
                dat = lig.split(';')
                if len(dat)>9:
                    if dat[9].isnumeric():
                        Scores.append(int(dat[9]))
                    else: #quelquefois le champs score est décalé... un ";" dans les données ???
                        Scores.append(int(dat[10]))
        ScoreMoy = sum(Scores)*1.0/len(Scores)
        if VraiNom[1:].strip() not in Matches.keys():
            Matches [VraiNom[1:].strip()] = [[ficCsv],
                                             len(Datacsv)-1, # Match par auteur
                                             len(os.listdir("/".join(ficCsv.split('/')[0:len(ficCsv.split('/'))-1])+'publis')), #nb publications
                                             len(Datacsv)-1, ScoreMoy]
        else:
            temp = Matches [VraiNom[1:].strip()][0]
            temp.append(ficCsv)
            if Matches [VraiNom[1:].strip()][1]  != len(Datacsv)-1:
                print ()
            Matches [VraiNom[1:].strip()] = [temp, 
                                             Matches [VraiNom[1:].strip()][1] + len(Datacsv)-1,
                                             len(os.listdir("/".join(ficCsv.split('/')[0:len(ficCsv.split('/'))-1])+'publis')),
                                             len(Datacsv)-1, (Matches [VraiNom[1:].strip()][2] + ScoreMoy)/2]

        # if VraiNom[1:].strip() in BadCasInv:
        #     CountBadNomMatches +=1
    else:
        pasMatches += 1
        if VraiNom[1:].strip() not in PasMatches.keys():
            PasMatches [VraiNom[1:].strip()] = [ficCsv]
        else:
            PasMatches [VraiNom[1:].strip()].append(ficCsv)


print ("Nombre d'auteurs/affiliations identifiés ", len(Csv))
#print ("Nombre d'auteurs affiliés Fr et NoFr ", )
print ("Nombre d'auteurs No Fr identifiés avec publications", sum([1 for fic in ficCsv if len(os.listdir("/".join(ficCsv.split('/')[0:len(ficCsv.split('/'))-1])+'publis'))>0]))
print ("Nombre d'auteurs FR identifiés avec publications", sum([1 for fic in Csv if "/Fr/" in fic and len(os.listdir("/".join(fic.split('/')[0:len(fic.split('/'))-1])+'publis'))>0]))

print ("Nombre de publications traitées des auteurs FR", sum([len(os.listdir("/".join(fic.split('/')[0:len(fic.split('/'))-1])+'publis')) for fic in Csv if "/Fr/" in fic]))
print ("Nombre  de publications traitées des auteurs no affil FR", sum([len(os.listdir("/".join(fic.split('/')[0:len(fic.split('/'))-1])+'publis')) for fic in Csv if "/NoFr/" in fic]))


print("Nombre de brevets matchés (le même auteur dans plusieurs brevets) ", sum([len(Matches[aut][0]) for aut in Matches.keys()]))

# print ("Nombre de publications traitées ", )

print("Nombre d'auteurs (uniques) identifiés avec publi  pubmed matchées IPCCat", len(Matches.keys()) )
print("Nombre d'auteurs (uniques) identifiés sans publi matchées IPCCat", len(PasMatches.keys()) )
print("Nombre d'auteurs à publications matchées", len(Matches.keys()) )
print("Max par auteur du nomnbre de publications matchées", max([len(Matches[aut][0]) for aut in Matches.keys()]))
print ("nombre de publications matchées ", cptPubli )



with open(RepDir + "//AuteursMatches.tsv", "w", encoding = 'utf8') as ficMatch:
    
    ficMatch.write('Auteur \t Nombre match \t Articles \t Score moyen \t\n')
    for aut in Matches.keys():
        if Matches[aut][1] == Matches[aut][3]:
            ficMatch.write(aut + '\t' +   str(Matches[aut][1]) +'\t' +  str(Matches[aut][2]) +'\t' +  str(Matches[aut][4]) +'\t\n')
        else:
            ficMatch.write(aut + '\t' +   str(Matches[aut][1] - Matches[aut][3]) +'\t' +  str(Matches[aut][2]) +'\t' +  str(Matches[aut][4]) +'\t\n')            
        

with open(RepDir + "//AuteursPAsMatches.tsv", "w", encoding = 'utf8') as ficMatch:
    ficMatch.write('Auteur \t\n')
    for aut in PasMatches.keys():
        ficMatch.write(aut +  '\t\n')


        
#echantillonge. Partie du script qui extrait des corpus un échantillon aléatoire de taille 10% du corpus
# en séparant les matchés des pas matchés afin de qualifier le process
# 

# import random
# from pathlib import Path, PureWindowsPath
# LstAuteurs= list(Matches.keys())
# #Liste = random.sample(range(0, 10, 1),5) #round(len(LstAuteurs)/9))) #len(LstAuteurs)-1)
# Liste = random.sample(range(0,len(LstAuteurs)-1), round(len(LstAuteurs)/9))
# loupes=0
# DossierDestination = "EchantillonMatches"
# os.mkdir(configFile.ResultPath +'//AcadCorpora//' + DossierDestination)
# with open (configFile.ResultPath +'//AcadCorpora//'+DossierDestination+'//QualificationMatch.csv', "w", encoding = 'utf8') as ficRes:
#     ficRes.write('Auteur;OK;Commentaires;URL;Résume brevet;Résumé Article;CIB Match;score Max IPCCat;Affiliation\n')
#     for num in Liste:
#         if LstAuteurs[num] not in BadCasInv.keys():
#             rep =[truc for truc in lstfic if truc.count(LstAuteurs[num].replace(' ', ''))>0]
#             if len(rep) >0:
#                 filename = PureWindowsPath(Path(configFile.ResultPath.replace('/', '\\') +'\\AcadCorpora\\'+rep[0]))
#                 dest = PureWindowsPath(Path(configFile.ResultPath.replace('/', '\\') +'\\AcadCorpora\\'+DossierDestination+'\\Echantillon\\'))
#                 Auteur =  LstAuteurs[num]
#                 ficCsvAut = Auteur.title().replace(' ', '').replace('"', '') + 'Match.csv'
#                 ficCsvAut2 ='-'.join(rep[0].split('-')[1:])+ 'Match.csv'
#                 filename2 = PureWindowsPath(Path(configFile.ResultPath.replace('/', '\\') +'\\AcadCorpora\\'+rep[0]+'\\'+ficCsvAut))
#                 filename3 = PureWindowsPath(Path(configFile.ResultPath.replace('/', '\\') +'\\AcadCorpora\\'+rep[0]+'\\'+ficCsvAut2))
#                 os.system('xcopy /I %s %s' % (filename, dest))
#                 try:
#                     with open(filename2, 'r', encoding = 'utf8') as ficSrc:
#                         lignes = ficSrc.readlines()
#                 except: #les noms composés
#                     with open(filename3, 'r', encoding = 'utf8') as ficSrc:
#                         lignes = ficSrc.readlines()

#                 Entete= enTete[0]
                
#                 for lig in lignes[1:]:
#                     col = lig.split(';')
#                     # label URL\#Résumé# Résumé article# CIB Match# Score Max # Affiliation
#                     contenu = ';;;https://worldwide.espacenet.com/patent/search?q=pn %3D '+ col [0] +\
#                                  ';' + col [1] + ';' + col [6] + ';'+ col [8] + ';' + col [9] + ';' + col [11] +"\n"   
#                     ficRes.write(Auteur+ contenu)                      
#             else:
#                 loupes+=1
#                 print(LstAuteurs[num])
#         else:
#             loupes+=1
#             print(LstAuteurs[num])
# print("Loupés des matchés", loupes)    

# loupes=0
# LstAuteurs= list(PasMatches.keys())
# Liste = random.sample(range(0,len(LstAuteurs)-1), round(len(LstAuteurs)/9))
# with open (configFile.ResultPath +'//AcadCorpora//'+DossierDestination+'//QualificationMatch2.csv', "w", encoding = 'utf8') as ficRes:
#     with open (configFile.ResultPath +'//AcadCorpora//'+DossierDestination+'//QualificationMatch.csv', "r", encoding = 'utf8') as ficSrc:
#         for lig in ficSrc.readlines():
#             if len(lig.strip().replace(' ','')) >0:
#                 ficRes.write(lig)
#             else:
#                 pass
    

# DossierDestination = "EchantillonNONMatches"
# os.mkdir(configFile.ResultPath +'//AcadCorpora//' + DossierDestination)
# with open (configFile.ResultPath +'//AcadCorpora//'+DossierDestination+'//QualificationPasMatch.csv', "w", encoding = 'utf8') as ficRes:
#     ficRes.write('Auteur;OK;Commentaires;URL;Résume brevet;Résumé Article;CIB Match;score Max IPCCat;Affiliation\n')
#     for num in Liste:
#         if LstAuteurs[num] not in BadCasInv.keys():
#             rep =[truc for truc in lstfic if truc.count(LstAuteurs[num].replace(' ', ''))>0]
#             if len(rep) >0:
#                 filename = PureWindowsPath(Path(configFile.ResultPath.replace('/', '\\') +'\\AcadCorpora\\'+rep[0]))
#                 dest = PureWindowsPath(Path(configFile.ResultPath.replace('/', '\\') +'\\AcadCorpora\\'+DossierDestination+'\\Echantillon\\'))
#                 Auteur =  LstAuteurs[num]
#                 ficCsvAut = Auteur.title().replace(' ', '').replace('"', '') + 'Match.csv'
#                 filename2 = PureWindowsPath(Path(configFile.ResultPath.replace('/', '\\') +'\\AcadCorpora\\'+rep[0]+'\\'+ficCsvAut))
#                 os.system('xcopy /I %s %s' % (filename, dest))
#                 ficCsvAut2 ='-'.join(rep[0].split('-')[1:])+ 'Match.csv'
#                 filename3 = PureWindowsPath(Path(configFile.ResultPath.replace('/', '\\') +'\\AcadCorpora\\'+rep[0]+'\\'+ficCsvAut2))
#                 try:
#                     with open(filename2, 'r', encoding = 'utf8') as ficSrc:
#                         lignes = ficSrc.readlines()
#                 except: #les noms composés
#                     with open(filename3, 'r', encoding = 'utf8') as ficSrc:
#                         lignes = ficSrc.readlines()

#                 Entete= enTete[0]
#                 if len(lignes)==1:
#                     ficRes.write(Auteur +';;;\n') 
                    
#                 for lig in lignes[1:]:
#                     col = lig.split(';')
                    
#                     # label URL\#Résumé# Résumé article# CIB Match# Score Max # Affiliation
#                     contenu = ';;;https://worldwide.espacenet.com/patent/search?q=pn %3D '+ col [0] +\
#                                  ';' + col [1] + ';' + col [6] + ';' + col [8] + ';'+ col [9] + ';' + col [11] +"\n"   
#                     ficRes.write(Auteur+ contenu)                      
#             else:
#                 loupes+=1
#                 print(LstAuteurs[num])
#         else:
#             loupes+=1
#             print(LstAuteurs[num])
# print("Loupés des NON matchés", loupes)      

# with open (configFile.ResultPath +'//AcadCorpora//'+DossierDestination+'//QualificationPasMatch2.csv', "w", encoding = 'utf8') as ficRes:
#     with open (configFile.ResultPath +'//AcadCorpora//'+DossierDestination+'//QualificationPasMatch.csv', "r", encoding = 'utf8') as ficSrc:
#         for lig in ficSrc.readlines():
#             if len(lig.strip().replace(' ','')) >0:
#                 ficRes.write(lig)
#             else:
#                 pass

