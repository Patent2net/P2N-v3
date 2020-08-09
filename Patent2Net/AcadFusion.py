# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 09:04:52 2020

@author: david
"""

fichierAtraiter = ["MalNommes.tsv", "DejaTraites.csv","AuteursPAsMatches.tsv", "AuteursMatches.tsv", "AuteursAffil.csv" ]
reps = ['P7-Largebis1', 'P7-Largebis2','P7-Largebis3', 'P7-Largebis4']
repDest= 'P7-LargeBis'


for fichier in fichierAtraiter:
    data = []
    for repSrc in reps:
        fic = '../DATA/'+repSrc+"/AcadCorpora/"+fichier
        with open(fic, 'r', encoding='utf8') as ficSrc:
                for ligne in ficSrc.readlines():
                    data.append(ligne)
    with open('../DATA/'+repDest+'/AcadCorpora/'+fichier, 'w', encoding='utf8') as ficRes:
        for ligne in data:
            ficRes.write(ligne)