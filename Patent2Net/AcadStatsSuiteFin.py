# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 07:41:54 2019

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
    DejaVus = fic.readlines()

if len (set(DejaVus)) == len(DataBrevet['brevets']):
    print ('Youhou, tous les brevets ' + ndf + ' ont été traités.')
    print ('Nb de brevets : ', len(DataBrevet['brevets']))
    
else:
    reste = [bre['label'] for bre in DataBrevet['brevets'] if bre['label'] not in DejaVus ]
    print ('il reste ', len(reste), ' brevets à traiter')
 
# Analyse stat des résultats
print ("""Ceux qui ont changé d'affiliation la première trouvée puis la seconde... 
       S'il en est plus de deux, ce sera la première puis la 3e....""")
lstfic = os.listdir(configFile.ResultPath +'//AcadCorpora')
with codecs.open(configFile.ResultPath +'//AcadCorpora//AuteursAffil.csv', 'r', 'utf8') as fic:
    data = fic.readlines()
multiAut = 0  # inventeurs prolixes
AffilDiff = 0   # les affiliations différentes
Auteurs = dict()
for lig in data:
    col = lig   .strip()
    col = col.split(';')
    if col[0] not in Auteurs.keys():
        Auteurs [col[0]] = col[1]
    else:
        if col[1] != Auteurs [col[0]]:
            print (col[0], " --> ", Auteurs [col[0]])
            print (col[0], " --> ", col[1])
            
            AffilDiff +=1
            multiAut+=1  # non sens, le script peut recollecter plusieurs fois le même
        else:
            multiAut+=1
            pass

Inventeurs = []
for bre in DataBrevet['brevets']:
    Inventeurs.extend(Nettoie(bre['inventor']))
Inventeurs1 = [inv for inv in Inventeurs if len(inv.split(' '))<2]
Inventeurs2 = [inv for inv in Inventeurs if inv not in Inventeurs1]
print ("Nombre d'auteurs identifiés sur PubMed ", len(list(Auteurs.keys())), " et le nombre d'inventeurs ", len(Inventeurs))
print ("Les auteurs inventeurs .... mais pour ces stats : Nom Prénom est différent de Prénom Nom" )

Inventeur_Norm = dict()
InvDejaVus = []
import copy
Inventeurs = set(Inventeurs)
InventeurSafe = copy.copy(Inventeurs)
print ("Nombre d'inventeurs :", len(set(Inventeurs)))
for inv in Inventeurs:
    if inv not in DejaVus:
        reste = Inventeurs- set([inv]+InvDejaVus)
        InvDejaVus.append(inv)
        for inv2 in reste:
            if fuzz.token_sort_ratio(inv, inv2)>89:
                if len(inv) == len(inv2) and inv.split()[0] != inv2.split()[1] and '-' not in inv and '-' not in inv2:
                    print ("Suspects : ", inv, inv2)
                InvDejaVus.append(inv2)
                if inv in Inventeur_Norm.keys():
                    Inventeur_Norm [inv].append(inv2)                    
                else:
                    Inventeur_Norm [inv] = [inv2]

Estrangers = [inv for inv in Inventeurs2 if inv not in Auteurs.keys() and inv.split(' ')[1] + inv.split(' ')[0] not in Auteurs.keys()]
Estrangers += [inv for inv in Inventeurs1 if inv not in Auteurs.keys()]
print ("nombre d'inventeurs non affiliés FR", len(Estrangers))
#distFonct = lambda x: { cle: max([fuzz.token_set_ratio( x, aut) for aut in Inventeurs]) for cle in Auteurs}
print ("Nouvelles stats")
BadCasInv = dict()
for inv in Inventeur_Norm.keys():
    if isinstance(Inventeur_Norm [inv], list):
        for inv2 in Inventeur_Norm [inv]:
            BadCasInv [inv2] = inv
    else:
        BadCasInv [Inventeur_Norm [inv]] = inv
        
print ("Nombre d'inventeurs rectifiants les erreurs de saisie :", len(set(Inventeurs))-len(BadCasInv.keys()))

# Traitement des dossiers et des abstracts collectés

def GenereListeFichiers(rep):
    """ prend un dossier en paramètre (chemin absolu) et génère la liste
    complète des fichiers TXT et CSV de l'arborescence"""
    import os
    listeFicCSV = []
    listeFicTXT = []

    for ficOuRep in os.listdir(rep):

        if "." not in ficOuRep:
            for fic in os.listdir(rep+'//'+ficOuRep):
                #for fic in os.listdir(root+"//"+sousRep):
               # temporar = GenereListeFichiers(rep+'//'+sousRep)

                         if fic.endswith('.csv'):
                             listeFicCSV.append(rep+"//"+ficOuRep+'//'+fic)
                         elif fic.endswith('.txt'):
                             listeFicTXT.append(rep+"//"+ficOuRep+'//'+fic)
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
matches, NotFound, CountBadNomMatches, CountBadNomPubMed = 0, 0,0, 0
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
        
    
    temp = ficcsv.name.split('//')[2]
    #Nom=temp.split('-')[1]
    First = False
    VraiNom = ''
    Numro = ''
    for lettre in temp:
        if not lettre.isnumeric():
            if lettre.lower() != lettre and not First:
                VraiNom += ' ' + lettre
            else:
                VraiNom +=lettre
                if lettre.lower() != lettre:
                    First = True
        else:
            Numro += lettre
    #decodage
    VraiNom = VraiNom.replace('- ', '-')
    if VraiNom[1:].strip() in Auteurs.keys():
        if VraiNom[1:].strip() in BadCasInv.keys():
            CountBadNomPubMed +=1
#            if VraiNom[1:].strip() in BadCasInv.keys():
#                BadCasInv [VraiNom[1:].strip()] 
#            #☻ on pourrait rassembler ici toutes lesprod d'un même gugusse
        else:
            GoodException = []
            for nom in BadCasInv.keys():
                if fuzz.token_set_ratio(nom, VraiNom[1:].strip()) >85:
                    GoodException.append(nom)
            if len(GoodException) == 1:
                VraiNom = ' '+GoodException [0] #on l'a retrouvé
            elif len(GoodException) == 0:
                pass
            else:
                
                VraiNom = ' '+GoodException [0]
#        else:
#            with open(ficCsv, "w", encoding='utf8') as ficcsvNet:
#                ficcsvNet.write("".join(Datacsv))
    else:
        
        pass
        
#        print(VraiNom)        
    #denombrement

    #sauvegarde de la version nettoyée


    if len(Datacsv)>1:
        matches+=1 # Mauvais compteurs si le processe de collecte n'a pas été correctement aboutit (en une fois)
        
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
        Matches [VraiNom[1:].strip()] = [Numro, str(len(Datacsv)-1), str(ScoreMoy)]
        if VraiNom[1:].strip() in BadCasInv:
            CountBadNomMatches +=1
    else:
        PasMatches [VraiNom[1:].strip()] = Numro
        NotFound+=1 # Mauvais compteurs si le processe de collecte n'a pas été correctement aboutit

print("Nombre d'auteurs identifiés (le même auteur dans plusieurs brevets) ", matches)
print("Nombre d'auteurs identifiés sans publi", NotFound)
print("Nombre d'auteurs (uniques) identifiés avec publi  pubmed matchées IPCCat", len(Matches.keys()) )
print("Nombre d'auteurs (uniques) identifiés sans publi matchées IPCCat", len(PasMatches.keys()) )

print("Nombre d'auteurs identifiés (mal orthogr) sans publi matchées IPCCat", CountBadNomPubMed)
print("Nombre d'auteurs identifiés (mal orthogr) avec publi matchées IPCCat", CountBadNomMatches )
print ("nombre de publications traitées ", cptPubli )
# Normalisation sur Mauvaise orthogrphes
pasGrave = 0 #les cas où c'est pas si grave (pas un vrai auteur puisque mal ortho et pas de publi)
MatchMalOrtho = dict()
for aut in Matches.keys():
    if aut in BadCasInv.keys():
        if BadCasInv [aut] in Matches.keys():
            MatchMalOrtho [aut] = [Matches [aut]]
            
            if Matches[BadCasInv [aut]] == Matches [aut]:
                print ("remove key ?")
            else:
                MatchMalOrtho [aut].append( Matches [BadCasInv [aut]])
                
        elif BadCasInv [aut] in PasMatches.keys():
            #La cas où un inventeur est un auteur mais sa version mal orthographiée non
            pass # faudrait virer de ce côté la ligne
        else:
            
            pasGrave += 1 # 
            #print ('wtf')
    else:
        pass

with open(RepDir + "//AuteursMatches.tsv", "w", encoding = 'utf8') as ficMatch:
    
    ficMatch.write('Auteur \t Numéro \t  Nombre Articles \t Score \t\n')
    for aut in Matches.keys():
        ficMatch.write(aut + '\t' +  Matches[aut][0]+ '\t' +  str(Matches[aut][1]) +'\t' +  str(Matches[aut][2]) +'\t\n')
        

with open(RepDir + "//AuteursPAsMatches.tsv", "w", encoding = 'utf8') as ficMatch:
    ficMatch.write('Auteur \t Numéro \t\n')
    for aut in PasMatches.keys():
        ficMatch.write(aut + '\t' +  PasMatches[aut]+ '\t\n')

with open(RepDir + "//MalNommes.tsv", "w", encoding = 'utf8') as ficMatch:
    ficMatch.write('Auteur \t Déclinaisons \t\n')
    for aut in Inventeur_Norm.keys():
        Ligne = aut + '\t' 
        for Badaut in Inventeur_Norm [aut]:
            Ligne+= Badaut +'\t'
            
            
        ficMatch.write(Ligne + '\n')
        
#echantillonga

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

