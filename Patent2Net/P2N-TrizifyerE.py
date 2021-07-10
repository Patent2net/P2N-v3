# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on Fri Aug  9 14:01:22 2019

@author: cherrabi
"""

import nltk
from sematch.semantic.similarity import WordNetSimilarity
import sys
import pandas as pd
#import re 
#import umap
#import seaborn as sns
#from nltk.corpus import stopwords
#from sklearn.feature_extraction.text import TfidfVectorizer
import os
import re
from nltk.corpus import stopwords
from P2N_Lib import LoadBiblioFile
from P2N_Lib import GenereListeFichiers
from P2N_Config import LoadConfig
from nltk.corpus import wordnet 
import spacy
from itertools import product

ListeBrevet = [] # The patent List
stop_words = set(stopwords.words('english'))

configFile = LoadConfig()
requete = configFile.requete
BiblioPath = configFile.ResultBiblioPath
GatherContent = configFile.GatherContent
GatherBiblio = configFile.GatherBiblio
GatherPatent = configFile.GatherPatent
GatherFamilly = configFile.GatherFamilly
IsEnableScript = configFile.GatherIramuteq

ResultBiblioPath = configFile.ResultBiblioPath
ndf = configFile.ndf
DataBrevet = LoadBiblioFile(BiblioPath, ndf)
InventorList = []
InventorList = DataBrevet['brevets']

# preparing parsing data for indicator scientific publication and inventive production
inventor_list = [auth['inventor'] for auth in DataBrevet['brevets']]
label_list = [auth['label'] for auth in DataBrevet['brevets']]
title_list = [auth['title'] for auth in DataBrevet['brevets']]

dict = { 'label' : label_list, 'title' : title_list, 'inventor' : inventor_list }
df = pd.DataFrame(dict) 
df.to_csv("data_inventor.csv", header=False, index=False)

temporPath = configFile.temporPath
ResultAbstractPath = configFile.ResultAbstractPath
#ResultClaimsPath = configFile.ResultClaimsPath
#add here templateFlask directory local to the request directory normalize path for windows

ResultPathContent= configFile.ResultContentsPath.replace('\\', '/' )
ResultTemplateFlask = os.path.join(ResultPathContent,'Trizifiier').replace('\\','/')
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
if not os.path.exists(ResultTemplateFlask):    #creation des dossiers templates et dataFormat
    os.mkdir(ResultTemplateFlask)
if not os.path.exists(ResultTemplateFlask+'/templates'):    #creation des dossiers templates et dataFormat
    os.mkdir(ResultTemplateFlask+'/templates')
if not os.path.exists(ResultTemplateFlask+'/DataFormat'):    #creation des dossiers templates et dataFormat
    os.mkdir(ResultTemplateFlask+'/DataFormat')
#add here tempo dir
temporar = configFile.temporPath 
wns = WordNetSimilarity()
i=0
# build file list
#direct = os.path.normpath(ResultBiblioPath)
#direct = os.path.normpath(ResultClaimsPath)
direct = os.path.normpath(ResultAbstractPath)

# affiche url de chaque documents txt dans le dossier de la requete inseree , EN tous les url dossier pour en ect...
Fr, En, Unk = GenereListeFichiers(direct)

def convert_tag(tag):    
    tag_dict = {'N': 'n', 'J': 'a', 'R': 'r', 'V': 'v'}
    try:
        return tag_dict[tag[0]]
    except KeyError:
        return None


CountFile_R = 0
CountFile_W = 0
FichierOrg={}


# compter les nombre de caractere de EN
#if len(En)



PSW = [] # liste de mots vide à compléter au fur et à mesure des recherches
# minimalistic HTML for result file in html format


dataF = """""" # va contenir tous les abstracts du dossier de la requete
import codecs

#DejaVus = dict()


f=open(ResultTemplateFlask + '/DataFormat/FileDataAnalysisTrizWikiE.csv','w')

entetes = [
                 u'i',
                 u'label',
                 u'classe',
                 u'Action',
                 u'indiceSimAction',
                 u'abstract',
                 u'urlEspacenet'
              ]
ligneEntete=",".join(entetes)+"\n"  
f.write(ligneEntete)
    

d= pd.read_csv("Resources/trizOxfordData.csv",delimiter=";") 






dnew= pd.read_csv("FileTrizNewList.csv",delimiter=",") 
classes = pd.DataFrame(dnew,columns=['Ref_classe'])
classes_syn = pd.DataFrame(dnew,columns=['syn_classe'])
classesUnique = classes.drop_duplicates(keep = False)
expansionTriz = classes_syn.drop_duplicates(keep = False)
tal = spacy.load('en_core_web_sm')





#lecture des fichiers txt en boucle et placement element dans dataF
for fic in En:
    with codecs.open(fic, 'r', 'utf8') as File:       
        dataF = File.readlines() #single File ne pas lire la première ligne de l'abstract
#        dataF = '\n'.join(dataF) 
#        FichierOrg = dataF
        abstract = '\n'.join(dataF[1:])
        NumberBrevet= fic.split('-')[1]
        #NumberBrevet=NumberBrevet.replace('*Label_','')
        NumberBrevet=NumberBrevet.replace('.txt','')
        #sys.exit(0)
        
        # tokenization  
        
        abstract = re.sub("[^a-zA-Z#]", " ",str(abstract))

        brevet = tal(abstract)



        #Blob = TextBlob(abstract)
        #wordlist=Blob.words #should give best results@ DR

        # remove stop-words  and words less 3 caracters
     
        filtered_sentence = [mot.lemma_ for mot in brevet if mot.pos_ == "NOUN" or mot.pos_ == "VERB"]

              
        #for w in wordlist: 
            #if w not in stop_words and len(w) > 3: 
                #filtered_sentence.append(w) 
              
        
        
        
            #Document-Term Matrix
        #print(filtered_sentence)   
        #print(resultType)    
            
        urlEspacenet="https://worldwide.espacenet.com/searchResults?submitted=true&locale=fr_EP&DB=EPODOC&ST=advanced&TI=&AB=&PN="+format(NumberBrevet)
        matriceListe = []
        matricelistePaire = []
        matricelistePaireSort=[]
        matricelistePaireAction = []
        matricelistePaireObject = []

       
        
        for classe in expansionTriz.keys() :  
            ExpansionClasse  = expansionTriz[classe]
        
        allsyns1 = set(ss for word in ExpansionClasse for ss in wordnet.synsets(word))
        allsyns2 = set(ss for word in  filtered_sentence for ss in wordnet.synsets(word))
        best = max((wordnet.wup_similarity(s1, s2) or 0, s1, s2) for s1, s2 in product(allsyns1, allsyns2) if all([lem1 not in s2._lemma_names for lem1 in s1._lemma_names]) )
        #print("allsyns1 ========",allsyns1)
        #print("\n")
        #print("allsyns2========",allsyns2)
        
        print("best: ", best)
        print("\n")



sys.exit()          
      


            
       
f.close()

sys.exit()

#open file data semantic classification 

d= pd.read_csv(ResultTemplateFlask + "/DataFormat/FileDataAnalysisTrizWikiE.csv")

df = pd.DataFrame(d,columns=['i','label','Term','Action','indiceSimAction','abstract','urlEspacenet'])

df.to_csv(ResultTemplateFlask + '/DataFormat/tableauTriE.csv')

sys.exit(0)  # je veux le csv généré ici, car a partir de cette ligne je vais changer pour afficher les classes autrement 

# sorted data by id and term ascending 

dfmax = df.sort_values(by=['i','Term','indiceSimAction'],ascending=[True,True,False])
dfmax.to_csv(ResultTemplateFlask + '/DataFormat/tableauTri.csv')

# selected just top indice similiraty for term / action 

dresult = dfmax.drop_duplicates(['Term'],keep='first')
dresult.to_csv(ResultTemplateFlask + '/DataFormat/tableauDrop.csv')

dresultmaxI=dresult.sort_values(by='indiceSimAction')

# create file formated datas to use in tabulator html 

dresultmaxI.to_csv(ResultTemplateFlask + '/DataFormat/resultatParserV2.csv')
dd=pd.read_csv(ResultTemplateFlask + '/DataFormat/resultatParserV2.csv')
dff = pd.DataFrame(dd,columns=['i','label','Action','Term','Patent Tags','indiceSimAction','abstract','urlEspacenet'])
dfjson= pd.DataFrame(dd,columns=['label','Action','Term','Patent Tags','abstract','urlEspacenet'])
dfjson.to_json(ResultTemplateFlask +'/DataFormat/caraTrizWikisemantic.json', orient='records', lines=False)

#shutil.copyfile("templates/sources", ResultTemplateFlask+"/sources")
ResFolder = configFile.ResultPath.replace('\\', '//')
ResFolder = ResFolder.replace('//','/')
shutil.copy("templates/P2N-Trizifyer-semantic.html", ResFolder)

#add variable vars json_data datatable 

src = open(ResultTemplateFlask +'/DataFormat/caraTrizWikisemantic.json','r')
lineadd = " var json_data = "
online=src.readlines()
online.insert(0,lineadd)
src.close

src = open(ResultTemplateFlask +'/DataFormat/caraTrizWikisemantic.json','w')
src.writelines(online)
src.close







        
    


    
       
 
        

