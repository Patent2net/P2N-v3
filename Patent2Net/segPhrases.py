from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from matplotlib import pyplot
import os
import re
import logging
import time
from operator import add
from textblob import TextBlob # importation de textblob outil liguistique 
from nltk.corpus import stopwords
from Patent2Net.P2N_Lib import LoadBiblioFile
from Patent2Net.P2N_Config import LoadConfig
configFile = LoadConfig()

requete = configFile.requete
projectName = configFile.ndf
phrase="invention relates to food industry, namely to production of granular caviar from hydrobionts, which has a high biological activity. Method for obtaining edible granular caviar from Artemia's gonad cancer includes cleaning the cysts by decapsulating them, drying the purified kernels of Artemia caviar to a residual moisture content of not more than 5-10 % by weight, at which the layers of the product are formed in polymer bags and processed by a stream of accelerated electrons obtained in a pulsed linear electron accelerator with an accelerated electron energy of 2.5-5 MeV and an absorbed radiation dose of not more than 20 kGy. Prior to formation of food product layers in polymer bags for irradiation with accelerated electrons, organoleptic and/or preservative additives are additionally added thereto at the following quantitative content of the components, % by weight: organoleptic and/or preservative additives 3.0-30.0; decapsulated cysts of Artemia crustaceans - the rest is up to 100 %.EFFECT: proposed method of obtaining food caviar provides for the expansion of the raw material base for the production of granular caviar, as well as production of granular caviar with new higher nutritional, biologically active and organoleptic properties.1 cl, 1 tbl, 10 ex"




phraseBlob = TextBlob(phrase)
sentences=phraseBlob.words

model = Word2Vec(sentences, min_count=1)
# summarize the loaded model
print(model)
# summarize vocabulary
words = list(model.wv.vocab)
print(words)
# access vector for one word
ndf = projectName
BiblioPath = configFile.ResultBiblioPath
ResultBiblioPath = configFile.ResultBiblioPath
temporPath = configFile.temporPath
ResultPathContent= configFile.ResultContentsPath
ResultAbstractPath = configFile.ResultAbstractPath
RepDir = configFile.ResultPath + '/NezhaWork'

if 'Description'+ndf in os.listdir(BiblioPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
    print( "loading patent biblio data with")
    DataBrevet = LoadBiblioFile(BiblioPath, ndf)
    print("Hi this is Scholar processor. Bibliographic data of ", ndf, " patent universe found.")
corpus = []
for brevet in DataBrevet["brevets"]:
    for abstract in brevet['abstract'] :
        corpus.append(abstract)
        
#        
#corpus = [
#          'Text of the first document.',
#          'Text of the second document made longer.',
#          'Number three.',
#          'This is number four.',
#]
# we need to pass splitted sentences to the model
tokenized_sentences = [sentence.split() for sentence in corpus]

print(model)