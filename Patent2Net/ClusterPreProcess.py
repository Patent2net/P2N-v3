# -*- coding: utf-8 -*-
"""
Created on Wed May 31 08:00:26 2017

Only to build the ngramm distribution frequencies
@author: dreymond
"""
from __future__ import print_function

import numpy as np
import pandas as pd
import nltk
import os
import codecs
from sklearn import feature_extraction
import mpld3
from P2N_Lib import LoadBiblioFile
from P2N_Config import LoadConfig
import sys, os
from nltk.stem.snowball import SnowballStemmer
import codecs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from sklearn.metrics.pairwise import pairwise_distances
from pandas.plotting import scatter_matrix
import os  # for os.path.basename
import pickle
import matplotlib.pyplot as plt
import matplotlib as mp
from sklearn.manifold import MDS
from sklearn.metrics.pairwise import cosine_similarity
from collections import OrderedDict
from TAL_P2N_Lib import tokenize_only 
stopwords = nltk.corpus.stopwords.words('english')
cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e', 5: '#ff6a61',6: '#00ff1e', 7: '#0001FF'}
#brev_stpswrds = ['production', 'method', 'preparation', 'preparing', 'use', \
 #                'effective', "provide", "containing", "extract", "invention", "materials", 'relates', \
 #                'discloses', "comprising"]
colors = ['#FF0000', '#00FF00', 'cyan', '#DDDD00', '#DD00DD', '#00DDDD', '#999999', '#FFFFFF']
markers = ['.', 'x', '^', 's','p', 'h', 'd', '+', 'o']

Tit = True

stemmer = SnowballStemmer("english")

configFile = LoadConfig()
requete = configFile.requete
ndf = configFile.ndf

ResultPath = configFile.ResultPath
temporPath = configFile.temporPath
ResultContentsPath = configFile.ResultContentsPath
ResultBiblioPath = configFile.ResultBiblioPath
# at final step, next line should enter configFile as above
ResultPathContentAug ='..//DATA//'+ndf+'//PatentContents//Metrics'
if "Metrics" not in os.listdir('..//DATA//'+ndf+'//PatentContents//'):
    os.makedirs(ResultPathContentAug)

if 'Excluding-voc.txt' not in os.listdir(ResultPath):
	with open (ResultPath +'//Excluding-voc.txt', 'w') as fic:
		fic.write('\n')
else: 
	with open (ResultPath +'//Excluding-voc.txt', 'r') as fic:
		data = fic.read()
		brev_stpswrds  = data.split(',')
		stopwords.extend(brev_stpswrds)
    

EnsVoc = dict()
Labelle  = OrderedDict()

if 'Description'+ndf or 'Description'+ndf.lower() in os.listdir(ResultBiblioPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
    ficBrevet = LoadBiblioFile(ResultBiblioPath, ndf)
else: #Retrocompatibility
    print ('gather your data again. sorry')
    sys.exit()

if ficBrevet.has_key('brevets'):
    lstBrevet = ficBrevet['brevets']
#        if data.has_key('requete'):
#            DataBrevet['requete'] = data["requete"]
    print ("Found  datafile with " +str(len(lstBrevet)) + " patents!")
else:
    print ('gather your data again')
    sys.exit()

cles =  ['IPCR11', 'CitO', 'dateDate', 'inventor-nice', 'equivalents', 'CitedBy', 'representative', 'Inventor-Country', 'date', 'inventor', 'kind', 'priority-active-indicator', 'applicant-nice', 'IPCR1', 'country', 'IPCR3', 'applicant', 'IPCR4', 'IPCR7', 'title', 'application-ref']
Titles = []
Labels = []

Abstracts  = [] # Pure abstracts
IPCRsText  = []

Contents = []   # Contains IPCRs (text of associated IPCR classes) + title + abstracts 
Tit2FicName = dict()

CIB = []

print("loading patents contents")
lstfic = os.listdir(ResultPathContentAug)
for bre in lstBrevet:
    FicName = 'en-'+ bre['label']+"AugCIB.txt" 
    AbsName = 'en-'+ bre['label']+".txt" 
    CibName = 'en-'+ bre['label']+"Desc.txt" 
    if FicName in lstfic:
        try: 
            toto = bre['title'].encode('ascii')
            with codecs.open(ResultContentsPath +'//CibDesc//'+CibName, 'r', encoding='ascii', errors="ignore") as fic:
                tempo = fic.readlines()
            IPCRsTexte= ' '.join([lig for lig in tempo if "***" not in lig])
            IPCRsTexte.encode('ascii')
            
#            with codecs.open(ResultPathContentAug+'//'+FicName, 'r', encoding='ascii', errors="ignore") as fic:
#                tempo = fic.readlines()
#                
##                tempo2=' '.join(tempo)
##                tempo2.encode('ascii')
#                abstract= ' '.join([lig for lig in tempo if "***" not in lig])
#                abstract.encode('ascii')
#                
                
                
            with codecs.open(ResultContentsPath +'//Abstract//'+AbsName, 'r', encoding='ascii', errors="ignore") as fic:
                tempo = fic.readlines()
            PureAbstract= '\n'.join([lig for lig in tempo if "***" not in lig])
            PureAbstract.encode('ascii')
            
            with codecs.open(ResultPathContentAug+'//'+FicName, 'w', encoding='ascii', errors="ignore") as fic:
                 tempo = fic.write(IPCRsTexte+' \n'+ toto.lower()+' \n'+ PureAbstract +' \n')
            Abstracts.append(PureAbstract)
            IPCRsText.append(IPCRsTexte)
            Contents.append(IPCRsTexte+' \n'+ toto.lower()+' \n'+ PureAbstract +' \n')
             #should explode on chinese titles
            Titles.append(toto.lower())
            Labels.append(bre['label'])    
            Tit2FicName[toto.lower()] = FicName
        except:
            pass # no file OR bad coding
        
        
print (str(len(Titles)) + ' title and ')
print (str(len(Abstracts)) + ' abstracts loaded')
print (str(len(IPCRsText)) + ' IPC texts loaded')

TitlesTok =[]
AbstractsTok =[]
ClassTextTok =[]
ContentsTok = []

joblib.dump(Tit2FicName, ResultContentsPath+'//Titles_ficNames-'+ndf+'.pkl')
joblib.dump(Contents, ResultContentsPath+'//Contents-'+ndf+'.pkl')
joblib.dump(Titles, ResultContentsPath+'//Titles-'+ndf+'.pkl')
joblib.dump(Labels, ResultContentsPath+'//Labels-'+ndf+'.pkl')
joblib.dump(Abstracts, ResultContentsPath+'//Abstracts-'+ndf+'.pkl')
joblib.dump(IPCRsText, ResultContentsPath+'//IPCRsText-'+ndf+'.pkl')

print (str(len(Contents)) + ' abstracts augmented with IPC and titles loaded')



for i in Titles:
    TitlesTok.extend(tokenize_only(i))
for i in Abstracts:
    AbstractsTok.extend(tokenize_only(i))
for i in IPCRsText:
    ClassTextTok.extend(tokenize_only(i))
for i in Contents:
    ContentsTok.extend(tokenize_only(i))


print ("mots des titres ->" + str(len(TitlesTok)))
print ("mots des résumés ->" + str(len(AbstractsTok)))
print ("mots des IPC ->" + str(len(ClassTextTok)))
print ("mots des totaux ->" + str(len(TitlesTok)+len(AbstractsTok)+len(ClassTextTok)))
print ("mots des totaux uniques ->" + str(len(set(TitlesTok+AbstractsTok+ClassTextTok))))
print ("mots des totaux (autre ensemble test)->"+ str(len(ContentsTok)))    # should be the same as previous
print ("mots des totaux uniques (autre ensemble test)->" +str(len(set(ContentsTok))))
print ("Diff (test et ense ref should be 0 !!!)" + str(len(set(TitlesTok+AbstractsTok+ClassTextTok)-set(ContentsTok))))
params={  'ls' : '-.',
            #'drawstyle' : 'steps',
            #'basex':10, 
            'color': 'black', 
            'lw': 1
            }     
Labelle[0] = "Res"# only
#EnsVoc[0] = [FreqTrie[term] for term in EnsVoc[0] if term in ResumesGrammed]
Labelle[1] = "Tit"
Labelle[2] = "IPC & Res"
Labelle[3] = "IPC"
Labelle[4] = "Tit & Res"
Labelle[5] = "Tit & IPC"
Labelle[6] = "$\cap All$"   
Labelle[7] = "Border"  

count_vectorized=CountVectorizer( stop_words=stopwords, ngram_range=(1,4), tokenizer=tokenize_only)


Titles_freq_vector = count_vectorized.fit_transform(Titles)
TitlesGrammed = count_vectorized.get_feature_names()
Abstracts_freq_vector = count_vectorized.fit_transform(Abstracts)
AbstractsGrammed = count_vectorized.get_feature_names()
ClassText_freq_vector = count_vectorized.fit_transform(IPCRsText) #may be a biais here du to gatherer and epo data
ClassTextGramed = count_vectorized.get_feature_names()
    
Contents_freq_vector = count_vectorized.fit_transform(Contents)
ContentsGrammed = count_vectorized.get_feature_names()
joblib.dump(Titles_freq_vector, ResultContentsPath+'//Titles_freq_vector'+ndf+'.pkl')
joblib.dump(Abstracts_freq_vector, ResultContentsPath+'//Abstracts_freq_vector'+ndf+'.pkl')
joblib.dump(ClassText_freq_vector, ResultContentsPath+'//ClassText_freq_vector'+ndf+'.pkl')
joblib.dump(Contents_freq_vector, ResultContentsPath+'//Contents_freq_vector'+ndf+'.pkl')

word_freq_df = pd.DataFrame({'term': count_vectorized.get_feature_names(), 'occurrences':np.asarray(Contents_freq_vector.sum(axis=0)).ravel().tolist()})
word_freq_df['frequency'] = word_freq_df['occurrences']/np.sum(word_freq_df['occurrences'])
    #plt.legend('n_grams = '+str(i))
FreqTrie = word_freq_df.sort_values('occurrences',ascending = False)#OrderedDict(sorted(FreqTrie.items(), key = lambda x: x[1], reverse = True))    

joblib.dump(word_freq_df , ResultContentsPath+'//word_freq'+ndf+'.pkl')
joblib.dump(FreqTrie , ResultContentsPath+'//FreqTrie'+ndf+'.pkl')

ClassTextGramed = set(ClassTextGramed)
TitlesGrammed =set(TitlesGrammed)
AbstractsGrammed = set(AbstractsGrammed)
CTGTG = ClassTextGramed | TitlesGrammed
CTGAG = ClassTextGramed | AbstractsGrammed
TGGAG = TitlesGrammed | AbstractsGrammed
ALL =  ClassTextGramed | TitlesGrammed | AbstractsGrammed
cpt=0


   
Voc = dict() #• check process
for i in Labelle.keys():
    Voc[Labelle[i]]=[]
for i in range(8):
    EnsVoc[i] = []
    
cpt=0
ClassTextGramed = set(ClassTextGramed)
TitlesGrammed =set(TitlesGrammed)
AbstractsGrammed = set(AbstractsGrammed)
ContentsGrammed = set(ContentsGrammed)
CTGTG = ClassTextGramed | TitlesGrammed #union
CTGAG = ClassTextGramed | AbstractsGrammed
TGGAG = TitlesGrammed | AbstractsGrammed
ALL =  ClassTextGramed | TitlesGrammed | AbstractsGrammed
    #(\"" + word + "\" is rank " + str(word_rank) + ")")
    #texte='n_grams='+str(i-1)
   
Voc = dict() #• check process
for i in Labelle.keys():
    Voc[Labelle[i]]=[]
for i in range(8):
    EnsVoc[i] = []
#fig,ax = plt.subplots(2)
#fig.add_axes()
joblib.dump(ClassTextGramed, ResultContentsPath+'//ClassFile'+ndf+'.pkl')
joblib.dump(TitlesGrammed, ResultContentsPath+'//TitlesFile'+ndf+'.pkl')
joblib.dump(AbstractsGrammed, ResultContentsPath+'//Abstracts'+ndf+'.pkl')
joblib.dump(ContentsGrammed, ResultContentsPath+'//ContentsFile'+ndf+'.pkl')
AbstractsGrammedNOTCTGTG =  AbstractsGrammed - CTGTG
ClassTextGrammedNOTTGGAG = ClassTextGramed - TGGAG
TitlesGrammedNOTCTGAG = TitlesGrammed - CTGAG
CAT =(ClassTextGramed & AbstractsGrammed)- TitlesGrammed
TAC =(TitlesGrammed & AbstractsGrammed)- ClassTextGramed 
TCA= (TitlesGrammed & ClassTextGramed)-AbstractsGrammed
CTA = ClassTextGramed & TitlesGrammed & AbstractsGrammed
InterAll = ContentsGrammed-ALL
for entr in  FreqTrie.values:
    if entr[1] in AbstractsGrammedNOTCTGTG:# abstract only
        EnsVoc[0].append((entr[0], cpt, entr[2]))
        Voc['Res'].append(entr[1]) 
    elif entr[1] in ClassTextGrammedNOTTGGAG :# IPC only
        EnsVoc[3].append((entr[0], cpt, entr[2]))
        Voc['IPC'].append(entr[1]) 
    elif entr[1] in  TitlesGrammedNOTCTGAG :# Titles only
        EnsVoc[1].append((entr[0], cpt, entr[2]))
        Voc['Tit'].append(entr[1]) 
    elif entr[1] in  CAT:# IPC and Abstract
        EnsVoc[2].append((entr[0], cpt, entr[2]))
        Voc["IPC & Res"].append(entr[1]) 
    elif entr[1] in  TAC :# Title and Abstract
        EnsVoc[4].append((entr[0], cpt, entr[2]))
        Voc["Tit & Res"].append(entr[1]) 
    elif entr[1] in  TCA: # IPC, Title
        EnsVoc[5].append((entr[0], cpt, entr[2]))
        Voc["Tit & IPC"].append(entr[1]) 
    elif entr[1] in CTA:
        EnsVoc[6].append((entr[0], cpt, entr[2]))
        Voc['$\cap All$'].append(entr[1]) 
    elif entr[1] in InterAll:
        EnsVoc[7].append((entr[0], cpt, entr[2]))
        Voc['Border'].append(entr[1])
    else:
        print ('lost in translation ', entr[0], cpt)
    cpt +=1

for indi in range(len(EnsVoc)):
    print ("taille de ", Labelle[indi],':', len(EnsVoc[indi]), "Uniques :", len(set(EnsVoc[indi])))
        


joblib.dump(EnsVoc, ResultContentsPath+'//EnsVocFile'+ndf+'.pkl')
joblib.dump(Voc, ResultContentsPath+'//VocFile'+ndf+'.pkl')

print("ready for P2N-Cluster")
   






##define vectorizer parameters
#tfidf_vectorizer = TfidfVectorizer(max_df=0.9, max_features=500000,
#                                 min_df=0.0, stop_words=stopwords,#'english',
#                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,5))
#
#
#tfidf_vectorizer2 = TfidfVectorizer(max_df=0.9, max_features=500000,
#                                 min_df=0.0, stop_words=stopwords,#'english',
#                                 use_idf=False, tokenizer=tokenize_and_stem, ngram_range=(1,5))

#
#tfidf_matrix = tfidf_vectorizer.fit_transform(Abstracts) #fit the vectorizer to synopses
#tfidf_matrix2 = tfidf_vectorizer2.fit_transform(Abstracts)
#print(tfidf_matrix.shape)
#print(tfidf_matrix2.shape)
#
#terms = tfidf_vectorizer.get_feature_names()
#
#
#dist = 1 - cosine_similarity(tfidf_matrix)
#dist2 = 1 - cosine_similarity(tfidf_matrix2)
#
#print()
#
#
##tfidf_matrix.indices # index of words
##tfidf_matrix.getcol(indice).toarray() # array of frequencies of word N° indice in documents
#
#num_clusters = 8
#
#km = KMeans(n_clusters=num_clusters)
#
#km.fit(tfidf_matrix)
#
#
#clusters = km.labels_.tolist()
#
#
#Clust_Distances = dict() # distances for each vector to its centroîd
#Diam_Clust = dict()     # diameter of clusters
#for ind in range(len(tfidf_matrix.toarray())):
#    Clust_Distances [clusters[ind]] = []
#for ind in range(len(tfidf_matrix.toarray())):
#    Clust_Distances [clusters[ind]].append(np.linalg.norm(tfidf_matrix[ind]- km.cluster_centers_[clusters[ind]]))
#    #scipy.spatial.distance.euclidean(tfidf_matrix[ind], km.cluster_centers_[clusters[ind]])
#for ind in range(num_clusters):
#    Diam_Clust [ind] = max(Clust_Distances [ind])
#    print (" diamètre cluster ", ind, " --> ", Diam_Clust [ind])
#    print (" diantce moyenne interne "," --> ", np.mean (Clust_Distances [ind]))
#
#for ind in range(num_clusters):
#    for ind2 in range(num_clusters):
#        Dmin = np.linalg.norm(km.cluster_centers_[clusters[ind]]- km.cluster_centers_[clusters[ind2]])
#
##DiffClust = np.linalg.norm(km.cluster_centers_- km.cluster_centers_[clusters[ind2]])    
#
##p.linalg.norm(km.cluster_centers_[clusters[ind]]- km.cluster_centers_[clusters[ind2]])
#DiffClust = pairwise_distances(  km.cluster_centers_, Y=None, metric='euclidean', n_jobs=1)
#data = pd.DataFrame( DiffClust, index = range(8))
#scatter_matrix( data, alpha=0.2, figsize=(20, 20), diagonal='kde')#, c=data.apply(lambda x:cluster_colors[x]))
#plt.plot()
#plt.show()
#uncomment the below to save your model 
#since I've already run my model I am loading from the pickle

#joblib.dump(km,  'doc_cluster.pkl')
#
##km = joblib.load('doc_cluster.pkl')
#clusters = km.labels_.tolist()
#
#Brevets = { 'title': Titles, 'labels': Labels, 'abstracts': Abstracts, 'cluster': clusters, 'CIB': CIB }
#
#
#frame = pd.DataFrame(Brevets, index = [clusters] , columns = ['labels', 'title', 'cluster', 'CIB'])
#frame['cluster'].value_counts() #number of patents per cluster (clusters from 0 to 4)
##grouped = frame['CIB'].groupby(frame['cluster']) #groupby cluster for aggregation purposes
#
##grouped.mean() #average rank (1 to 100) per cluster
#
#
#
#
#print("Top terms per cluster:")
#print()
##sort cluster centers by proximity to centroid
#order_centroids = km.cluster_centers_.argsort()[:, ::-1] 
#
##set up colors per clusters using a dict
#
#cluster_names = dict()
##set up cluster names using a dict
#for i in range(num_clusters):
#    cluster_names [i] =[]
#    for ind in order_centroids[i, :10]: 
#        word=vocab_frame.loc[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore')
#        if word not in stopwords:
#            cluster_names [i].append(word )
#    cluster_names [i] = set(cluster_names [i])
#    cluster_names [i] = ','.join(cluster_names [i])
#for i in range(num_clusters):
#    print("Cluster %d words:" % i, end='')
#    
#    for ind in order_centroids[i, :6]: #replace 6 with n words per cluster
#        print(' %s' % vocab_frame.loc[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
#    print() #add whitespace
#    print() #add whitespace
#    
#    print("Cluster %d titles:" % i, end='')
#    for title in frame.loc[i]['title'].values.tolist():
#        print(' %s,' % title.encode('utf-8', 'ignore'), end=',')
#    print() #add whitespace
#    print() #add whitespace
#    
#print()
#print()
#
#MDS()
#
## convert two components as we're plotting points in a two-dimensional plane
## "precomputed" because we provide a distance matrix
## we will also specify `random_state` so the plot is reproducible.
#mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
#
#pos = mds.fit_transform(dist)  # shape (n_components, n_samples)
#
#xs, ys = pos[:, 0], pos[:, 1]
#print()
##%matplotlib inline 
#
##create data frame that has the result of the MDS plus the cluster numbers and titles
#df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=Titles)) 
#
##group by cluster
#groups = df.groupby(clusters)
#
#
#
#
#    
#print (cluster_names)
#
## set up plot
#fig, ax = plt.subplots(figsize=(20, 9)) # set size
#ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
#
##iterate through groups to layer the plot
##note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
#for name, group in groups:
#    ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, 
#            label=cluster_names[name], color=cluster_colors[name], 
#            mec='none')
#    ax.set_aspect('auto')
#    ax.tick_params(\
#        axis= 'x',          # changes apply to the x-axis
#        which='both',      # both major and minor ticks are affected
#        bottom='off',      # ticks along the bottom edge are off
#        top='off',         # ticks along the top edge are off
#        labelbottom='off')
#    ax.tick_params(\
#        axis= 'y',         # changes apply to the y-axis
#        which='both',      # both major and minor ticks are affected
#        left='off',      # ticks along the bottom edge are off
#        top='off',         # ticks along the top edge are off
#        labelleft='off')
    
#ax.legend(numpoints=3)  #show legend with only 1 point
#
##add label in x,y position with the label as the film title
#for i in range(len(df)):
#    ax.text(df.loc[i]['x'], df.loc[i]['y'], df.loc[i]['label'], size=6)  
#
#    
#    
#plt.show() #show the plot
#plt.close()
#
#
##define custom toolbar location
#class TopToolbar(mpld3.plugins.PluginBase):
#    """Plugin for moving toolbar to top of figure"""
#
#    JAVASCRIPT = """
#    mpld3.register_plugin("toptoolbar", TopToolbar);
#    TopToolbar.prototype = Object.create(mpld3.Plugin.prototype);
#    TopToolbar.prototype.constructor = TopToolbar;
#    function TopToolbar(fig, props){
#        mpld3.Plugin.call(this, fig, props);
#    };
#
#    TopToolbar.prototype.draw = function(){
#      // the toolbar svg doesn't exist
#      // yet, so first draw it
#      this.fig.toolbar.draw();
#
#      // then change the y position to be
#      // at the top of the figure
#      this.fig.toolbar.toolbar.attr("x", 250);
#      this.fig.toolbar.toolbar.attr("y", 400);
#
#      // then remove the draw function,
#      // so that it is not called again
#      this.fig.toolbar.draw = function() {}
#    }
#    """
#    def __init__(self):
#        self.dict_ = {"type": "toptoolbar"}
#
##create data frame that has the result of the MDS plus the cluster numbers and titles
#df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=Titles)) 
#
##group by cluster
#groups = df.groupby(clusters)
#
##define custom css to format the font and to remove the axis labeling
#css = """
#text.mpld3-text, div.mpld3-tooltip {
#  font-family:Arial, Helvetica, sans-serif;
#}
#
#g.mpld3-xaxis, g.mpld3-yaxis {
#display: none; }
#
#svg.mpld3-figure {
#margin-left: -200px;}
#"""
#
## Plot 
#fig, ax = plt.subplots(figsize=(22,12)) #set plot size
#ax.margins(0.03) # Optional, just adds 5% padding to the autoscaling
#
##iterate through groups to layer the plot
##note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
#for name, group in groups:
#    points = ax.plot(group.x, group.y, marker='o', linestyle='', ms=18, 
#                     label=cluster_names[name], mec='none', 
#                     color=cluster_colors[name])
#    ax.set_aspect('auto')
#    labels = [i for i in group.title]
#    
#    #set tooltip using points, labels and the already defined 'css'
#    tooltip = mpld3.plugins.PointHTMLTooltip(points[0], labels,
#                                       voffset=10, hoffset=10, css=css)
#    #connect tooltip to fig
#    mpld3.plugins.connect(fig, tooltip, TopToolbar())    
#    
#    #set tick marks as blank
#    ax.axes.get_xaxis().set_ticks([])
#    ax.axes.get_yaxis().set_ticks([])
#    
#    #set axis as blank
#    ax.axes.get_xaxis().set_visible(False)
#    ax.axes.get_yaxis().set_visible(False)
#
#    
#ax.legend(numpoints=1) #show legend with only one dot
#
#mpld3.display() #show the plot
#
#from pandas.plotting import scatter_matrix
#ptl = scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')
##ptl.show()
#
##uncomment the below to export to html
#html = mpld3.fig_to_html(fig)
#
#with open(ResultPathContentAug+"//test.html", "w") as fic:
#    fic.write(html)