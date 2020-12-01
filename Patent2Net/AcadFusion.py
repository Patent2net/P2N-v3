# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 09:04:52 2020

@author: david
"""
import os, shutil
fichierAtraiter = ["MalNommes.tsv", "DejaTraites.csv","AuteursPAsMatches.tsv", "AuteursMatches.tsv", "AuteursAffil.csv" ]
reps = ['P7-Largebis1', 'P7-Largebis2','P7-Largebis3', 'P7-Largebis4']
repDest= 'P7-LargeBisFin'


for fichier in fichierAtraiter:
    data = []
    for repSrc in reps:
        # copie des repertoires auteurs
        dest = '../DATA/'+repDest+"/AcadCorpora/"            
        for rep in os.listdir("../DATA/"+repSrc+"/AcadCorpora/"):
            try:
                shutil.copytree("../DATA/"+repSrc+"/AcadCorpora/"+rep, dest+rep) 
            except:
                pass #devrait être un des fichiers qui sont traités après
        #mise en mémoire
        fic = '../DATA/'+repSrc+"/AcadCorpora/"+fichier
        with open(fic, 'r', encoding='utf8') as ficSrc:
                for ligne in ficSrc.readlines():
                    data.append(ligne)
    # écriture des fichiers de traitements (Match ou pas, coquilles de noms, affiliations et déjà traités)
    with open('../DATA/'+repDest+'/AcadCorpora/'+fichier, 'w', encoding='utf8') as ficRes:
        for ligne in data:
            ficRes.write(ligne)