# -*- coding: utf-8 -*-
"""
Created on Tue Avr 1 13:41:21 2014
This script will extract the data from biblio file and prepare them for each net.
Parameter of the script specifies the targeted net. Ouputs a graph file.


USE THIS!!!
# import networkx as nx

# df_network = nx.from_pandas_dataframe(df,source='Src', target='Dst', edge_attr=["weight"], create_using=nx.DiGraph())
# nx.write_graphml(df_network,'movement_net_charite.graphml') 




21/02/2019
@author: dreymond
"""
import networkx as nx

#dicot = copy.deepcopy(dict)

import os
import sys
import datetime


from collections import OrderedDict
#from networkx_functs import calculate_degree, calculate_betweenness, calculate_degree_centrality
from lxml import etree

import copy
from Patent2Net.P2N_Lib import flatten, DecoupeOnTheFly, LoadBiblioFile #UrlPatent,UrlApplicantBuild,UrlInventorBuild,UrlIPCRBuild, cmap_discretize
#from P2N_Lib import getStatus2, getClassif,getCitations, getFamilyLenght, isMaj, quote, GenereDateLiens
#from P2N_Lib import  symbole, ReturnBoolean, FormateGephi, GenereListeSansDate, GenereReseaux3, cmap_discretize
#from Ops3 import UnNest2List
from Patent2Net.P2N_Config import LoadConfig

Nets = ["CountryCrossTech", "CrossTech", "InventorsCrossTech", "Applicants_CrossTech", "Inventors",
 "ApplicantInventor", "Applicants", "References", "Citations", "Equivalents"]

if len(sys.argv)<2 or sys.argv[1] not in Nets:
    print("give me a net as parameter, one from this list: ", Nets)
    sys.exit()
else:
    Nets.remove(sys.argv[1])
DureeBrevet = 20
SchemeVersion = '20140101' #for the url to the classification scheme


configFile = LoadConfig()
requete = configFile.requete
projectName = configFile.ndf
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

# should set a working dir one upon a time... done it is temporPath
ResultGephiPath = configFile.ResultGephiPath
BiblioPath = configFile.ResultBiblioPath
temporPath = configFile.temporPath


NeededInfo = ['label', 'date', 'prior-dateDate']
# overloading toi False network creation, these are processed through p2n-NetworkMix script
for net in Nets: #passing other to false, but the script can be called
    Networks["_"+net][0] = False     # and the switch setted to false: the script won't process


def Cleaning(texte): # this is for graphviz. Maybe an ascii converter would be ok....
# Issue #7 - by cvanderlei in 4-jan-2016
    try:
        tempo = texte.replace('empty', '')
        tempo= tempo.replace('Empty', '')
        tempo = tempo.replace('-', '')
        tempo = tempo.replace('&', '')
        tempo = tempo.replace("'", "")
        tempo = tempo.replace('"', "")
    #PY 3... something goes wrong with the code bellow
    # commenting and seeing what appens
#        import curses.ascii
#        try:
#            tutu = [car for car in tempo.encode('ascii', 'ignore') if curses.ascii.isalnum(car) or curses.ascii.isblank(car)]
#        except:
#            tutu = ''  # damn unicode
#        tempo = ''.join(tutu)
        if tempo != '':
            return tempo.strip()
        else:
            return None
    except UnicodeDecodeError:
        return None

prefixes = [""]
if P2NFamilly:
    prefixes.append("Families")

for prefix in prefixes:
    ndf = prefix + projectName
    Category = dict()
    appars = []
    network = "_"+ sys.argv[1]
    mixNet = Networks[network][1]

    if Networks[network][0]:
        ListeBrevet =[]         # patentList
        Patents = set()         # Patents labels
        Nodes = OrderedDict()   # Nodes of the Graph
        Appariement = [] # collaborations for each patent
        dateMini = datetime.date(3000,1,1)
        dateMaxi =  datetime.date(1000,1,1)
        NeededInfo .extend(mixNet)  # list of needed field for building the net
        # may be should use  from
        # from collections import OrderedDict
        # class OrderedNodeGraph(nx.Graph):
        #   node_dict_factory=OrderedDict
        # G = OrderedNodeGraph()
        G1 = nx.MultiDiGraph()        # Multi edges directed network for Gephi
        attr_dict = dict()       # attributes for the net
        # flat net for gexf.js may be it is possible to use previous instead of this one...

        if 'Description'+ndf in os.listdir(BiblioPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
            print(network, ": loading data with ", " and ".join(mixNet), " fields.")
            DataBrevet = LoadBiblioFile(BiblioPath, ndf)
            print("Hi this is Pre-Network processor. Bibliographic data of ", ndf, " patent universe found.")
        else: #Retrocompatibility
            print("please use Comptatibilizer")

        print("Nice, ", len(DataBrevet["brevets"]), " patents found. Pre-formating ", sys.argv[1], " net.")
        for brev in DataBrevet["brevets"]:
                #tempo = pickle.load(fic) # we only memorize needed nfo
            pat = OrderedDict ()
            if "date" not in list(brev.keys()):
                brev['date'] = '1-1-1'
            if isinstance(brev['label'], list):
                brev['label'] = brev['label'][0]
            for key in NeededInfo:

                if key.count('nice')>0 and isinstance(brev[key], list):
                    brev[key] = flatten(brev[key])
                    machin = []
                    for truc in brev[key]:
                        Tt = Cleaning(truc)
                        if Tt is not None and len(Tt)>0:
                            machin.append(Tt)
                    if len(machin)>0:
                        pat[key] = machin  #can you do more ugly ?
                    else:
                        pat[key]= ''

                elif isinstance(brev[key], list):
                    pat[key]= flatten(brev[key])
                    if key.count('Date') ==0:
                       pat[key]= [cont for cont in brev[key] if (cont.lower() not in ['', 'empty', 'none'] or cont !=None)]
                    else:
                       pat[key]= [cont for cont in brev[key] if (cont not in ['', 'empty', 'none'] or cont !=None)]

                elif isinstance (brev[key], str) or isinstance (brev[key], str):
                    pat[key]= Cleaning(brev[key])

                if brev[key] is not None and not isinstance(brev[key], datetime.date):
                    if len(brev[key])>0:
                        pat[key] = brev[key]
                    else:
                        pat[key] =''
                elif brev[key] is not None and isinstance(brev[key], datetime.date):
                    pat[key] = brev[key]
                else:
                    pat[key] =''
            if 'CitO' in list(pat.keys()):
                if pat['CitO'] != '' and pat['CitO'] != []:
                    pat['CitO'] =[thing.replace('\n', ' ') for thing in pat['CitO']]
                    if isinstance(pat['CitO'], list):
                        pat['CitO'] = [Cleaning(truc)[0:14] for truc in pat['CitO'] if Cleaning(truc) is not None]

                    else:
                        pat['CitO'] =Cleaning(pat['CitO'])[0:14]
            tempoBrev = DecoupeOnTheFly(pat, ['prior-dateDate'])
            pattents = [res for res in tempoBrev if res not in ListeBrevet]
            ListeBrevet.extend(pattents)
            if pat['label'] not in Patents:
                Patents.add(pat['label'])

        for lab in Patents:
            temp = []

            for bre in [brev for brev in ListeBrevet if brev['label']==lab]:
                for cat in mixNet:
                    if  (bre[cat],  cat) not in temp :
                        temp.append((bre[cat],  cat))
                        Dates = []
                        tempo = bre['date'].split('-')
                        Dates.append(datetime.date(int(tempo[0]), int(tempo[1]), int(tempo[2] )))
                    else:
                        pass

            if len(temp)>1: # only collaborators in the net
     #               Appariement.append(([noeud[0] for noeud in temp], Dates))
                if lab not in list(Category.keys()):
                    Category[lab] = 'label'
                if network in ["_Citations", "_Equivalents", "_References"]:
                    for ind in range(1, len(temp)):
                        if temp[ind][0] is not None and temp[ind][0] != '' and temp[ind][0].lower() not in ['empty', 'none']:
                            couple =  [Cleaning(temp[0][0]), Cleaning(temp[ind][0])]
                            if couple[0] is not None and couple[1] is not None:
                                appars.append((couple,Dates))
                else:
                    for ind in range(len(temp)-1):
                        if temp[ind][0] is not None and temp[ind][0] != '' and temp[ind][0].lower() not in ['empty', 'none']:
                            if temp[ind+1][0] != lab and temp[ind+1][0] is not None and temp[ind+1][0] != '' and temp[ind+1][0].lower() not in ['empty', 'none']:
                                couple =  [Cleaning(temp[ind][0]), Cleaning(temp[ind+1][0])]
                                if couple[0] is not None and couple[1] is not None:
                                    appars.append((couple,Dates))
                                else:
                                    print(couple)

                for noeud, cat in temp:
                    if noeud is not None and noeud != '' and noeud.lower() != 'empty':
                        if noeud not in Patents:
                            Category[Cleaning(noeud)] = cat
                        else:
                            Category[noeud] = 'label'
                #Building nodes properties

        # CREATING THE WEIGHTED GRAPH
        WeightDyn = dict()
        AtribDynLab = dict()
        for (source, target), datum in appars:
            if source is not None and target is not None: #I don't where those None would come from
                if Category[source] in mixNet and Category[target] in mixNet and source!=target:
                    datum = [ddd for ddd in datum if isinstance(ddd, datetime.date)]

                    if source not in list(Nodes.keys()) and source != '':
                            Nodes[source] = OrderedDict ()
                            Nodes[source]['date'] = datum
                            Nodes[source]['category'] = Category[source]
                            Nodes[source]['label'] = source
                            Nodes[source]['index'] = len(list(Nodes.keys()))-1
                            Nodes[source]['date']= flatten(Nodes[source]['date'])
                    elif datum not in Nodes[source]['date']:
                            Nodes[source]['date'].extend(datum)
                    else:
                            pass
                    if target not in list(Nodes.keys()) and target != '':
                            Nodes[target] = OrderedDict ()
                            Nodes[target]['date'] = datum
                            Nodes[target]['category'] = Category[target]
                            if Nodes[target]['category'] == 'CitO':
                                Nodes[target]['label'] = target[0:14]
                            else:
                                Nodes[target]['label'] = target

                            Nodes[target]['index'] = len(list(Nodes.keys()))-1
                            Nodes[target]['date']= flatten(Nodes[target]['date'])
                    elif datum not in Nodes[target]['date']:
                            Nodes[target]['date'].extend(datum)
                    else:
                            pass
                    indSRC = Nodes[source]['index']
                    indTGT = Nodes[target]['index']
#                    if (indSRC, indTGT) not in list(WeightDyn.keys()):
#                        WeightDyn[(indSRC, indTGT)] = dict()
                    for dat in datum:
                        if isinstance(dat, list):
                                deb = min([dates for dates in dat])
                                fin = max([dates for dates in dat])
                                fin = datetime.date(fin.year+20, fin.month, fin.day)
                        else:
                            deb = min(datum)
                            fin = datetime.date(dat.year+20, dat.month, dat.day) #setting endtime collaboration to 20 year after starting date....
                        if int(fin.year) - int(datetime.date.today().year)>2:
                            fin = datetime.date(int(datetime.date.today().year)+20, 
                                                int(datetime.date.today().month), 
                                                int(datetime.date.today().day))
                        if (indSRC, indTGT) not in WeightDyn.keys():
                            WeightDyn[(indSRC, indTGT)] = dict()
                            tempo = dict()
                            tempo['value'] = 1
                            tempo['start'] = dat.isoformat()
            #                        tempo['start'] = deb.isoformat()
                            tempo['end'] = fin.isoformat()
                            WeightDyn[(indSRC, indTGT)]= [tempo]

                        else:
                            tempo = dict()
                            tempo['value'] = WeightDyn[(indSRC, indTGT)][len(WeightDyn[(indSRC, indTGT)])-1]['value']+1
            #                        
                            tempo['start'] = dat.isoformat()
                            tempo['end'] = fin.isoformat()
                            WeightDyn[(indSRC, indTGT)].append(tempo)
                        attr_dict_lab = dict()
                        attr_dict_weight = dict()
                        if list(Nodes.keys()).index(source) in list(AtribDynLab.keys()):
                            existant =  AtribDynLab[list(Nodes.keys()).index(source)] ['label']['start'].split('-')
                            dateActu = datetime.date (int(existant[0]), int(existant[1]), int(existant[2]))
                            G1deb= min(dat, dateActu).isoformat()
                            existant =  AtribDynLab[list(Nodes.keys()).index(source)] ['label']['end'].split('-')
                            dateActu = datetime.date (int(existant[0]), int(existant[1]), int(existant[2]))
                            G1fin = max(fin, dateActu ).isoformat()
                            G1poids = int(AtribDynLab[list(Nodes.keys()).index(source)] ['weight']['value']) +1
                            attr_dict_lab['label'] = Nodes[source]['label']
                            attr_dict_lab['start'] = G1deb
                            attr_dict_lab['end'] = G1fin
                            attr_dict_weight['value'] =str(G1poids)
                            attr_dict_weight['start'] = G1deb
                            attr_dict_weight['end'] = G1fin
                            AtribDynLab[list(Nodes.keys()).index(source)] ['label'] = copy.copy(attr_dict_lab)
                            AtribDynLab[list(Nodes.keys()).index(source)] ['weight'] = copy.copy(attr_dict_weight)
                        else:
                            G1deb=dat.isoformat()
                            G1fin = fin.isoformat()
                            G1poids = 1
                            attr_dict_lab['label'] = Nodes[source]['label']
                            attr_dict_lab['start'] = G1deb
                            attr_dict_lab['end'] = G1fin
                            attr_dict_weight['value'] =str(G1poids)
                            attr_dict_weight['start'] = G1deb
                            attr_dict_weight['end'] = G1fin
                            AtribDynLab[list(Nodes.keys()).index(source)] = dict()
                            AtribDynLab[list(Nodes.keys()).index(source)] ['label'] = copy.copy(attr_dict_lab)
                            AtribDynLab[list(Nodes.keys()).index(source)] ['weight'] = copy.copy(attr_dict_weight)
                        #setting node properties (target)
                        if list(Nodes.keys()).index(target) in list(AtribDynLab.keys()):
                            existant =  AtribDynLab[list(Nodes.keys()).index(target)] ['label']['start'].split('-')
                            dateActu = datetime.date (int(existant[0]), int(existant[1]), int(existant[2]))
                            G1deb= min(dat, dateActu).isoformat()
                            existant =  AtribDynLab[list(Nodes.keys()).index(target)] ['label']['end'].split('-')
                            dateActu = datetime.date (int(existant[0]), int(existant[1]), int(existant[2]))
                            G1fin = max(fin, dateActu ).isoformat()
                            G1poids = int(AtribDynLab[list(Nodes.keys()).index(target)] ['weight']['value']) +1
                            attr_dict_lab['label'] = Nodes[target]['label']
                            attr_dict_lab['start'] = G1deb
                            attr_dict_lab['end'] = G1fin
                            attr_dict_weight['value'] =str(G1poids)
                            attr_dict_weight['start'] = G1deb
                            attr_dict_weight['end'] = G1fin
                            AtribDynLab[list(Nodes.keys()).index(target)] ['label'] =copy.copy( attr_dict_lab)
                            AtribDynLab[list(Nodes.keys()).index(target)] ['weight'] = copy.copy(attr_dict_weight)
                        else:
                            G1deb=dat.isoformat()
                            G1fin = fin.isoformat()
                            G1poids = 1
                            attr_dict_lab['label'] = Nodes[target]['label']
                            attr_dict_lab['start'] = G1deb
                            attr_dict_lab['end'] = G1fin
                            attr_dict_weight['value'] =str(G1poids)
                            attr_dict_weight['start'] = G1deb
                            attr_dict_weight['end'] = G1fin
                            AtribDynLab[list(Nodes.keys()).index(target)] = dict()
                            AtribDynLab[list(Nodes.keys()).index(target)] ['label'] = copy.copy(attr_dict_lab)
                            AtribDynLab[list(Nodes.keys()).index(target)] ['weight'] = copy.copy(attr_dict_weight)

                        G1.add_node(indSRC)
                        #nx.set_node_attributes(G1[indSRC],, 'label')
                        G1.nodes [indSRC]['label'] =  Nodes[source]['label']
                        #nx.set_node_attributes(G1[indSRC], Nodes[source]['category'], 'category')
                        G1.nodes[indSRC]['category'] = Nodes[source]['category']
                        #G1.add_node(indTGT, attr_dict={'label':Nodes[target]['label'], 'category':Nodes[target]['category']})
                        
                        G1.add_node(indTGT)
                        G1.nodes [indTGT]['label'] =  Nodes[target]['label']
                        #nx.set_node_attributes(G1[indSRC], Nodes[source]['category'], 'category')
                        G1.nodes [indTGT]['category'] = Nodes[target]['category']
#                        nx.set_node_attributes(G1[indTGT], Nodes[target]['label'], 'label')
#                        nx.set_node_attributes(G1[indTGT], Nodes[target]['category'], 'category')
        OtherMEm = list()       
        # this way (in comments) we add edges and the attributes (dynamic)
        # but networks adds them once a time as edge attributes
        # hence only the last one wins in the list of potential attributes for an edge
        # so I just created the edges and parse after the xml gexf produced to
        # insert the attributes (see )
        for ed in WeightDyn.keys():

            if Nodes[AtribDynLab[ed[1]]['label']['label']]['category'] == 'CitedBy':
                for Weight in WeightDyn[ed]:
                    #if (ed[1], ed[0]) in OtherMEm.keys():  
                      #  for cplDat in OtherMEm [(ed[1], ed[0])]:
   
                      num = G1.add_edge(ed[1], ed[0], name = 'CitedBy')
#                      G1.edges[ed[1], ed[0], num]['weight'] ={'value': Weight['value'], 
#                              'start':Weight['start'], 
#                              'end':fin.isoformat() 
#                              }#Weight['end'] #the edge exists ad vitam
                              
                    #if (ed[1], ed[0]) not in OtherMEm.keys():
#                        OtherMEm[(ed[1], ed[0])] = [(Weight['start'], Weight['end'])]
#                    else:
#                        OtherMEm[(ed[1], ed[0])].append((Weight['start'], Weight['end']))
#                        
                # new_attr=WeightDyn[(indSRC, indTGT)])# reverse link for citind the patent
            else:
                for Weight in WeightDyn[ed]:
#                   
                    num = G1.add_edge(ed[0], ed[1], name = 'CitedBy')
#                    G1.edges[ed[0], ed[1], num]['weight'] ={'value': Weight['value'], 
#                              'start':Weight['start'], 
#                              'end':fin.isoformat() 
#                              }
#                    G1.add_edge(ed[0], ed[1],  weight=Weight['value'],
#                              start=Weight['start'], 
#                              end=fin.isoformat()#end=Weight['end']
#                              )# key='CitedBy', new_attr=WeightDyn[(indSRC, indTGT)])#
#                G2.add_edge(indSRC, indTGT, attr_dict)
    #
                #print
                

       # nx.set_edge_attributes( G1, WeightDyn, "weight")
        AtribDyn=OrderedDict()
        Atrib = OrderedDict()
        for noeud in list(AtribDynLab.keys()):
            AtribDyn[noeud] = dict()
            AtribDyn[noeud]['id']= list(AtribDynLab.keys()).index(noeud)
            AtribDyn[noeud]['start']= AtribDynLab[noeud]['label']['start']
            AtribDyn[noeud]['end']= AtribDynLab[noeud]['label']['end']
            AtribDyn[noeud]['label']= AtribDynLab[noeud]['label']['label']
            
       # setting nodes attributes (id, start, end in time format)
        nx.set_node_attributes(G1, AtribDyn)

        nx.write_gpickle(G1, temporPath+'/'+network+prefix)
        
        
        nx.write_gexf(G1, ResultGephiPath+'/test.gexf', version='1.2draft')

#from there its a hack (sometimes ugly) as networkx2.2 doesn't deal correctly with dynamics nets
        with open(ResultGephiPath+'/test.gexf') as fic:
            data = fic.readlines()
        enco = data[0:2]
        temp=data[1:1]
        temp.append("""  <graph defaultedgetype="directed" mode="dynamic" name="" timeformat="date">\n""")
        enco.append("""  <graph defaultedgetype="directed" mode="dynamic" name="" timeformat="date">\n""")
        temp.append("""   <attributes class="edge" mode="static">\n""")
        temp.append("""      <attribute id="1" title="name" type="string" />\n""")
        temp.append("""      </attributes>\n""")
        temp.append("""   <attributes class="edge" mode="dynamic" timeformat="date">\n""" )
        temp.append("""      <attribute id="2" title="weight" type="double" />\n""")
        temp.append("""    </attributes>\n""")
        temp.append("""    <attributes class="node" mode="dynamic" timeformat="date">\n""")
        temp.append("""      <attribute id="0" title="category" type="string" />\n""")
        temp.append("""     </attributes>\n""")
        
        temp.append("""    <meta>\n""")
        temp.append("""      <creator>Patent2Net V3</creator>\n""")
        temp += data[12:]
        data= "".join(temp)
        with open(ResultGephiPath+'/test.gexf', "w") as fic:
            fic.write(enco[1] + data)
        
        with open(ResultGephiPath+'/test.gexf') as fic:
#            don = fic.readlines()
#            data = ''.join(don[1:])
            data=fic.read()
        don = data.splitlines()
        root = etree.fromstring(data.strip())
        nodes = [truc for truc in root.iterdescendants()]
        bords = [truc for truc in don if truc.count('edges')]
        with open(ResultGephiPath+'/HackTest.gexf', 'w') as ficRes:
            ficRes.write("".join(enco))
#            ficRes.write(don[1])
#            ficRes.write(don[2])
            for el  in  nodes:
                if el.tag in ["{http://www.gexf.net/1.2draft}attributes",
                              "{http://www.gexf.net/1.2draft}meta",
                              ]:
                    ficRes.write(str(etree.tostring(el, pretty_print=True, encoding='unicode', method='xml')))
        
                elif  el.tag in ["{http://www.gexf.net/1.2draft}nodes"]:
                    ficRes.write(str(etree.tostring(el, pretty_print=True, encoding='unicode', method='xml')))
                    ficRes.write(bords[0])
                elif el.tag == "{http://www.gexf.net/1.2draft}edge":
                    rac = copy.copy(el)
                    rac.clear()
                    rac.attrib['source']= el.attrib['source']
                    rac.attrib['target'] = el.attrib['target']
                    for attr in el.iterchildren():
                        compt = 0
                        NewAttr=etree.Element(attr.tag)
                        for attrs in attr.iterchildren():
                          #  NewAttrs =etree.Element( attrs.tag)
                            
                            if attrs.attrib['for'] == '2':
                                
                                SRC = int(el.attrib['source'])
                                TGT = int(el.attrib['target'])
                                if (SRC, TGT) in WeightDyn.keys():
                                    for poids in WeightDyn[(SRC, TGT)]:
        
                                        attrs.attrib['value'] = str(poids['value'])
                                        attrs.attrib['start'] = poids['start']
                                        attrs.attrib['end'] = poids['end']
                                        #NewAttrs =etree.Element(attrs)
                                        NewAttr.append(attrs)
                            else:
                                NewAttr.append(attrs)
                        rac.append(NewAttr)
                        ficRes.write(str(etree.tostring( rac, pretty_print=True, encoding='unicode', method='xml')))
                        
            ficRes.write(don[len(don)-3])
            ficRes.write(don[len(don)-2].strip())
            ficRes.write(don[len(don)-1])
        if ndf+network+'.gexf'in os.listdir(ResultGephiPath+'/'):
            os.remove(ResultGephiPath+'/'+ndf+network+'.gexf')
        os.rename(ResultGephiPath+'/HackTest.gexf', ResultGephiPath+'/'+ndf+network+'.gexf')
        os.remove( ResultGephiPath+'/test.gexf')
