# -*- coding: utf-8 -*-
"""
Created on Tue Avr 1 13:41:21 2014

@author: dreymond
"""
import networkx as nx
#import copy
from networkx.drawing.nx_agraph import graphviz_layout


#dicot = copy.deepcopy(dict)

import os
import sys
import datetime
import pydot
import ctypes # pydot needed for pyinstaller !!! seems that ctype also I should learn making hooks....
from urllib import quote as quot
import numpy as np
import matplotlib.cm
from collections import OrderedDict
from networkx_functs import calculate_degree, calculate_betweenness, calculate_degree_centrality
import cPickle as pickle
import copy
from P2N_Lib import UrlPatent,UrlApplicantBuild,UrlInventorBuild,UrlIPCRBuild, cmap_discretize, flatten, DecoupeOnTheFly, RenderTemplate
#from P2N_Lib import getStatus2, getClassif,getCitations, getFamilyLenght, isMaj, quote, GenereDateLiens
#from P2N_Lib import  symbole, ReturnBoolean, FormateGephi, GenereListeSansDate, GenereReseaux3, cmap_discretize
#from Ops3 import UnNest2List
from P2N_Config import LoadConfig

#read running mode
#screen size of JS windows (from Gexf-JS, should be 800x600)
screenX = 800
screenY = 600
Nets = ["CountryCrossTech", "CrossTech", "InventorsCrossTech", "Applicants_CrossTech", "Inventors",
 "ApplicantInventor", "Applicants", "References", "Citations", "Equivalents"]

if len(sys.argv)<2 or sys.argv[1] not in Nets:
    print "give me a net as parameter, one from this list: ", Nets
    sys.exit()
else:
    Nets.remove(sys.argv[1])
    if len(sys.argv) < 3:
        visu = 'neato'
    else:
        visu = sys.argv[2]

DureeBrevet = 20
SchemeVersion = '20140101' #for the url to the classification scheme

configFile = LoadConfig()
requete = configFile.requete
ndf = configFile.ndf
Gather = configFile.GatherContent
GatherBiblio = configFile.GatherBiblio
GatherPatent = configFile.GatherPatent
GatherFamilly = configFile.GatherFamilly



Networks = dict()
#next lines are here to avoid the changing scheme lecture of requete.cql
Networks["_CountryCrossTech"] =  [configFile.CountryCrossTechNetwork, [ 'IPCR7', "country"]]
Networks["_CrossTech"] =  [configFile.CrossTechNetwork, ['IPCR7']]
Networks["_InventorsCrossTech"] =  [configFile.InventorCrossTechNetwork, ['IPCR7', "inventor-nice"]]
Networks["_Applicants_CrossTech"] =  [configFile.ApplicantCrossTechNetwork, ['IPCR7', "applicant-nice"]]
Networks["_ApplicantInventor"] = [configFile.ApplicantInventorNetwork, ["applicant-nice", "inventor-nice"]]
Networks["_Applicants"] =  [configFile.ApplicantNetwork, ["applicant-nice"]]
Networks["_Inventors"] =  [configFile.InventorNetwork, ["inventor-nice"]]
Networks["_References"] =  [configFile.References, [ 'label', 'CitP', "CitO"]]
Networks["_Citations"] =  [configFile.Citations, [ 'label', "CitedBy"]]
Networks["_Equivalents"] =  [configFile.Equivalents, [ 'label', "equivalents"]]
ListeBrevet = []
Networks["_"+sys.argv[1]][0] = True #setting net to true but reading parameter file can reverse this

P2NComp = configFile.CompleteNetwork
P2NFamilly = configFile.GatherFamilly

 #should set a working dir one upon a time... done it is temporPath
ResultGephiPath = configFile.ResultGephiPath
BiblioPath = configFile.ResultBiblioPath
temporPath = configFile.temporPath

print "bibliographic data of ", ndf, " patent universe found."

NeededInfo = ['label', 'date', 'prior-dateDate']
#overloading toi False network creation, these are processed through p2n-NetworkMix script
for net in Nets: #passing other to false, but the script can be called
    Networks["_"+net][0] = False     # and the switch setted to false: the script won't process


prefixes = [""]
if P2NFamilly:
    prefixes.append("Families")

for prefix in prefixes:

    network = "_" +sys.argv[1]
    mixNet = Networks[network][1]
    if Networks[network][0]:

        G = nx.read_gpickle(temporPath+'/'+network + prefix)
    #arbiutrary
        G.graph['mode'] = "static"
        for k in G.nodes(): #statifying
                G.nodes(data=True)[k][1].pop('id', None)
                G.nodes(data=True)[k][1]['weight'] = G.nodes(data=True)[k][1]['weight']['value']
        G, deg = calculate_degree(G)
        G, bet = calculate_betweenness(G)

    #            #g, eigen = calculate_eigenvector_centrality(g)
    #            G, degcent = calculate_degree_centrality(G)
        size = len(mixNet)
        count = -1

        MaxWeight = -1
      #  if G == G1:
        tutu = [int(G.node[tt]['weight']) for tt in G.nodes()]
        if len(tutu)>0:
            Maxdegs = max(tutu)
        else:
            Maxdegs = 1
        zoom = len(G)*1.0/Maxdegs # should be function of network...
    #                #pos = nx.spring_layout(G, dim=2, k=2, scale =1)
     #                                        }

        #pos = nx.spring_layout( G, dim=2,  scale =10, iterations = 50)
        #arguDot='-Goverlap="0:prism" -Gsize="800,600" -GLT=550 -GKsep='+str(zoom+10)
        arguDot='-Goverlap="0:prism" -Gsize="1000,800" -GLT=550 -GKsep='+str(zoom)
        pos = graphviz_layout(G,prog=visu, args = arguDot )
     #    pos = nx.graphviz_layout(G,prog=visu)


        factx, facty = 1, 1 # neatto
        if len(pos)>0:
            MaxPosX = max([pos[k][0] for k in pos.keys()])
            MaxPosY = max([pos[k][1] for k in pos.keys()])
            MinPosX = min([pos[k][0] for k in pos.keys()])
            MinPosY = min([pos[k][1] for k in pos.keys()])
            GvScreenX = MaxPosX-MinPosX
            GvScreenY = MaxPosY-MinPosY
            factx = screenX/GvScreenX
            facty = screenX/GvScreenY
        else: #by the way this is an empty net
            MaxPosX = 200
            MaxPosY = 100
            MinPosX = -200
            MinPosY = -100
            GvScreenX = MaxPosX-MinPosX
            GvScreenY = MaxPosY-MinPosY
            factx = screenX/GvScreenX
            facty = screenX/GvScreenY
        if MinPosY>0:
            posx, posy = 0, -400
        else:
            posx, posy = 0, 0

         #one color for one kind of node


     #                   argu='-Goverlap="9:prism" -Gsize="1000,800" -Gdim=3 -Gdimen=2 -GLT=550 -GKsep='+str(zoom)
     #                   pos=nx.graphviz_layout(G,prog='sfdp', args = argu )
                #pos = nx.graphviz_layout(G, prog='dot', args = arguDot )

     #               pos = nx.spring_layout(G, dim=2, k=3, scale =1, iterations = 800)
               # pos = nx.spectral_layout(G, dim=2,scale =1)
    #                newCoord = project_points(pos[k][0], pos[k][1], pos[k][2], 0, 0, 1)
    #                Visu['position']= {'x':newCoord[0][0], 'y':newCoord[0][1], 'z':0}
    #                norme = np.linalg.norm(pos[k])
        cmpe = cmap_discretize(matplotlib.cm.jet, int(size))
        for k in G.nodes():
            #G.node[k]["weight"] = G.node[k]["weight"]['value'] # static net
            #G.node[k]["id"] = G.node[k]["id"]['id']
            Visu = dict()
            Visu['color'] = dict()
            #G.node[k]['label'] =  Nodes.keys()[k]
            #G.node[k]['category'] = Nodes[Nodes.keys()[k]]['category']
            if G.node[k]['category'] == 'label':
                G.node[k]['url'] =UrlPatent(G.node[k]['label'])[0]
                Visu['color']['a'] = 1
                Visu['color']['r']= int(254)
                Visu['color']['g']= int(0)
                Visu['color']['b']= int(0)
                Visu['shape'] ="diamond"
            elif G.node[k]['category'] =='CitP':
                    Visu['color']['a'] = 1
                    Visu['color']['r']= int(0)
                    Visu['color']['g']= int(254)
                    Visu['color']['b']= int(0)
                    Visu['shape'] ="ellipse"

            elif G.node[k]['category'] == 'CitO':
                # a hack here, trying to find out content in scholar
                #https:/scholar.google.fr/scholar?hl=fr&q=pipo+test&btnG=&lr=
                Visu['color']['r']= int(0)
                Visu['color']['g']= int(0)
                Visu['color']['b']= int(254)
                Visu['color']['a'] =1
                Visu['shape'] ="disc"
                #UrlTemp = "https:/scholar.google.com/scholar?q=" + quot(Nodes.keys()[k])
                #G.node[k]['url'] = UrlTemp
            elif G.node[k]['category'] == 'CitedBy':
                Visu['color']['a'] = 1
                Visu['color']['r']= int(0)
                Visu['color']['g']= int(127)
                Visu['color']['b']= int(127)
                Visu['shape'] ="square"
                G.node[k]['url'] =UrlPatent(G.node[k]['label'])[0]

            elif G.node[k]['category'] == "equivalents":
                Visu['color']['a'] = 1
                Visu['color']['r']= int(127)
                Visu['color']['g']= int(127)
                Visu['color']['b']= int(0)
                Visu['shape'] ="ellipse"
                G.node[k]['url'] =UrlPatent(G.node[k]['label'])[0]
            elif G.node[k]['category'] == 'applicant-nice':
                G.node[k]['category'] = 'applicant'# for readable facility
                G.node[k]['url'] = UrlApplicantBuild(G.node[k]['label'])[0]
                Visu['color']['a'] = 1
                Visu['color']['r']= int(127)
                Visu['color']['g']= int(0)
                Visu['color']['b']= int(127)
                Visu['shape'] ="star"
            elif G.node[k]['category'] == 'IPCR1' or G.node[k]['category'] == 'IPCR3' or G.node[k]['category'] == 'IPCR4' or G.node[k]['category'] == 'IPCR7' or G.node[k]['category'] == 'IPCR7' or G.node[k]['category'] == 'CPC':
                G.node[k]['url'] = UrlIPCRBuild(G.node[k]['label'])[0]
                Visu['color']['a'] = 1
                Visu['color']['r']= int(127)
                Visu['color']['g']= int(254)
                Visu['color']['b']= int(127)
                Visu['shape'] ="database"
            elif G.node[k]['category'] == 'inventor-nice':
                G.node[k]['category'] = 'inventor'# for readable facility
                G.node[k]['url'] = UrlInventorBuild(G.node[k]['label'])[0]
                Visu['color']['a'] = 1
                Visu['color']['r']= int(127)
                Visu['color']['g']= int(127)
                Visu['color']['b']= int(254)
                Visu['shape'] ="triangleDown"
            else:
                Visu['color']['a'] = 1
                Visu['color']['r']= int(0)
                Visu['color']['g']= int(0)
                Visu['color']['b']= int(0)
            if "label" not in mixNet:
                mixNet.append('label')
            #factx, facty = 500, 400
            if 'inventor' in G.node[k]['category'] or 'applicant' in G.node[k]['category']:
                categ = G.node[k]['category']+'-nice' # for readable facility
                count = mixNet.index(categ)
            else:
                count = mixNet.index(G.node[k]['category'])
            Visu['position']= {'x':(int(pos[k][0])*factx+posx), 'y':(int(pos[k][1])*facty+posy), 'z':0.0}
            # Visu['size'] = np.log(int(G.node[k]["weight"])+1)+4#
            Visu['color']['a']= count
            G.node[k]['viz'] =dict()


        #            Visu['color']['a']= count

        #        Visu['size'] = (G.node[k]["degree"]*1.0)#(G.node[k]["degree"]*1.0/Maxdegs)*150#(G.node[k]["weight"]) /MaxWeight #addd 1 for viewiong all...
            #Visu['size'] = (G.node[k]["degree"]*zoom) +1 #(G.node[k]["weight"]) /MaxWeight #addd 1 for viewiong all...
            Visu['size'] = G.node[k]["degree"]*10.0/max(G.degree().values()) +4
        #        Visu['size'] = np.log(int(G.node[k]["weight"])+1)*zoom+1#
            for cle in Visu.keys():
                G.node[k]['viz'][cle] = Visu[cle]

         #               print G.node[k]
         #       nx.set_node_attributes(G, 'weight', attr_dict)

        outputFile = ndf+network+prefix+'JS.gexf'

        try:
            os.remove(ResultGephiPath+'/'+outputFile)
        except:
            try:
                os.remove(ResultGephiPath+'/'+outputFile)
            except:
                pass
    #
        nx.write_gexf(G, ResultGephiPath+'/'+outputFile, version='1.2draft')
        fic = open(ResultGephiPath+'/'+outputFile, 'r')

        # Next is a hack to correct the bad writing of the header of the gexf file
        # with dynamics properties
        fictemp=open(ResultGephiPath+'/'+"Good"+outputFile, 'w')


        ecrit = True
        data = fic.read()
        # VERY UGLY Hack here !!!!
        data = data.replace('ns0:', 'viz:') # may be someone knows how to set namespace in networkx...
        data = data.replace('a="None"', '') # may be someone knows why network set the "a" attribute...

        for lig in data.split('\n'):
            if lig.count('<nodes>'):
                ecrit = True
            if ecrit:
                fictemp.write(lig+'\n')
        fictemp.close()
        fic.close()
        try:
            #os.remove(ResultGephiPath+'\\'+ndf+'.gexf')
            os.remove(ResultGephiPath+'/'+outputFile)
        except:
            pass

        os.rename(ResultGephiPath+'/'+"Good"+outputFile, ResultGephiPath+'/'+outputFile)
        print "Network file writen in ",  ResultGephiPath+' directory.\n See file: '+outputFile
        print
        print
        #making the html from model
        RenderTemplate(
            "Graphe.html",
            ResultGephiPath + '/'+outputFile.replace('.gexf','.html'),
            TitleNet=network[1:]+' Network for ' + requete,
            fichierConfigJS=outputFile.replace('.gexf','') +'Conf.js',
            mediaStyle='../../../Patent2Net/media/styles',
            mediaJs='../../../Patent2Net/media/js',
        )

        # making the js from model
        # maybe we could adjust node size and other parameters here
        RenderTemplate(
            "gephiConfig.js",
            ResultGephiPath + '/'+outputFile.replace('.gexf','') +'Conf.js',
            FicRezo=outputFile,
        )
