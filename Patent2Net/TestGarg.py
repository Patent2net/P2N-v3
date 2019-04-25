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

# =============================================================================
# # Corpus HAL
# =============================================================================
# =============================================================================
## =============================================================================
def CollecteHal(Auteur, start, nbColl):
    UrlHal = "https://api.archives-ouvertes.fr/search/?q="
    req = "authFullName_s:%s&start=%s&fl=label_s,abstract_s,docid,keyword_s,authEmailDomain_s,deptStructCountry_s" %(Auteur, start)
    reponse = requests.get(UrlHal+req)
    data = None
    if reponse.status_code == 200:
        data = reponse.json()
        if "response" in data.keys():
            charset = ( reponse.headers["Content-Type"]
                                .split("; ")[1]
                                .split("=" )[1]
                      )
            
            data = data['response']#dict_keys(['numFound', 'start', 'docs'])
            if data['numFound']>30 and nbColl<data['numFound']:
                start+=30
                nbColl+=len(data['docs'])
                data['docs'].extend(CollecteHal(Auteur, start=start, nbColl= nbColl))
                
            else:
                return data #return (json.loads(reponse.content.decode(charset)))
    else:
        raise ValueError(reponse.status_code, reponse.reason)
    return data

corpus1 = dict()
corpus1['name'] = 'HAL (english) [API]' #conforme aux déclarations de constants.py
corpus1['fileName'] = 'Hal'#Adapter à la requete
corpus1['ressources'] = get_resource_by_name(corpus1['name'] )
Aut='"David Reymond"'
#corpus1['path'] = newCorpus(project, source="hal", name="test", 
HalDocs =  CollecteHal(Aut, start=0, nbColl=0)


print()
#authFirstName_s
#authLastName_s
##authMiddleName_s
##authFullName_s
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
## =============================================================================
## #Corpus PubMed
## =============================================================================
##corpus4 = dict()
##corpus4['name'] = 'Pubmed [XML]'
##corpus4['fileName'] = 'Pubmed' #Adapter à la requete
##corpus4['ressources'] = get_resource_by_name(corpus4['name'] )
##corpus4['path'] = newCorpus(project, source="pubmed", name="test", query="calibrate cardiovascular metabolism")
##
##
###Tout pareil
##with open ('test'+corpus4['fileName']+'.pkl', 'wb') as fic:
##    pickle.dump(corpus4, fic)
##
###with open ('test'+corpus4['fileName']+'.pkl', 'rb') as fic:
###    corpus4 = pickle.load(fic)
##
##parse2(corpus4)
