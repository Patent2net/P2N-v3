# -*- coding: utf-8 -*-
"""
Created on Mon Apr  10 11:26:06 2019

@author: dreymond
"""

from gargDown_biblio import newCorpus, get_resource_by_name, parse2
import pickle

#import pprint
import codecs
from urllib.parse import urlparse

import requests
import epo_ops
from epo_ops.models import Docdb
from epo_ops.models import Epodoc
from Patent2Net.P2N_Lib import MakeIram2, LoadBiblioFile


global key
global secret

# put your credential from epo client in this file...
# chargement clés de client
fic = open('../cles-epo.txt', 'r')
key, secret = fic.read().split(',')
key, secret = key.strip(), secret.strip()
fic.close()

ops_client = epo_ops.Client(key, secret)
ops_client.accept_type = 'application/json'
    
PotentielAuteurs = list()

from Patent2Net.P2N_Lib import flatten, DecoupeOnTheFly, RenderTemplate, \
                         UrlPatent,UrlApplicantBuild,\
                        UrlInventorBuild,UrlIPCRBuild#, cmap_discretize
from Patent2Net.P2N_Config import LoadConfig
configFile = LoadConfig()

requete = configFile.requete
projectName = configFile.ndf
#prefixes = [""]
#if P2NFamilly:
#    prefixes.append("Families")
    
NeededInfo = ['label', 'date', 'inventor', 'title', 'abstract']
ndf = projectName
BiblioPath = configFile.ResultBiblioPath
ResultBiblioPath = configFile.ResultBiblioPath
temporPath = configFile.temporPath
ResultPathContent= configFile.ResultContentsPath
ResultAbstractPath = configFile.ResultAbstractPath
Auteur = configFile.ResultPath + '\AcadCorpora'
RepDir = configFile.ResultPath + '\AcadCorpora'
project = RepDir
if 'AcadCorpora' not in os.listdir(configFile.ResultPath):
    os.makedirs(RepDir)
#Version simple... on ne prends pas les familles
if 'Description'+ndf in os.listdir(BiblioPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
    print( "loading patent biblio data with ", " and ".join(NeededInfo), " fields.")
    DataBrevet = LoadBiblioFile(BiblioPath, ndf)
    print("Hi this is Scholar processor. Bibliographic data of ", ndf, " patent universe found.")
else: #Retrocompatibility #Je me demande si c'est utile depuis la V3....
    print("please use Comptatibilizer")
#    for ndf in [fic2 for fic2 in os.listdir(ResultBiblioPath) if fic2.count('Description')==0]:
#        if ndf.startswith('Families'):
#            typeSrc = 'Families'
#        else:
#            typeSrc = ''
#        if ('Description'+ndf in os.listdir(ResultBiblioPath)) or ('Description'+ndf.lower() in os.listdir(ResultBiblioPath)): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
#            ficBrevet = LoadBiblioFile(ResultBiblioPath, ndf)
def SearchAuthorHal(aut):
    class Dummy(object):
        pass

    request = Dummy()
    request.method = 'POST'
    request.path = 'nowhere'
    request.META = {}
    # XXX 'string' only have effect on moissonneurs.pubmed; its value is added
    #     when processing request client-side, take a deep breath and see
    #     templates/projects/project.html for more details.
    request.POST = {'string': name,
                    'query': query,
                    'N': QUERY_SIZE_N_MAX}
    
typeSrc = ''
print("Nice, ", len(DataBrevet["brevets"]), " patents found. On cherche les auteurs...")
for brevet in DataBrevet["brevets"]:
    for Auteur in brevet['inventor'] :
        Auteur = 'David Reymond'
        Auteur = Auteur.title()
        corpus = dict()
        corpus['name'] = 'HAL (english) [API]' #conforme aux déclarations de constants.py
        corpus['fileName'] = Auteur #Adapter à la requete
        corpus['ressources'] = get_resource_by_name(corpus['name'] )
        corpus['path'] = newCorpus(project, source="hal", name=Auteur, query='authFullName_s:%s&fl=label_s,abstract_s,docid,keyword_s,authEmailDomain_s,deptStructCountry_s' %(Auteur))
        #sans les facettes: https://api.archives-ouvertes.fr/search/?q=authFullName_s:%22David%20Reymond%22&&fl=label_s,abstract_s,docid,keyword_s,authEmailDomain_s
        #avec : https://api.archives-ouvertes.fr/search/?q=authFullName_s:%22David%20Reymond%22&facet=true&facet.field=abstract_s&facet.field=keyword_s&facet.field=authEmailDomain_s&facet.limit=5
        if corpus['path']  is not None:
            parse2(corpus)
        else:
            pass # rien dans HAL
        RepResult = "AcadCheck"
        try:
            PotentielAuteurs.append( next(res).fill())
        except:
            break
        Continue = True
        while Continue and PotentielAuteurs[0] is not None:
            try:
                PotentielAuteurs.append( next(res).fill())
            except:
                Continue = False
        #pprint.pprint(PotentielAuteurs)
        
        # PotentielAuteurs Contient la liste des homonymes (approximatifs Reymond, Raymond sont collectés)
        
        # Extractions selon affiliation
        
        BonneAffiliation=['laboratoire', 'france', "centre", "université"]
        
        GoodPotentielAuteur = [aut for aut in PotentielAuteurs for aff in BonneAffiliation if aff in aut.affiliation.lower()]
        
        #Au cas où on rajoute les email en .fr
        #peut-être qu'il faudra rajouter la présence de "univ"
        GoodPotentielAuteur.extend([aut for aut in PotentielAuteurs 
                                    if aut not in GoodPotentielAuteur and aut.email.endswith('fr')])
        
        
        NumAut = 0 # Numero d'auteurs
        if len(GoodPotentielAuteur)>0:
            for auteur in GoodPotentielAuteur:
                IramFull ="""""" #the complete IramuTeq File
                NumAut+=1
                Publis = []
                # la librairie a seulement téléchargé titre et année dans les ref biblio
                # on complète
                for publi in auteur.publications:
                    Publis.append(publi.fill())
                    
                RepStockage = RepDir + "\\" + Auteur.title().replace(' ', '') +str(NumAut)  
                if "AcadCorpora" not in os.listdir(configFile.ResultPath):
                    os.makedirs(RepDir)
                if Auteur.title().replace(' ', '') +str(NumAut) not in os.listdir(RepDir):
                    os.makedirs(RepStockage+"\\publis")
                    os.makedirs(RepStockage+"\\abstracts")
                Num = 0 # Numero de Publis retrouvées
                # récupération des publications
                for pub in Publis:
                    Num+=1
                    if 'year' not in pub.bib.keys():
                        pub.bib['year'] = 1000
                    if 'title' not in pub.bib.keys():    
                        pub.bib['title'] = "Titre inconnu"
                    if 'eprint' in pub.bib.keys():
                        try:
                            req = requests.get(pub.bib['eprint'], allow_redirects=True)
                            #recupération de l'extension de la ressource
                            pathURl = urlparse(pub.bib['eprint'])
                            extension = os.path.splitext(pathURl.path)[1]
                            if extension is None or extension =='': #on force le pdf
                                extension='.pdf'
                            # création du nom de la ressource
                            ndf = pub.bib['title'].title().replace(' ', '')+ '-' + str(pub.bib['year']) + '-' + str(Num) + extension 
                            with open(RepStockage+ '\\publis\\' + ndf, 'wb') as fic:
                                fic.write(req.content)
                        except:
                            pass
                    elif 'url' in pub.bib.keys():
                        #use unpayload here...
                        pass
                    else:
                        pass
                    if 'abstract' in pub.bib.keys():
                        #formatage IRAMUTEQ
                        Entete= "**** *auteur_" + Auteur.replace(" ", "") + " *date_"+ str(pub.bib['year']) + '\n'
                        Contenu = pub.bib['title'] + '\n' +  pub.bib['abstract'].text
                        ndf = str(pub.bib['year']) + '-' + str(Num) + '.txt'
                        # On stocke chaque résumé dans un fichier dans le rep abstract
                        with codecs.open(RepStockage+ '\\abstracts\\' + ndf, 'w', 'utf8') as fic:
                            fic.write(Entete + Contenu)
                        IramFull += Entete + Contenu + "\n"
                        #Pour chaque auteur la somme des titres résumé dans le format Iramuteq
                with codecs.open(RepStockage+'\\IRAM' +Auteur.title().replace(' ', '') +str(NumAut)+'.txt', 'w', 'utf8') as fic:
                    fic.write(IramFull)
                    
                #la suite est adaptée du scropt de récup des résumés 
                #si on a trouvé un match dans scolar, on récupère l'abstract
                
            ndb = brevet['label']#[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$']brevet['publication-ref'][u'document-id'][0][u'kind']['$'])
            print("Retrieving ", ndb)
    #check for already gathered patents
            pays = brevet['country']
            if isinstance(ndb, list):
                print(ndb, "using first one...")
                ndb = ndb[0]
                for key in ['label', 'country', 'kind']:
                    brevet[key] = list(set(brevet[key])) # hum some problem (again) in cleaning data within the family gatherer... 22/12/15
            if isinstance(pays, list):
                pays = pays[0]
            for content in [typeSrc+'Abstract']:# , typeSrc+'Claims',typeSrc+'Description']:

                try:
                    lstfic = os.listdir(ResultPathContent+'//' + content)
                except:
                    lstfic = []
                endP= content.replace(typeSrc, "").lower()
                if endP == 'abstract':
                    endP = 'biblio'
                fichier = [fics[3:] for fics in lstfic]   # content already gathered
                if ndb+'.txt' not in fichier: #hack here as chinese patents seems not be in claims or description endpoint
                #, u'fulltext'
                    temp =('publication', Epodoc(pays+ndb[2:])) #, brevet[u'document-id'][u'kind']['$']))
                    try:
                        data = ops_client.published_data(*temp, endpoint = endP)             #ops_client.published_data()
                        if data.ok and content.replace(typeSrc, "").lower() in str(data.json()):
                            CheckDocDB = False
                        else:
                            CheckDocDB = True
                    except Exception as err:
                        CheckDocDB = True
                    if CheckDocDB:
                        if isinstance(brevet['kind'], list):
                            tempoData = []
                            for cc in brevet['kind']:
                                temp =('publication', Docdb(ndb[2:],pays, cc)) # hope all comes from same country
                                try:
                                    tempoData.append(ops_client.published_data(*temp, endpoint = endP))
                                except:
                                    data = None
                                    pass
                            for dat in tempoData:
                                if dat is not None and dat.ok: #doing the same for all content. This may result in redundancy
                                    contenu = content.replace(typeSrc, "")

                                    patentCont = dat.json()
                                    Langs = MakeIram2(brevet, ndb +'.txt', patentCont, RepDir+ '//'+ typeSrc + contenu+'//', contenu)
                                    if endP == 'biblio':
                                        for contenu in ['Claims', 'Description']:
                                            Langs = MakeIram2(brevet, ndb +'.txt', patentCont, RepDir+ '//'+ typeSrc + contenu+'//', contenu)
                        else:
                            temp =('publication', Docdb(brevet['label'][2:],brevet['country'], brevet['kind']))
                            try:
                                data = ops_client.published_data(*temp, endpoint = endP)
                            except:
                                data = None
                                pass
                        #OPS limitation ?
                        #OPS includes character-coded full text only for EP, WO, AT, CH, CA, GB and ES.
                        #http://forums.epo.org/open-patent-services-and-publication-server-web-service/topic3728.html



                    if data is not None and data.ok:
                        contenu = content.replace(typeSrc, "")

                        patentCont = data.json()
                        Langs = MakeIram2(brevet, ndb +'.txt', patentCont, RepDir+ '//'+ typeSrc + contenu+'//', contenu)
