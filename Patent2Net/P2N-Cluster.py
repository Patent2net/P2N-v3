# -*- coding: utf-8 -*-
"""
Created on Sat Jul 08 16:24:35 2017

@author: dreymond
"""




import os
import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import MDS
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords as nltkSW
from Patent2Net.TAL_P2N_Lib import tokenize_only, tokenize_and_stem
from Patent2Net.P2N_Lib import LoadBiblioFile, AnnonceProgres
from Patent2Net.P2N_Config import LoadConfig

import collections
import matplotlib
import matplotlib.pyplot as plt

import mpld3
from mpld3.utils import get_id
import numpy as np
import logging
import joblib
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
Labelle  = collections.OrderedDict()
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

if 'brevets' in ficBrevet:
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
Goffman = list(range(rankGoffman -5, rankGoffman +5))
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
 
DicoMaxiGood = collections.OrderedDict()    

for thing in GoodZone[int(rankGoffman-rankGoffman/2):CuttingRight].values:
    if thing[0] in quadripc:
        DicoMaxiGood [thing[0]] = thing[2]
    elif thing[0] in tripc:
            DicoMaxiGood [thing[0]] = thing[2]
    elif thing[0] in bigrams:
            DicoMaxiGood [thing[0]] = thing[2] 
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
                             ngram_range=(1,4), vocabulary = list(DicoMaxiGood.keys()))
PreX = vectorizer.fit_transform(Contents)           
km2 = KMeans(n_clusters=num_clusters , init='k-means++', max_iter=100, n_init=1, verbose=True)
#define vectorizer parameters
km2.fit(PreX)


labels=list(range(num_clusters))
Preclusters = km2.labels_.tolist()
 
terms = vectorizer.get_feature_names()

print ("say enought with 3, 4-gramms", len(list(DicoMaxiGood.keys())))
#selcting document with the msemantic terms
Precluster_names = dict()
#X2 = pd.DataFrame.from_dict(Dico2, orient='columns')
#cleaning words from classes names
Preorder_centroids = km2.cluster_centers_.argsort()[:, ::-1] 
for i in range(num_clusters):
    Precluster_names [i] =[]
    for ind in Preorder_centroids[i, :15]: #arbitrar 20 
        #word=word_freq_df.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore')
        word=terms[ind]# .encode('utf-8', 'ignore') Put the comment here 25/04/2019
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
for ind in list(Precluster_names.keys()):
    NewClusName2[ind] =[]
    OderKeys = list(Precluster_names.keys())
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
labels=list(range(num_clusters))
print("Top terms per cluster:")
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
clusters = km.labels_.tolist()
#
Brevets = { 'title': Titles, 'labels': Labels, 'abstracts': Abstracts, 'IPC': IPCRsText, 'cluster': clusters }


frame = pd.DataFrame(Brevets, index = [clusters] , columns = ['labels', 'title',  'IPC','cluster'])
frame['cluster'].value_counts() #number of patents per cluster (clusters from 0 to 4)

#sort cluster centers by proximity to centroid
order_centroids = km.cluster_centers_.argsort()#♣[:, ::-1] 

#set up colors per clusters using a dict
#Ðcluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e', 5: '#ff6a61',6: '#00ff1e', 7: '#0001FF'}
cluster_names = dict()
#set up cluster names using a dict
#quite the same cleaning process as above
for i in range(num_clusters):
    cluster_names [i] =[]
    for ind in order_centroids[i, :11]: #arbitrar 20 
        #word=word_freq_df.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore')
        #word=word_freq_df['term'].tolist()[ind]#.encode('utf-8', 'ignore') same he 04/19
        #changed 21/07/19
        word=terms[ind]
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
for ind in list(cluster_names.keys()):
    NewClusName[ind] =[]
    OderKeys = list(cluster_names.keys())
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
class InteractiveLegendPlugin(mpld3.plugins.PluginBase):
    """A plugin for an interactive legends.

    Inspired by http://bl.ocks.org/simzou/6439398

    Parameters
    ----------
    plot_elements : iterable of matplotlib elements
        the elements to associate with a given legend items
    labels : iterable of strings
        The labels for each legend element
    ax :  matplotlib axes instance, optional
        the ax to which the legend belongs. Default is the first
        axes. The legend will be plotted to the right of the specified
        axes
    alpha_unsel : float, optional
        the alpha value to multiply the plot_element(s) associated alpha
        with the legend item when the legend item is unselected.
        Default is 0.2
    alpha_over : float, optional
        the alpha value to multiply the plot_element(s) associated alpha
        with the legend item when the legend item is overlaid.
        Default is 1 (no effect), 1.5 works nicely !
    start_visible : boolean, optional (could be a list of booleans)
        defines if objects should start selected on not.
    font_size : int, optional
        defines legend font-size.
        Default is 10.
    legend_offset : list of int (length: 2)
        defines horizontal offset and vertical offset of legend.
        Default is (0, 0).

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from mpld3 import fig_to_html, plugins
    >>> N_paths = 5
    >>> N_steps = 100
    >>> x = np.linspace(0, 10, 100)
    >>> y = 0.1 * (np.random.random((N_paths, N_steps)) - 0.5)
    >>> y = y.cumsum(1)
    >>> fig, ax = plt.subplots()
    >>> labels = ["a", "b", "c", "d", "e"]
    >>> line_collections = ax.plot(x, y.T, lw=4, alpha=0.6)
    >>> interactive_legend = plugins.InteractiveLegendPlugin(line_collections,
    ...                                                      labels,
    ...                                                      alpha_unsel=0.2,
    ...                                                      alpha_over=1.5,
    ...                                                      start_visible=True,
    ...                                                      font_size=14,
    ...                                                      legend_offset=(-100,20))
    >>> plugins.connect(fig, interactive_legend)
    >>> fig_to_html(fig)
    """

    JAVASCRIPT = """
    mpld3.register_plugin("interactive_legend", InteractiveLegend);
    InteractiveLegend.prototype = Object.create(mpld3.Plugin.prototype);
    InteractiveLegend.prototype.constructor = InteractiveLegend;
    InteractiveLegend.prototype.requiredProps = ["element_ids", "labels"];
    InteractiveLegend.prototype.defaultProps = {"ax":null,
                                                "title":"text title", 
                                                "alpha_unsel":0.2,
                                                "alpha_over":1.0,
                                                "start_visible":true,
                                                "font_size": 10,
                                                "legend_offset": [0,0]}
    function InteractiveLegend(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    InteractiveLegend.prototype.draw = function(){
        var ax = this.props.ax
        var title = this.props.title;
        var alpha_unsel = this.props.alpha_unsel;
        var alpha_over = this.props.alpha_over;
        var font_size = this.props.font_size;
        var legend_offset = this.props.legend_offset;
        this.fig.canvas.append("text")
            .text(title)
            .style("font-size", 20)
            .style("opacity", 1)
            .style("text-anchor", "right")
            .attr("x",2*this.fig.width/3 + 50 + legend_offset[0])
            .attr("y", this.fig.height/9 + legend_offset[1] )
        var legendItems = new Array();
        for(var i=0; i<this.props.labels.length; i++){
            var obj = {};
            obj.label = this.props.labels[i];

            var element_id = this.props.element_ids[i];
            mpld3_elements = [];
            for(var j=0; j<element_id.length; j++){
                var mpld3_element = mpld3.get_element(element_id[j], this.fig);

                // mpld3_element might be null in case of Line2D instances
                // for we pass the id for both the line and the markers. Either
                // one might not exist on the D3 side
                if(mpld3_element){
                    mpld3_elements.push(mpld3_element);
                }
            }

            obj.mpld3_elements = mpld3_elements;
            obj.visible = this.props.start_visible[i]; // should become be stable from python side
            legendItems.push(obj);
            set_alphas(obj, false);
        }

        // determine the axes with which this legend is associated
        
        if(!ax){
            ax = this.fig.axes[0];
        } else{
            ax = mpld3.get_element(ax, this.fig);
        }

        // add a legend group to the canvas of the figure
        var legend = this.fig.canvas.append("svg:g")
                               .attr("class", "legend");

        // add the rectangles
        legend.selectAll("rect")
                .data(legendItems)
                .enter().append("rect")
                .attr("height", 0.7*font_size)
                .attr("width", 1.6*font_size)
                .attr("x", ax.width + ax.position[0] + 15 + legend_offset[0])
                .attr("y",function(d,i) {
                           return ax.position[1] + i * (font_size+5) + 10 + legend_offset[1];})
                .attr("stroke", get_color)
                .attr("class", "legend-box")
                .style("fill", function(d, i) {
                           return d.visible ? get_color(d) : "white";})
                .on("click", click).on('mouseover', over).on('mouseout', out);

        // add the labels
        legend.selectAll("text")
              .data(legendItems)
              .enter().append("text")
              .attr("font-size", font_size)
              .attr("x", function (d) {
                           return ax.width + ax.position[0] + (1.9*font_size+15) + legend_offset[0];})
              .attr("y", function(d,i) {
                           return ax.position[1] + i * (font_size+5) + 10 + (0.72*font_size-1) + legend_offset[1];})
              .text(function(d) { return d.label })
              .on('mouseover', over).on('mouseout', out);


        // specify the action on click
        function click(d,i){
            d.visible = !d.visible;
            d3.select(this)
              .style("fill",function(d, i) {
                return d.visible ? get_color(d) : "white";
              })
            set_alphas(d, false);

        };

        // specify the action on legend overlay 
        function over(d,i){
             set_alphas(d, true);
        };

        // specify the action on legend overlay 
        function out(d,i){
             set_alphas(d, false);
        };

        // helper function for setting alphas
        function set_alphas(d, is_over){
            for(var i=0; i<d.mpld3_elements.length; i++){
                var type = d.mpld3_elements[i].constructor.name;

                if(type =="mpld3_Line"){
                    var current_alpha = d.mpld3_elements[i].props.alpha;
                    var current_alpha_unsel = current_alpha * alpha_unsel;
                    var current_alpha_over = current_alpha * alpha_over;
                    d3.select(d.mpld3_elements[i].path[0][0])
                        .style("stroke-opacity", is_over ? current_alpha_over :
                                                (d.visible ? current_alpha : current_alpha_unsel))
                        .style("stroke-width", is_over ? 
                                alpha_over * d.mpld3_elements[i].props.edgewidth : d.mpld3_elements[i].props.edgewidth);
                } else if((type=="mpld3_PathCollection")||
                         (type=="mpld3_Markers")){
                    var current_alpha = d.mpld3_elements[i].props.alphas[0];
                    var current_alpha_unsel = current_alpha * alpha_unsel;
                    var current_alpha_over = current_alpha * alpha_over;
                    d3.selectAll(d.mpld3_elements[i].pathsobj[0])
                        .style("stroke-opacity", is_over ? current_alpha_over :
                                                (d.visible ? current_alpha : current_alpha_unsel))
                        .style("fill-opacity", is_over ? current_alpha_over :
                                                (d.visible ? current_alpha : current_alpha_unsel));
                } else{
                    console.log(type + " not yet supported");
                }
            }
        };


        // helper function for determining the color of the rectangles
        function get_color(d){
            var type = d.mpld3_elements[0].constructor.name;
            var color = "black";
            if(type =="mpld3_Line"){
                color = d.mpld3_elements[0].props.edgecolor;
            } else if((type=="mpld3_PathCollection")||
                      (type=="mpld3_Markers")){
                color = d.mpld3_elements[0].props.facecolors[0];
            } else{
                console.log(type + " not yet supported");
            }
            return color;
        };
    };
    """

    css_ = """
    .legend-box {
      cursor: pointer;
    }
    """

    def __init__(self, plot_elements, labels, ax=None, title='texte titre',
                 alpha_unsel=0.2, alpha_over=1., start_visible=True, font_size=10, legend_offset=(0,0)):

        self.ax = ax

        if ax:
            ax = get_id(ax)

        # start_visible could be a list
        if isinstance(start_visible, bool):
            start_visible = [start_visible] * len(labels)
        elif not len(start_visible) == len(labels):
            raise ValueError("{} out of {} visible params has been set"
                             .format(len(start_visible), len(labels)))     

        mpld3_element_ids = self._determine_mpld3ids(plot_elements)
        self.mpld3_element_ids = mpld3_element_ids
        self.dict_ = {"type": "interactive_legend",
                      "title" : title,
                      "element_ids": mpld3_element_ids,
                      "labels": labels,
                      "ax": ax,
                      "alpha_unsel": alpha_unsel,
                      "alpha_over": alpha_over,
                      "start_visible": start_visible,
                      "font_size": font_size,
                      "legend_offset": legend_offset}

    def _determine_mpld3ids(self, plot_elements):
        """
        Helper function to get the mpld3_id for each
        of the specified elements.
        """
        mpld3_element_ids = []

        # There are two things being done here. First,
        # we make sure that we have a list of lists, where
        # each inner list is associated with a single legend
        # item. Second, in case of Line2D object we pass
        # the id for both the marker and the line.
        # on the javascript side we filter out the nulls in
        # case either the line or the marker has no equivalent
        # D3 representation.
        for entry in plot_elements:
            ids = []
            if isinstance(entry, collections.Iterable):
                for element in entry:
                    mpld3_id = get_id(element)
                    ids.append(mpld3_id)
                    if isinstance(element, matplotlib.lines.Line2D):
                        mpld3_id = get_id(element, 'pts')
                        ids.append(mpld3_id)
            else:
                ids.append(get_id(entry))
                if isinstance(entry, matplotlib.lines.Line2D):
                    mpld3_id = get_id(entry, 'pts')
                    ids.append(mpld3_id)
            mpld3_element_ids.append(ids)

        return mpld3_element_ids




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
        var getUrl = window.location;
        if (getUrl.protocol==="file:") {
            var Chemin = getUrl.pathname.split('/').slice(0, 6);
            }
        else {
            var Chemin = getUrl.pathname.split('/').slice(0, 3);
            }
        var baseUrl = getUrl.protocol + "//" + getUrl.host + Chemin.join('/');
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
                            window.open(baseUrl+urls[i], '_blank')});
		obj.elements().on("mousemove", function(d, i){
                  tooltip
                    .style("top", d3.event.pageY + this.props.voffset + "px")
                    .style("left",d3.event.pageX + this.props.hoffset + "px");
                 }.bind(this))								  
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
#import mpld3
#from mpld3 import plugins

#group by cluster
 

 



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
Here = os.getcwd().replace('\\', '//')
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
tempoLab2 = []
for name, group in groups2: 
    
#    points = ax.plot(group.x, group.y, marker='o', linestyle='', ms=10, 
#                     mec= cluster_colors [name],color=cluster_colors [name])
    points = ax.plot(group.x, group.y, marker='x', linestyle='', ms=10, mew=3, #♀title = 'test1a',
                     mec= 'red',color=cluster_colors[name], alpha=0.9)
    
#
																  
    memoFig2.append(points)
    memoLab2.append(NewClusName2[name])
#    

    Lab = [ lab  for lab in labels]
#    tempoLab2.extend(Lab)
TitFic =[]

														 
																						
for name, group in groups:
    points = ax.plot(group.x, group.y, marker='o', linestyle='', ms=18, mec='none',
                       label=cluster_names[name], 
                     color=cluster_colors2[name], alpha=0.6 
                     )
#    memoPts.extend([tuple(truc) for truc in points[0].get_xydata()])
    memoFig.append(points)
#    memoFig3.extend(points)
    memoCoul.append(cluster_colors[name])
    memoLab.append(cluster_names[name])
    for cle in group.x.keys():
        MemoPoints[(group.x[cle], group.y[cle])] =group.title[cle]
    ax.set_aspect('auto')
    labels = [i for i in group.title]
#    Lab2.append(labels)
    #memoLab2.extend(group.title.values.tolist())
#    memoLab.append(cluster_names[name])
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
    TitFic += [['/PatentContents/Metrics/' + Tit2FicName [lab] for lab in labels]]
#    tempoLab.append(labels)
    #TiftempoFic.extend(TitFic)
    
        
interactive_legend = InteractiveLegendPlugin(memoFig , memoLab, legend_offset=(0,300), title = 'Choose kmeans++ classes from their most common terms',
                                                         alpha_unsel=0.1, alpha_over=0.9, start_visible=False)
interactive_legend2 = InteractiveLegendPlugin(memoFig2,  memoLab2, legend_offset=(0,0), title = 'Combine with IPC (mostly) terms in Goffman zone',
                                                          alpha_unsel=0.1, alpha_over=0.8, start_visible=False)
#TitFics = []
#tempoFic=[]

mpld3.plugins.connect(fig,interactive_legend)
mpld3.plugins.connect(fig,interactive_legend2) 
#fig.text(1, 1, "Here are some curves", size=18, ha='right')
#mpld3.plugins.connect(fig, ClickInfo( memoFig, labels=Lab2,  urls = TitFic))
indice=0 #to indiciate on filenames in Labels list
compt2 = 0
compt = 0
#tooltip =dict()        
Urls=[]
labels =[]
ligne=[]
for pt in fig.get_axes()[0].lines:
#    if compt2>len(Titles)/2:
				  
        for point in pt.get_xydata():
            if tuple(point) in MemoPoints.keys():
               Urls.append('/PatentContents/Metrics/' +Tit2FicName[MemoPoints[tuple(point)]])
               labels.append(Labels[indice % len(Titles)]+': '+ MemoPoints[tuple(point)])
               compt+=1
               ligne.append(pt)
            else:
                print("should never be here")
            indice+=1
        
    #compt2+=1

#REbulding a line for setting tooltips and clickpoint
indi1=0
indi2=0
Bulles =[]
for pt in fig.get_axes()[0].lines:
    indi2=indi1+len(pt.get_xydata())
    Bulles.append(ClickInfo(pt, labels[indi1:indi2], Urls[indi1:indi2],
                 hoffset=0, voffset=-30, css=None))
    indi1=indi2  
mpld3.plugins.connect(fig, TopToolbar())
Pt=[truc.points for truc in Bulles]
testo=[]
for tr in Pt:
   testo.extend(tr.get_xydata())
coord= np.asarray(testo)   
dessin = Pt[0].set_data(coord[:,0], coord[:,1])
points = ax.plot(coord[:,0], coord[:,1], marker='o', linestyle='', ms=18, mec= 'black',color='green', alpha=0.01)
mpld3.plugins.connect(fig, ClickInfo(points[0], labels, Urls,
                 hoffset=0, voffset=-30, css=None))
 
#define custom css to format the font and to remove the axis labeling
#css = """
#text.mpld3-text, div.mpld3-tooltip {
#  font-family:Arial, Helvetica, sans-serif;
#}
#
#g.mpld3-xaxis, g.mpld3-yaxis {
#display: none; }
#
#svg.mpld3-figure {
#margin-left: -200px;
#margin-right: -300px;}}
#""" 
css = """
text.mpld3-text, div.mpld3-tooltip {
  font-family:Arial, Helvetica, sans-serif;
  font-weight: bold;
  color: black;
  opacity: 1.0;
  padding: 2px;
  border: 0px;
}

g.mpld3-xaxis, g.mpld3-yaxis {
display: none; }

svg.mpld3-figure {
margin-left: -300px;
margin-right: -50px;}}

"""  


#uncomment the below to export to html
html = mpld3.fig_to_html(fig)

#mpld3.save_json(fig, ResultPath+"//"+ndf+"-Clust.json")
#Go for th ugly way
jsFile = [truc for truc in html.split('\n')]
sty = []
ind=0

while True:
    if '/style' in jsFile[ind]:
        sty.append(""".alert {
            padding: 20px;
            background-color: #f44336;
            color: white;
        }
        .danger {
            background-color: #ffdddd;
            border-left: 6px solid #f44336;
        }
        .closebtn {
            margin-left: 15px;
            color: white;
            font-weight: bold;
            float: right;
            font-size: 22px;
            line-height: 20px;
            cursor: pointer;
            transition: 0.3s;
        }
        
        .closebtn:hover {
            color: black;
        }
        
        
        .info {
            background-color: #e7f3fe;
            border-left: 6px solid #2196F3;
        }""")
        sty.append(css)
        sty.append(jsFile[ind])
        break
    else:
        sty.append(jsFile[ind])
        ind+=1
    if ind>5000:
        break #just in case
        
#define custom css to format the font and to remove the axis labeling
      
with open(os.path.normpath(ResultPath+"//"+"ClusterStyle.css"), "w") as fic:
    fic.write('\n'.join(sty))
while True:
    if jsFile[ind].count('/div'):
        divi=jsFile[ind]
        ind+=1
        break
    else:
        ind+=1
        if ind>5000:
            break #just in case
with open(os.path.normpath(ResultPath+"//"+ndf+"-Clust.src"), "w") as fic:
    fic.write('\n'.join(jsFile[ind+1:len(jsFile)-1]))
indi1= divi.index('"') +1
indi2 = divi[indi1:].index('"') + indi1
diviId= divi[indi1:indi2]
ficSrc = ndf+'-Clust.src'
html2 = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>P2N twin clusterisation (Abstract / IPC description)</title>
    <link rel="stylesheet" href="ClusterStyle.css">
    <script type="text/javascript" src="../../Patent2Net/extensions/mpld3/d3.v3.min.js"></script>
    <script type="text/javascript" src="../../Patent2Net/extensions/mpld3/mpld3.v0.2.js"></script>
       
  </head>
  <body>
  <h1>Double clusterisation features for abstracts from request:</h1></br>"""+requete +"""
  <h4>Use the cluster selector legend at the right side and allow popups to view patent abstracts and primary IPC's description</h3>
  <div class="info">
  <p><strong>Tip:</strong> Use Excluding-Voc.txt to specify coma separated vocabulary to be excluded from class representation. P2N-Cluster must be relaunched to take effect.</p>
</div>
  """+ divi + '\n' +  """
<script type="text/javascript" src="""+ficSrc +"""></script>
   <div class="danger">
  <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span>
</div> 
     
  </body>
</html>
"""
html2.replace("'", '"')

with open(os.path.normpath(ResultPath+"//"+ndf+"-Clust.html"), "w") as fic:
    fic.write(html2)
from pandas.plotting import scatter_matrix
ptl = scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')

AnnonceProgres (Appli = 'p2n_cluster', valMax = 100, valActu = 100/3)  
