# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Created on Fri Aug  9 14:01:22 2019

@author: cherrabi
"""


from P2N_Lib import GenereListeFichiers # import 
from P2N_Config import LoadConfig #
import os # importation de la bibliothèque os qui sert à 
from textblob import TextBlob # importation de textblob outil liguistique 
from nltk.corpus import stopwords
import nltk
from sematch.semantic.similarity import WordNetSimilarity
from nltk.corpus import wordnet as wn
import pandas as pd
import re
import shutil  
import sys
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
import re 
import umap
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
from gensim.corpora import Dictionary
from sklearn.decomposition import TruncatedSVD
import os
import re
import codecs 
import logging
import time
from operator import add
from P2N_Lib import LoadBiblioFile
from P2N_Lib import GenereListeFichiers
from P2N_Config import LoadConfig

ListeBrevet = [] # The patent List
stop_words = set(stopwords.words('english'))

configFile = LoadConfig()
requete = configFile.requete
GatherContent = configFile.GatherContent
GatherBiblio = configFile.GatherBiblio
GatherPatent = configFile.GatherPatent
GatherFamilly = configFile.GatherFamilly
IsEnableScript = configFile.GatherIramuteq

ResultBiblioPath = configFile.ResultBiblioPath
ndf = configFile.ndf
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

DejaVus = dict()


f=open(ResultTemplateFlask + '/DataFormat/FileDataAnalysisTrizWiki.csv','w')

entetes = [
                 u'i',
                 u'Abstract Number',
                 u'Term',
                 u'Action',
                 u'indiceSimAction',
                 u'abstract',
                 u'urlEspacenet'
              ]
ligneEntete=",".join(entetes)+"\n"  
f.write(ligneEntete)
    

d= pd.read_csv("trizOxfordData.csv",delimiter=";") 

listcaras = pd.DataFrame(d,columns=['Colonne3'])
listcara = listcaras.drop_duplicates(['Colonne3'],keep='first')


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
        Blob = TextBlob(abstract)
        wordlist=Blob.words #should give best results@ DR

        # remove stop-words  and words less 3 caracters
     
        filtered_sentence = [] 
              
        for w in wordlist: 
            if w not in stop_words and len(w) > 3: 
                filtered_sentence.append(w) 
              
        
        
         
        # calcul term frequency in abstract ( fix to 5 terms )
            
            
        frequency = {}
        
        for word in filtered_sentence:
            count = frequency.get(word,0)
            frequency[word] = count + 1
             
        frequency_list = frequency.keys()
         
        sorted_term_frequency = []
        
        for words in frequency_list:
            #print (words, frequency[words])
            sorted_term_frequency.append((words, frequency[words]))
            
            
        sorted_terms = sorted(sorted_term_frequency, key= lambda x:x[1], reverse=True)[:5]
        print(sorted_terms)
        sorted_terms_list = []
        for t in sorted_terms:
            sorted_terms_list.append (t[0])
            
        
        
        sorted_terms_lists=sorted_terms_list
       
        urlEspacenet="https://worldwide.espacenet.com/searchResults?submitted=true&locale=fr_EP&DB=EPODOC&ST=advanced&TI=&AB=&PN="+format(NumberBrevet)
        matriceListe = []
        matricelistePaire = []
        matricelistePaireSort=[]
        matricelistePaireAction = []
        matricelistePaireObject = []

       
        
        for word in sorted_terms_lists :  
           tokens = word 
           for index, row in listcara.iterrows():
                abstractNumber='abs'.format(str((i)))
                listaction = row['Colonne3']
                listaction = re.sub(r'\([^)]*\)', '', listaction)
           
               #comparaison betwen tags and classe Triz
               
                indiceSimAction = wns.word_similarity(word,str(listaction))
                
                   
                if indiceSimAction == 0 or word.isdigit() == True:
                        #print "rien a faire "
                       continue 
        
                else:
                    valeurs=[]
                        
                    valeurs=[i,NumberBrevet,word,listaction,indiceSimAction,abstract,urlEspacenet]
                        
                    ligne=",".join(str(v) for v in valeurs) + "\n"
                      
                    f.write(ligne)    


    
    i=i+1   
     
    print((NumberBrevet), " abstracts processed" )              


            
       
f.close()

#open file data semantic classification 

d= pd.read_csv(ResultTemplateFlask + "/DataFormat/FileDataAnalysisTrizWiki.csv")

df = pd.DataFrame(d,columns=['i','Abstract Number','Term','Action','indiceSimAction','abstract','urlEspacenet'])

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
dff = pd.DataFrame(dd,columns=['i','Abstract Number','Action','Term','indiceSimAction','abstract','urlEspacenet'])
dfjson= pd.DataFrame(dd,columns=['Abstract Number','Action','Term','abstract','urlEspacenet'])
dfjson.to_json(ResultTemplateFlask +'/DataFormat/caraTrizWikisyntax.json', orient='records', lines=False)

#shutil.copyfile("templates/sources", ResultTemplateFlask+"/sources")
ResFolder = configFile.ResultPath.replace('\\', '//')
ResFolder = ResFolder.replace('//','/')
shutil.copy("templates/P2N-Trizifyer-syntax.html", ResFolder)

#add variable vars json_data datatable 

src = open(ResultTemplateFlask +'/DataFormat/caraTrizWikisyntax.json','r')
lineadd = " var json_data = "
online=src.readlines()
online.insert(0,lineadd)
src.close

src = open(ResultTemplateFlask +'/DataFormat/caraTrizWikisyntax.json','w')
src.writelines(online)
src.close







        
    


    
       
 
        

