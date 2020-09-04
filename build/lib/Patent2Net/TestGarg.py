# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 07:58:47 2019

@author: dreymond
"""

from gargDown_biblio import newCorpus, get_resource_by_name, parse2
import pickle
import os
os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'#cacert.pem
os.environ['CA_BUNDLE'] = 'cacert.pem'
import requests

import json
project = "Data"



### =============================================================================
### # décommenter pour sauvegarder dans un fichier 
### =============================================================================
#with open ('test'+corpus1['fileName']+'.pkl', 'wb') as fic:
#    pickle.dump(corpus1, fic)
### =============================================================================
## # décommenter pour utiliser une sauvegarde (et commenter ce qui précède jusqu'à la ligne 16)    
## =============================================================================
##with open ('test'+corpus1['fileName']+'.pkl', 'rb') as fic:
##    corpus1 = pickle.load( fic)    
## =============================================================================
## Analyse lexicale et extraction des champs
## parse2 sauvegarde dans un fichier corpus1['fileName'].txt (à l'arrache, à la racine à côté de ce script)
## #
## =============================================================================
#parse2(corpus1)
#
##Corpus ISTEX
##corpus2 = dict()
##corpus2['name'] = 'ISTex'
##corpus2['fileName'] = 'ISTex'#Adapter à la requete
##corpus2['ressources'] = get_resource_by_name(corpus2['name'] )
##corpus2['path'] = newCorpus(project, source="ISTex", name="testIstex", query="author.name:(David AND Reymond)")
#
##0 =============================================================================
# #Mémorise le résultat de la collecte (pour éviter de relancer 2000 fois pour affiner le code)
# #même commentaires
## =============================================================================
##with open ('test'+corpus2['fileName']+'.pkl', 'wb') as fic:
##    pickle.dump(corpus2, fic)
#    
##with open ('test'+corpus2['fileName']+'.pkl', 'rb') as fic:
##    corpus2 = pickle.load( fic)    
#
## =============================================================================
## # Analyse lexicale et extraction des champs
## =============================================================================
##parse2(corpus2)
##print 
# =============================================================================
 #Corpus PubMed
# =============================================================================
from gargDown.util.parsers.PUBMED import PubmedParser
corpus4 = dict()
corpus4['name'] = 'Pubmed [XML]'
corpus4['fileName'] = 'Pubmed' #Adapter à la requete
corpus4['ressources'] = get_resource_by_name(corpus4['name'] )
corpus4['path'] = newCorpus(project, source="pubmed", name="test", query="Cédric Reymond[Author - Full]")
test = PubmedParser(list(corpus4['path'])[0][1])
pipo = test.parse(test._file)

#Tout pareil
with open ('test'+corpus4['fileName']+'.pkl', 'wb') as fic:
    pickle.dump(corpus4, fic)

#with open ('test'+corpus4['fileName']+'.pkl', 'rb') as fic:
#    corpus4 = pickle.load(fic)

parse2(corpus4)
