# -*- coding: utf-8 -*-
"""
Created on Sat Jul 08 16:24:35 2017

@author: dreymond
"""


from __future__ import print_function

import os
import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import MDS
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords as nltkSW
from TAL_P2N_Lib import tokenize_only, tokenize_and_stem
from P2N_Lib import LoadBiblioFile
from P2N_Config import LoadConfig

from collections import OrderedDict

import matplotlib
import matplotlib.pyplot as plt

import mpld3
import numpy as np
import logging
from sklearn.externals import joblib
from optparse import OptionParser


num_clusters = 9 
a = np.linspace(0, 1, num_clusters)
def get_colors(inp, colormap, vmin=None, vmax=None):
    norm = plt.Normalize(vmin, vmax)
    return colormap(norm(inp))
colors = get_colors(a, plt.cm.autumn)
colors2 = get_colors(a, plt.cm.winter)



cluster_colors=dict()
cluster_colors2=dict()
stopwords = nltkSW.words('english')
for aaa in range(len(colors)):
    cluster_colors[aaa] =colors[aaa]
    cluster_colors2[aaa] =colors2[aaa]
#cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e', 5: '#ff6a61',6: '#00ff1e', 7: '#0001FF'}
#brev_stpswrds = ['production', 'method', 'preparation', 'preparing', 'use', \
 #                'effective', "provide", "containing", "extract", "invention", "materials", 'relates', \
 #                'discloses', "comprising"]
#colors = ['#FF0000', '#00FF00', 'cyan', '#DDDD00', '#DD00DD', '#00DDDD', '#999999', '#FFFFFF']
markers = ['.', 'x', '^', 's','p', 'h', 'd', '+', 'o']

Tit = True

#stemmer = SnowballStemmer("english")

configFile = LoadConfig()
requete = configFile.requete
ndf = configFile.ndf

ResultPath = configFile.ResultPath
temporPath = configFile.temporPath
ResultContentsPath = configFile.ResultContentsPath
ResultBiblioPath = configFile.ResultBiblioPath
# at final step, next line should enter configFile as above
ResultPathContentAug =os.path.normpath('..//DATA//'+ndf+'//PatentContents//Metrics')
Excluded = []

EnsVoc = dict()
Labelle  = OrderedDict()
if "Excluding-voc.txt" not in os.listdir(ResultPath):
    Excl = open(os.path.normpath(os.path.join(ResultPath,'Excluding-voc.txt')), 'w')
    print("I've created a new empty file " + ResultPath +"//Excluding-voc.txt")
    print ("Consider revisiting it to exclude vocabulary (coma separated terms) from process")
    Excl.write('\n')
    Excl.close()
    
with open (os.path.normpath(os.path.join(ResultPath, 'Excluding-voc.txt')), 'r') as fic:
    data = fic.read()
    brev_stpswrds  = data.split(',')
    stopwords.extend(brev_stpswrds) # for tdidf vectorizer
    Excluded.extend(brev_stpswrds)  # for cluster presentation
    
if 'Description'+ndf or 'Description'+ndf.lower() in os.listdir(ResultBiblioPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
    ficBrevet = LoadBiblioFile(ResultBiblioPath, ndf)
else: #Retrocompatibility
    print ('gather your data again. sorry')
    sys.exit()

if ficBrevet.has_key('brevets'):
    lstBrevet = ficBrevet['brevets']
#        if data.has_key('requete'):
#            DataBrevet['requete'] = data["requete"]
    print ("Found "+ ndf+ " datafile with " +str(len(lstBrevet)) + " patents!")
else:
    print ('gather your data again')
    sys.exit()

cles =  ['IPCR11', 'CitO', 'dateDate', 'inventor-nice', 'equivalents', 'CitedBy', 'representative', 'Inventor-Country', 'date', 'inventor', 'kind', 'priority-active-indicator', 'applicant-nice', 'IPCR1', 'country', 'IPCR3', 'applicant', 'IPCR4', 'IPCR7', 'title', 'application-ref']
Titles = []
Labels = []

Abstracts  = [] # Pure abstracts
IPCRsText  = []

Contents = joblib.load(os.path.normpath(ResultContentsPath+'//Contents-'+ndf+'.pkl'))   # Contains IPCRs (text of associated IPCR classes) + title + abstracts 
Titles = joblib.load( os.path.normpath(ResultContentsPath+'//Titles-'+ndf+'.pkl'))
Labels = joblib.load( os.path.normpath(ResultContentsPath+'//Labels-'+ndf+'.pkl'))
IPCRsText = joblib.load( os.path.normpath(ResultContentsPath+'//IPCRsText-'+ndf+'.pkl'))
Abstracts = joblib.load( os.path.normpath(ResultContentsPath+'//Abstracts-'+ndf+'.pkl'))
CIB = []

print("loading patents contents")
#
Tit2FicName=joblib.load(os.path.normpath(ResultContentsPath+'//Titles_ficNames-'+ndf+'.pkl'))
#
FreqTrie= joblib.load(os.path.normpath(ResultContentsPath+'//FreqTrie'+ndf+'.pkl'))
word_freq_df = joblib.load(os.path.normpath(ResultContentsPath+'//word_freq'+ndf+'.pkl'))

D0=len(set(word_freq_df['term'])) #unic forms of corpus
H0=np.log(D0) # 
H1=-sum([pi* np.log(pi) for pi in FreqTrie.get_values().transpose()[2]]) #pi means p_i in latex writing style ;-). Shannon entropy
D1 = np.exp(H1)
R = np.abs(H1/H0) #regularité
C=sum([ np.emath.power(pi,2) for pi in FreqTrie.get_values().transpose()[2]])
H2 = -np.log(C)
D2 =  1/C                       #trivial shortcut
Lt = H1-H2
Li = (H1+H2)/H1
Lb = H0-H1
Cb= D0 -D0*(1/R)*(Lb/(Lb+Lt+Li)) # noise shortcut 
CuttingLeft=int(Cb) #Lhen, J, T Lafouge, Y Elskens, L Quoniam, et H Dou. « La statistique des lois de Zipf, actes du colloque, Les systèmes d’informations élaborés ». In Les systèmes d’information élaborés. Ile Rousse - Corse: Société Française de Bibliométrie Appliquée, 1995.
CuttingRight=int(D2)
minDf = FreqTrie.get_values().transpose()[2][CuttingLeft]
maxDf = FreqTrie.get_values().transpose()[2][CuttingRight]
I1 = len( FreqTrie[FreqTrie['occurrences']==1]) # words of Occurence =1
rankGoffman  = int(round(np.sqrt(1+8+I1)-1)/2) 
GoodZone = FreqTrie[rankGoffman:CuttingRight] # non trivial and non noisy terms
#`olders test with int(round(np.sqrt(1+8+I1)-1/2)) !!!!
Goffman = range(rankGoffman -5, rankGoffman +5)
Rk, Val,Term = [], [], []
#GoffmanWords = FreqTrie.values[Goffman]


ValueTerms = GoodZone['term'].tolist()
bigrams = [truc for truc in ValueTerms if isinstance(truc.split(' '), list) and (len(truc.split(' ')) ==2)]
trigrams = [truc for truc in ValueTerms if isinstance(truc.split(' '), list) and (len(truc.split(' ')) ==3)]
quadrigrams = [truc for truc in ValueTerms if isinstance(truc.split(' '), list) and (len(truc.split(' ')) ==4)]
monog = [truc for truc in ValueTerms if ' ' not in truc]
EnsVoc=joblib.load(os.path.normpath(ResultContentsPath+'//EnsVocFile'+ndf +'.pkl'))
Voc=joblib.load(os.path.normpath(ResultContentsPath+'//VocFile'+ndf+ '.pkl'))
#cleanning exluded words  
for termes in Excluded:
    for mot in bigrams:
        for sousmot in mot.split():
            if termes == sousmot:
                bigrams.remove(mot)
    for mot in trigrams:
        for sousmot in mot.split():
            if termes == sousmot:
                trigrams.remove(mot)
    
    for mot in quadrigrams:
        for sousmot in mot.split():
            if termes == sousmot:
                quadrigrams.remove(mot)

quadripc = [truc for truc in quadrigrams if truc in Voc['IPC']]    
tripc = [truc for truc in trigrams if truc in Voc['IPC']]  
bipc = [truc for truc in bigrams if truc in Voc['IPC']]  
print ("Taille des quadripc", len(quadripc))
print ("Taille des tripc", len(tripc)) 
quadripc = [truc for truc in quadrigrams if truc in Voc['IPC']]    
tripc = [truc for truc in trigrams if truc in Voc['IPC']]  
bipc = [truc for truc in bigrams if truc in Voc['IPC']]  

print (len(monog) + len(bigrams) + len(trigrams) +len(quadrigrams))
 
DicoMaxiGood = OrderedDict()    

for thing in GoodZone[rankGoffman-rankGoffman/2:CuttingRight].values:
    if thing[1] in quadripc:
        DicoMaxiGood [thing[1]] = thing[2]
    elif thing[1] in tripc:
            DicoMaxiGood [thing[1]] = thing[2]
    elif thing[1] in bigrams:
            DicoMaxiGood [thing[1]] = thing[2] 
    else:
        pass
# NExt is for future computing : the code aims to detail in witch documents MaxiGood word appears
#for thing in GoodZone[rankGoffman-rankGoffman/4:CuttingRight].values:
#    if thing[1] in  quadripc:
#        DicoMaxiGood [thing[1]] = [thing[2], vectorizer.get_feature_names().index(thing[1])]
#if len(DicoMaxiGood) > 80:
#    print ("say enought with 4-gramms")
#else:
#    for thing in GoodZone[Goffman-Goffman/4:CuttingRight].values:
#        if thing[1] in tripc:
#            DicoMaxiGood [thing[1]] = [thing[2] , vectorizer.get_feature_names().index(thing[1]) ] 
#        elif thing[1] in bigrams:
#            DicoMaxiGood [thing[1]] = [thing[2] , vectorizer.get_feature_names().index(thing[1]) ] 
#Dico2 = dict()#new df
#for cle in DicoMaxiGood.keys():
#    Dico2[cle]=tfidf_matrix.getcol(DicoMaxiGood[cle][1]).transpose()


###◘
#learnig from IPC vocabulary 
vectorizer = TfidfVectorizer(stop_words=stopwords, use_idf=True, tokenizer=tokenize_only, 
                             ngram_range=(1,4), vocabulary = DicoMaxiGood.keys())
PreX = vectorizer.fit_transform(Contents)           
km2 = KMeans(n_clusters=num_clusters , init='k-means++', max_iter=100, n_init=1, verbose=True)
#define vectorizer parameters
km2.fit(PreX)


labels=range(num_clusters)
Preclusters = km2.labels_.tolist()
 
terms = vectorizer.get_feature_names()

print ("say enought with 3, 4-gramms", len(DicoMaxiGood.keys()))
#selcting document with the msemantic terms
Precluster_names = dict()
#X2 = pd.DataFrame.from_dict(Dico2, orient='columns')
#cleaning words from classes names
Preorder_centroids = km2.cluster_centers_.argsort()[:, ::-1] 
for i in range(num_clusters):
    Precluster_names [i] =[]
    for ind in Preorder_centroids[i, :15]: #arbitrar 20 
        #word=word_freq_df.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore')
        word=terms[ind].encode('utf-8', 'ignore')
        if word not in stopwords and word not in ' '.join(Precluster_names [i]):
            if isinstance(word.split(), list):
                cpt =0
                for mot in word.split():
                    if mot in ' '.join(Precluster_names [i]):
                        cpt+=1
                if cpt<len(word.split()):
                    Precluster_names [i].append(word )
            else:
                Precluster_names [i].append(word )
    Precluster_names [i] = set(Precluster_names [i]) 
NewClusName2 = dict()
for ind in Precluster_names.keys():
    NewClusName2[ind] =[]
    OderKeys = Precluster_names.keys()
    OderKeys.remove(ind)
    Other = []
    for termes in OderKeys:
        Other.extend(Precluster_names[termes])
    for mot in Precluster_names[ind]:
        if mot not in Other:
            NewClusName2[ind].append(mot) #excluding word belonging to two classes
    tempo = NewClusName2[ind]

    for mot in NewClusName2[ind]:#excluding words belonging to other terms in same classes
        if len(mot)>1:
            for mot2 in tempo:
                if mot != mot2:
                    if mot2 in mot:
                        try:
                            NewClusName2[ind].remove(mot)
                        except:
                            try:
                                NewClusName2[ind].remove(mot2)
                            except:
                                pass
    print (len(NewClusName2[ind]))
    NewClusName2[ind] = ','.join(NewClusName2[ind])
for i in range(num_clusters):    
    Precluster_names [i] = ','.join(list(Precluster_names [i])[:6])

vectorizer = TfidfVectorizer(stop_words=stopwords, use_idf=True, tokenizer=tokenize_only, ngram_range=(1,4))
X = vectorizer.fit_transform(Contents)    
km = KMeans(n_clusters=num_clusters, init="k-means++", max_iter=15, n_init=1, verbose=True)
km.fit(X)

cluster_names = dict()
print("Clustering sparse data with %s" % km)
print()
labels=range(num_clusters)
print("Top terms per cluster:")
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
clusters = km.labels_.tolist()
#
Brevets = { 'title': Titles, 'labels': Labels, 'abstracts': Abstracts, 'IPC': IPCRsText, 'cluster': clusters }


frame = pd.DataFrame(Brevets, index = [clusters] , columns = ['labels', 'title',  'IPC','cluster'])
frame['cluster'].value_counts() #number of patents per cluster (clusters from 0 to 4)

#sort cluster centers by proximity to centroid
order_centroids = km.cluster_centers_.argsort()[:, ::-1] 

#set up colors per clusters using a dict
#Ðcluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e', 5: '#ff6a61',6: '#00ff1e', 7: '#0001FF'}
cluster_names = dict()
#set up cluster names using a dict
#quite the same cleaning process as above
for i in range(num_clusters):
    cluster_names [i] =[]
    for ind in order_centroids[i, :15]: #arbitrar 20 
        #word=word_freq_df.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore')
        word=word_freq_df['term'].tolist()[ind].encode('utf-8', 'ignore')
        if word not in stopwords and word not in ' '.join(cluster_names [i]):
            if isinstance(word.split(), list):
                cpt =0
                for mot in word.split():
                    if mot in ' '.join(cluster_names [i]):
                        cpt+=1
                if cpt<len(word.split()):
                    cluster_names [i].append(word )
            else:
                cluster_names [i].append(word )
    cluster_names [i] = set(cluster_names [i]) 
NewClusName = dict()
for ind in cluster_names.keys():
    NewClusName[ind] =[]
    OderKeys = cluster_names.keys()
    OderKeys.remove(ind)
    Other = []
    for termes in OderKeys:
        Other.extend(cluster_names[termes])
    for mot in cluster_names[ind]:
        if mot not in Other:
            NewClusName[ind].append(mot) #excluding word belonging to two classes
    tempo = NewClusName[ind]
    for mot in NewClusName[ind]:#excluding words belonging to other terms in same classes
        if len(mot)>1:
            for mot2 in tempo:
                if mot != mot2:
                    if mot2 in mot:
                        try:
                            NewClusName[ind].remove(mot)
                        except:
                            try:
                                NewClusName[ind].remove(mot2)
                            except:
                                pass
    print (len(NewClusName[ind]))
    NewClusName[ind] = ','.join(NewClusName[ind])
for i in range(num_clusters):    
    cluster_names [i] = ','.join(list(cluster_names [i])[:6])
    
    
MDS()
dist = 1 - cosine_similarity(X)
# convert two components as we're plotting points in a two-dimensional plane
# "precomputed" because we provide a distance matrix
# we will also specify `random_state` so the plot is reproducible.
mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

pos = mds.fit_transform(dist)  # shape (n_components, n_samples)

xs, ys = pos[:, 0], pos[:, 1]
print()
#%matplotlib inline 

#create data frame that has the result of the MDS plus the cluster numbers and titles
df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=Titles)) 
df2 = pd.DataFrame(dict(x=xs, y=ys, label=Preclusters, title=Titles)) 
groups2 = df2.groupby(Preclusters)
#group by cluster
groups = df.groupby(clusters)




    
print (cluster_names)



class TopToolbar(mpld3.plugins.PluginBase):
    """Plugin for moving toolbar to top of figure"""

    JAVASCRIPT = """
    mpld3.register_plugin("toptoolbar", TopToolbar);
    TopToolbar.prototype = Object.create(mpld3.Plugin.prototype);
    TopToolbar.prototype.constructor = TopToolbar;
    function TopToolbar(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    TopToolbar.prototype.draw = function(){
      // the toolbar svg doesn't exist
      // yet, so first draw it
      this.fig.toolbar.draw();

      // then change the y position to be
      // at the top of the figure
      this.fig.toolbar.toolbar.attr("x", 1200);
      this.fig.toolbar.toolbar.attr("y", 310);

      // then remove the draw function,
      // so that it is not called again
      this.fig.toolbar.draw = function() {}
    }
    
    """
    def __init__(self):
        self.dict_ = {"type": "toptoolbar"}
        
class ClickInfo(mpld3.plugins.PluginBase):
    """Hack of mpld3 Plugin for getting info on click adding "on mouse over" tooltip function   """

    JAVASCRIPT = """
    mpld3.register_plugin("ClickInfo", ClickInfo);
    ClickInfo.prototype = Object.create(mpld3.Plugin.prototype);
    ClickInfo.prototype.constructor = ClickInfo;
    ClickInfo.prototype.requiredProps = ["id", "urls", "labels"];
    ClickInfo.prototype.defaultProps = {hoffset:10,
                                                voffset:10};
        
    function ClickInfo(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    ClickInfo.prototype.draw = function(){
        var obj = mpld3.get_element(this.props.id);
        urls = this.props.urls;
        labels = this.props.labels;
        var tooltip = d3.select("body").append("div")
                    .attr("class", "mpld3-tooltip")
                    .style("position", "absolute")
                    .style("z-index", "10")
                    .style("visibility", "hidden");
        obj.elements().on("mousedown",
                          function(d, i){ 
                            window.open(urls[i], '_blank')});
        obj.elements().on("mouseover", function(d, i){
                              tooltip.html(labels[i])
                                     .style("visibility", "visible");});
        obj.elements().on("mouseout",  function(d, i){
                           tooltip.style("visibility", "hidden");});
    }
    """
    def __init__(self, points, labels, urls,
                 hoffset=0, voffset=10, css=None):
        self.points = points
        self.urls = urls
        self.labels = labels
        self.voffset = voffset
        self.hoffset = hoffset
        self.css_ = css or ""
        if isinstance(points, matplotlib.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None
        self.dict_ = {"type": "ClickInfo",
                      "id": mpld3.utils.get_id(points, suffix),
                      "urls": urls,
                      "labels": labels,
                      "hoffset": hoffset,
                      "voffset": voffset}


#create data frame that has the result of the MDS plus the cluster numbers and titles
df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=Titles)) 
import mpld3
from mpld3 import plugins
from mpld3.utils import get_id
#group by cluster
 

 

#define custom css to format the font and to remove the axis labeling
css = """
text.mpld3-text, div.mpld3-tooltip {
  font-family:Arial, Helvetica, sans-serif;
}

g.mpld3-xaxis, g.mpld3-yaxis {
display: none; }

svg.mpld3-figure {
margin-left: -200px;
margin-right: -300px;}}
"""

# Plot 
fig, ax = plt.subplots(figsize=(22,12)) #set plot size
ax.margins(0.03) # Optional, just adds 5% padding to the autoscaling
fig.subplots_adjust(right=0.7)
memoFig =[] #fig memoriz
memoCoul = []#cool memoriz
memoLab=[]
memoLab2=[]#Lab memoriz
#iterate through groups to layer the plot
#note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
ClickNfo = []
tempoLab =[]
tempoFic = []
Here = os.getcwdu().replace('\\', '//')
Here = Here.replace('Patent2Net', ResultPathContentAug[ResultPathContentAug.index('DATA'):])+'//'


print (len(tempoLab))
print (len(tempoFic))
 #tooltip
  
#leg=ax.legend(numpoints=1, bbox_to_anchor=(1.60, 0), loc='lower right') #show legend with only one dot
#leg.draggable(state=True)
#    
#interactive_legend = plugins.InteractiveLegendPlugin(memoFig,  memoLab , 
#                                                          alpha_unsel=0.2, alpha_over=1.5, start_visible=True)
memoFig2 =[]
memoLab2=[]
tempoFic = []
MemoPoints= dict()
for name, group in groups2: 
    
#    points = ax.plot(group.x, group.y, marker='o', linestyle='', ms=10, 
#                     mec= cluster_colors [name],color=cluster_colors [name])
    points = ax.plot(group.x, group.y, marker='x', linestyle='', ms=10, mew=3, #♀title = 'test1a',
                     mec= 'red',color=cluster_colors[name], alpha=0.9)
    
    for cle in group.x.keys():
        MemoPoints[(group.x[cle], group.y[cle])] =group.title[cle]
    memoFig2.append(points)
    memoLab2.append(NewClusName2[name])
    

    Lab = [ lab  for lab in labels]
    tempoLab.extend(Lab)
    #tempoFic.append(TitFic)
#iterFic=iter(tempoFic)
#for ligne in  fig.get_axes()[0].lines[11:22]:#memoFig2:#
#    mpld3.plugins.connect(fig, mpld3.plugins.ClickInfo( ligne,  urls = iterFic.next()))
for name, group in groups:
    points = ax.plot(group.x, group.y, marker='o', linestyle='', ms=18, mec='none',
                       label=cluster_names[name], title = 'test1b',
                     color=cluster_colors2[name], alpha=0.6 
                     )
    memoFig.append(points)
    memoCoul.append(cluster_colors[name])
    memoLab.append(cluster_names[name])
    
    ax.set_aspect('auto')
    labels = [i for i in group.title]
    #memoLab2.append(labels)

    #set tooltip using points, labels and the already defined 'css'
#    tooltip = mpld3.plugins.PointHTMLTooltip(points[0], labels,
#                                       voffset=10, hoffset=10, css=css)
#    #connect tooltip to fig
#    mpld3.plugins.connect(fig, tooltip, TopToolbar())     
    
    #set tick marks as blank
    ax.axes.get_xaxis().set_ticks([])
    ax.axes.get_yaxis().set_ticks([])
    
    #set axis as blank
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    #next shoul be done at the en of loop for I guess
    #TitFic = ['file:///D:/Doc-David/Developpement/SpyderWorkspace/Git-P2N/DATA/Banana/PatentContents/Metrics/' +Tit2FicName [lab] for lab in labels]
    TitFic = ['file:///'+ Here +Tit2FicName [lab] for lab in labels]
    tempoLab.append(labels)
    tempoFic.append(TitFic)
    
interactive_legend = plugins.InteractiveLegendPlugin(memoFig , memoLab, legend_offset=(0,300), title = 'test2a',
                                                         alpha_unsel=0.1, alpha_over=0.9, start_visible=False)
interactive_legend2 = plugins.InteractiveLegendPlugin(memoFig2,  memoLab2, legend_offset=(0,0), title = 'test2b',
                                                          alpha_unsel=0.1, alpha_over=0.8, start_visible=False)
#TitFics = []
#tempoFic=[]

mpld3.plugins.connect(fig,interactive_legend)
mpld3.plugins.connect(fig,interactive_legend2)   

tooltip =dict()
for ligne in fig.get_axes()[0].lines:
        Urls=[]
        labels =[]
        for point in ligne.get_xydata():
            if tuple(point) in MemoPoints.keys():
                Urls.append('file:///'+ Here +Tit2FicName [MemoPoints[tuple(point)]])
                labels.append(MemoPoints[tuple(point)])
            else:
                print("should never be here")
        mpld3.plugins.connect(fig, ClickInfo( ligne, labels=labels,  urls = Urls))
 
mpld3.plugins.connect(fig, TopToolbar())

from pandas.plotting import scatter_matrix
ptl = scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')


#uncomment the below to export to html
html = mpld3.fig_to_html(fig)

with open(os.path.normpath(ResultPath+"//"+ndf+"-Clust.html", "w")) as fic:
    fic.write(html)
 
#plt.close()




#grouped = frame['CIB'].groupby(frame['cluster']) #groupby cluster for aggregation purposes

#grouped.mean() #average rank (1 to 100) per cluster
#set up cluster names using a dict


#print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels, km.labels_))
#print("Completeness: %0.3f" % metrics.completeness_score(labels, km.labels_))
#print("V-measure: %0.3f" % metrics.v_measure_score(labels, km.labels_))
#print("Adjusted Rand-Index: %.3f"
#      % metrics.adjusted_rand_score(labels, km.labels_))
#print("Silhouette Coefficient: %0.3f"
#      % metrics.silhouette_score(X, km.labels_, sample_size=1000))