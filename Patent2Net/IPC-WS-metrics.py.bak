# -*- coding: utf-8 -*-
"""
Created on Wed May 24 08:00:33 2017
This script load the xml IPCR descriptions text from Wipo (ipcr-2015.xml) and 
a patent universe from P2N (a list of patent according to a request).
It develops "Augmented Abstracts" consisting of each abstracts completed with
the sum of the first deepers classifications descriptions text (up to the section level) found 
in the patent metadata
@author: dreymond
"""

from lxml import etree
from P2N_Lib import LoadBiblioFile, symbole
from P2N_Config import LoadConfig
import sys, os
configFile = LoadConfig()
requete = configFile.requete
ndf = configFile.ndf
 #should set a working dir one upon a time... done it is temporPath
ResultPath = configFile.ResultBiblioPath
temporPath = configFile.temporPath
ResultContentsPath = configFile.ResultContentsPath
ResultBiblioPath = configFile.ResultBiblioPath
ResultPathContent = '..//DATA//'+ndf+'//PatentContents'

#Setting wether or not we use only primary classification
Primar = True
#Setting cache for performance purposes
CIB = dict()

if 'Description'+ndf or 'Description'+ndf.lower() in os.listdir(ResultBiblioPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
    ficBrevet = LoadBiblioFile(ResultBiblioPath, ndf)

else: #Retrocompatibility
    print 'gather your data again. sorry'
    sys.exit()

if ficBrevet.has_key('brevets'):
    lstBrevet = ficBrevet['brevets']
#        if data.has_key('requete'):
#            DataBrevet['requete'] = data["requete"]
    print "Found  datafile with ", len(lstBrevet), " patents!"
else:
    print 'gather your data again'
    sys.exit()

cles =  ['IPCR11', 'CitO', 'dateDate', 'inventor-nice', 'equivalents', 'CitedBy', 'representative', 'Inventor-Country', 'date', 'inventor', 'kind', 'priority-active-indicator', 'applicant-nice', 'IPCR1', 'country', 'IPCR3', 'applicant', 'IPCR4', 'IPCR7', 'title', 'application-ref']

classe = ['IPCR1',  'IPCR3', 'IPCR4', 'IPCR7','IPCR11']
classe.reverse()


with open('ipcr_2015.xml', 'r') as fic:

    xml = fic.read()
IPCtree = etree.fromstring(xml)
#soup = Soup(xml, "xml")
def ExtractTextFromNode(NodeSchema, IPC):
    """extract text from schema if related to IPC"""
    noeud= NodeSchema
    ancestor = [truc for truc in etree.AncestorsIterator(noeud[0], tag = 'ipcEntry')]
    ancetre = ancestor[len(ancestor)-1]
    for truc in ancetre.iterchildren():
        if truc.tag == 'textBody':
            print truc.text
        elif truc.tag== 'ipcentry':
            if 'symbol' in truc.keys():
                if truc.attrib['symbol'] == IPC:
                    print 'textBody'
        else:
            print
        print truc
    return truc

def GenereListeFichiers(rep):
    """ prend un dossier en paramètre (chemin absolu) et génère la liste
    complète des fichiers TXT de l'arborescence"""
    import os
    listeFicFR = []
    listeFicEN = []
    listeFicUNK = []
    for root, subFolders, files in os.walk(rep):

        if len(subFolders)>0:
            for sousRep in subFolders:
                temporar = GenereListeFichiers(rep+'//'+sousRep)
                listeFicFR.extend(temporar[0])
                listeFicEN.extend(temporar[1])
                listeFicUNK.extend(temporar[2])
        else:
            for fichier in files:
                if fichier.endswith('.txt') and fichier.startswith('fr'):
                    listeFicFR.append(root+'//'+fichier)
                elif fichier.endswith('.txt') and fichier.startswith('en'):
                    listeFicEN.append(root+'//'+fichier)
                else:
                    if fichier.endswith('.txt'):
                        listeFicUNK.append(root+'//'+fichier)
                
    return (list(set(listeFicFR)), list(set(listeFicEN)), list(set(listeFicUNK)))

def GetIPCdef(SchemaIPC, IPCR, CacheCIB):
 #   EntreIPCR = [nn for nn in SchemaIPC.iter() if nn.tag=='ipcEntry' if IPCR in nn.values() or ]
 # should crate a single function that insert all  concerned nodes to extract information from
    EventConcerned =[nn for nn in SchemaIPC.iter() if nn.tag=='ipcEntry' and 'endSymbol' in nn.keys() and 'EN' in nn.values()] 
    #next line works but unused: as far as I could see the notes only concerns CIB readers
    #and do not deliver information on definitions
    Concerned = [nn for nn in EventConcerned if IPCR >= nn.attrib['symbol'] and IPCR < nn.attrib['endSymbol'] ]
    noeud= [nn for nn in SchemaIPC.iter() if nn.tag=='ipcEntry' and IPCR in nn.values() and 'EN' in nn.values()]
    #noeud should be the node of the IPCR
    tct=[]
    for noe in noeud:
        #gettign ârents up to the first (IPCR1)
        tempo = noe.getparent()
        par = []
        while tempo.tag == 'ipcEntry':
            par.append(tempo)
            tempo = tempo.getparent()
        #par must containt all parents
        for node in par: #excluding the section A, B; ...[0:len(par)-1]
            pretexte = [truc for truc in node.iterchildren() if truc.tag == 'textBody'] #description
            for machin in pretexte:
                if machin.tag =='mref':
                            print "alert machin"
                if machin.tag == 'references' or machin.tag=='entryReference':
                    print "refs"
                temporar, temporar2=[], []
               # ExtractTextFromNode(node, IPCR)
                for tit in machin.iterchildren():   
                    if tit.tag =='mref':
                            print "alert ti"
                    for el in tit.iterchildren():
                        if el.tag =='mref':
                            print "alert el"
                        cpt=0
                        app = False
                        for tlepart in el.iterchildren():
                            memo = [tlepart.text, False]
                            if tlepart.tag =='mref':
                                print "alert titll" 
                            cpt+=1
                            if "reference" in tlepart.tag:
                                print "alert"
                            if tlepart.tag=='entryReference':
                                testi = tlepart.getchildren()
                                cpt = 0
                                for sub in testi:
                                    if sub.tag=='sref':
                                        for ref in sub.items():
                                            if IPCR.startswith(ref[1]):
                                                app = True #not sure this isn't useless
                                                
                                               # precision for description text <ref>ipc</ref> the text needed occurs sometimes in the
                                               #precedent tag tail or in the upper tag text: 
                                                   # '<entryReference>separating solids from solids by wet methods <sref ref="B03B"/>, <sref ref="B03D"/>, by pneumatic jigs or tables <sref ref="B03B"/>, by other dry methods <sref ref="B07"/></entryReference>\n
                                                # furthermore, single refs can exeist for one description
                                                
                                                
                                                if cpt == 0 and not memo[1]:
                                                    if memo[0] not in temporar and memo[0].strip() not in temporar:
                                                        temporar.append(memo[0])
                                                    memo[1] = True
#                                                    temporar.append('\n le 1 \n')
                                                elif not memo[1]:
                                                    if memo[0] not in temporar and memo[0].strip() not in temporar:
#                                                    temporar.append('\n le 2 \n')
                                                        temporar.append(memo[0]) # putting previous tail
                                                    memo[1] = True
                                            cpt+=1
                                                #temporar.append('\n le 3 \n')
                                    elif sub.tag=='mref':#case in witch deription text correspond to a range of number... 
                                        # in this case the descrption is added
                                        if IPCR>sub.attrib['ref'] and IPCR<sub.attrib['endRef']:
                                            if tlepart.text not in temporar and tlepart.text.strip() not in temporar :
                                                temporar.append(tlepart.text)
                                            print " Mutltiple refsssss", tlepart.text
                                            print etree.tostring(tlepart)
                                    else: #  hope nbsp tag are threaten anyway
                                        pass
                                    memo= [sub.tail, False]
                                #temporar = [tlepart.text for toto in tlepart.getchildren() if toto.values()==IPCR]
                            if tlepart.tag =='text':
                                if tlepart.text is not None and '\n           'not in tlepart.text:
                                    if tlepart.text not in temporar and tlepart.text.strip() not in temporar :
                                        temporar.append(tlepart.text)
#                                        temporar.append('\n le 7 \n')
                                        
                                
#                            else:
#                                 temporar2.append("\n".join([truc for truc in el.itertext() if '\n    ' not in truc and truc not in temporar2]))
#                print "***************"
#                print temporar
#                print "***************"  
                for chain in temporar:
                    if chain not in tct and chain.strip() not in tct:
                        tct.append(chain)
                #tct.extend(temporar)
            #temporar2.append("\n".join([truc for truc in el.itertext() if '\n    ' not in truc]))
#        tempo3 = [truc for truc in noe.itertext() if '\n    ' not in truc]
#        tct.extend(tempo3)    
        tct.reverse()
#        tct.append('\n'.join([tut for tut in noe.itertext() if '\n           'not in tut]))
#    tct.extend([pipo for pipo in noe.itertext() if '\n                   ' not in pipo])
    #concerned tag aren't trheatened 
#    tct.reverse()
#    if len(Concerned) >0:
#        #seems that concerned do not contain valuable information.
#        for nod in Concerned:
##            temp = [pipo for pipo in nod.itertext() if '\n       ' not in pipo ]
#            for noed in nod.iterchildren():
#                for noed1 in noed.iterchildren():
#                    
#                    if noed1.tag =='':
#                        pass
#            tct.extend(temp)
    res= '\n'.join(tct)
    res = res.lower()
    for sec in ['a,', 'b', 'c', 'd', 'e', 'f', 'g','h']:
        res =res.replace('section '+sec, '')
    CacheCIB [IPCR] = res        
    return res, CacheCIB 
# Call the service 'A61M1/18', '', 'B01D69/08', 'B01D71/38'
#toto = GetIPCdef(IPCtree,symbole('B01D71/38'))
#toto = GetIPCdef(IPCtree,'A63J0015000000')
#
#toto = GetIPCdef(IPCtree,symbole('B01D69/08'))
#for brevet in lstBrevet:
#    it = iter(classe)
#    ClassTxt = ''
#    cur = "current classif level"
##    cpt=0 # index of IPC levels
#    while not len(ClassTxt)>0 or cur == 'IPCR1':
#        
#        cur = it.next()
#        if not isinstance(brevet[cur], list):
#            brevet[cur] = [brevet[cur]]
#        for cla in brevet[cur]:# may be we should use only primary classification
#            if len(cla) >0 and cla != "empty":
#                ClassTxt += GetIPCdef(IPCtree,symbole(cla))
import codecs
Labels= [bre['label'] for bre in lstBrevet]
if True:
    Rep = '..//DATA//'+ndf+'//PatentContents'
    #temporar = GenereListeFichiers(Rep)
    content="Abstract"
    lstfic = os.listdir(ResultContentsPath +'//'+content)
    print "found also ", str(len(lstfic)), " abstracts in english"
cpt = 0
for brevet in lstBrevet:
    
    
    ClassTxt = u''
    cur = "current classif level"
#    cpt=0 # index of IPC levels
    
    if 'en-'+brevet["label"] +'.txt' in lstfic:
        #while not len(ClassTxt)>0 or cur == 'IPCR1':
       
        for cur in classe:
            if bre[cur] is not None and not isinstance(brevet[cur], list):
                brevet[cur] = [brevet[cur]]
            for cla in brevet[cur]:# may be we should use only primary classification
                if len(cla) >0 and cla != "empty":
                    if cla not in CIB.keys():
                        tempora, CIB = GetIPCdef(IPCtree,symbole(cla), CIB)
                    else:
                        tempora = CIB[cla]
                    if tempora not in ClassTxt:
                        ClassTxt += tempora +'\n'
            if len(ClassTxt)>0:
                break # deeper IPCR level is enough
    #for content in ['Abstract']:#, 'Claims', u'Description', 'FamiliesAbstract', 'FamiliesClaims', u'FamiliesDescription' ]: 
        
        #lstfic = os.listdir(ResultContentsPath +'//'+content)
        #print len(lstfic), " not so empty", content, " gathered. See ", ResultPathContent + '//'+ content+'// directory for files'
        #print 'Over the ', len(lstfic),  ' patents...'+ content
        if 'Metrics' not in os.listdir(ResultContentsPath):
            os.mkdir(ResultContentsPath +'//Metrics')
        if 'CIBDesc' not in os.listdir(ResultContentsPath):
            os.mkdir(ResultContentsPath +'//CIBDesc')
        fi = 'en-'+brevet["label"] +'.txt' 
        with codecs.open(ResultContentsPath +'//Metrics//'+fi.replace('.txt','')+'AugCIB.txt', "w", 'utf8') as ficRes:
            
            contenuFic = ResultPathContent+ '//'+ content+'//'+fi
            label = fi[3:len(fi)-4]
            if label in Labels:
                with codecs.open(contenuFic, 'r', 'utf8') as absFic:
                    data = absFic.read().strip()
                    ClassTxt=ClassTxt.lower()
                    ficRes.write(data+ u'\n\n'+ClassTxt)
                    ficRes.write(u'\n')
                    cpt+=1
        with codecs.open(ResultContentsPath +'//CIBDesc//'+fi.replace('.txt','')+'Desc.txt', 'w', 'utf8') as ficDescCib:
                ficDescCib.write(ClassTxt)
                ficDescCib.write('\n')  
with codecs.open(ResultContentsPath +'//ClassementCorpus.txt', 'w', 'utf8') as ficCib:
    for key in CIB.keys():
        ficCib.write(key + '\n') #CIB code is noisy for further process
        ficCib.write(CIB[key])
        ficCib.write('\n')               
print str(cpt) + ' ' + ' abstract and CIB merged' 
print "Done. use it with whatever you want :-) or IRAMUTEQ. See DATA/"+ResultContentsPath +'//Metrics//*.AumentCIB.txt'  
print "See also ", ResultContentsPath +'//ClassementCorpus.txt', " for CIB description used"
  
        
        