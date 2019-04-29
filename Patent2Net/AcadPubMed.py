# -*- coding: utf-8 -*-
"""
Created on Mon Apr  10 11:26:06 2019

@author: dreymond
"""

#from gargDown_biblio import newCorpus, get_resource_by_name, parse2
import pickle

#import pprint
import codecs
from urllib.parse import urlparse
import os
import requests
import epo_ops
from epo_ops.models import Docdb
from epo_ops.models import Epodoc
from Patent2Net.P2N_Lib import MakeIram2, LoadBiblioFile
from pymed import PubMed
import xmltodict
global key
global secret
pubmed = PubMed(tool="P2N-Acad", email="patent2net@gmail.com")

def getAffiliation(pubmedId, auteur):
    Base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=%s&rettype=fasta&retmode=xml" %(pubmedId)
    reponse = requests.get(Base)
    data = None
    if reponse.status_code == 200:
        data = xmltodict.parse(reponse.text)
        ListeAuteur = data ['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']['AuthorList']
        for Aut in ListeAuteur ['Author']:
            Nom = Aut['LastName'] +' ' + Aut['ForeName']+ ' ' + Aut['Initials']
            if 'AffiliationInfo' in Aut.keys():
                Affiliaton = Aut['AffiliationInfo']
            if auteur.split(' ')[0] in Nom and auteur.split(' ')[1] in Nom:
                if 'AffiliationInfo' in Aut.keys():
                    if 'Affiliation' in Aut['AffiliationInfo'].keys():
                        return Aut['AffiliationInfo']['Affiliation']
                    else:
                        print ('inconsistent')
                else:
                    return Affiliaton['Affiliation'] #if author is the second author in the same structure as primary then the affiliation is not mentioned twice. We use previos.
                # I hope the rule is the same for all the number of authors.
    
    else:
        raise ValueError(reponse.status_code, reponse.reason)
    return data    

def ChercheAbstractBrevet(pat, DirStockage ):
    ndb = pat['label']#[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$']brevet['publication-ref'][u'document-id'][0][u'kind']['$'])
    if isinstance(ndb, list):
        ndb = ndb[0]
    print("Retrieving ", ndb)
    pays = pat['country']

    
    for key in ['label', 'country', 'kind']:
        brevet[key] = list(set(brevet[key])) # hum some problem (again) in cleaning data within the family gatherer... 22/12/15
    if isinstance(pays, list):
        pays = pays[0]
#    for content in ['Abstract']:# , typeSrc+'Claims',typeSrc+'Description']:
        
    content = 'Abstract'
    endP = 'biblio'
#
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
                if dat is not None and dat.ok: 
                    contenu = content

                    patentCont = dat.json()
                    Langs = MakeIram2(brevet, ndb +'.txt', patentCont, DirStockage, contenu)
                    # Make2Iram2 devrait formater le brevet dans un fichier txt au format Iramuteq dans le bon repertoire
                    # Lang est un truc :-) (je crois que cela renvoit la langue de l'abstract récupéré))
    else:
        temp =('publication', Docdb(brevet['label'][2:],brevet['country'], brevet['kind']))
        if data is not None and data.ok:
            contenu = content
            patentCont = data.json()
            Langs = MakeIram2(brevet, ndb +'.txt', patentCont, RepStockage, contenu)
    return patentCont
#
# put your credential from epo client in this file...
# chargement clés de client, utilisé pour récupérer l'abstract du brevet du gugusse retrouvé
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

# La liste des structures adéquates s'appuie sur un fichier dans AcadRessources 
# encodé  en UTF8 avec une affiliation par ligne
#BonneAffiliation= LoadAffiliation('BonnesAffiliations.csv') #['laboratoire', 'institut', "centre de recherche", "université"] #à compléter
# Les champs nécessaires par brevet.
NeededInfo = ['label', 'date', 'inventor', 'title', 'abstract']
ndf = projectName
BiblioPath = configFile.ResultBiblioPath
ResultBiblioPath = configFile.ResultBiblioPath
temporPath = configFile.temporPath
ResultPathContent= configFile.ResultContentsPath
ResultAbstractPath = configFile.ResultAbstractPath
Auteur = configFile.ResultPath + '//AcadCorpora'
RepDir = configFile.ResultPath + '//AcadCorpora'
project = RepDir
if 'AcadCorpora' not in os.listdir(configFile.ResultPath):
    os.makedirs(RepDir)
#Version simple... on ne prends pas les familles
if 'Description'+ndf in os.listdir(BiblioPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
    print( "loading patent biblio data with ", " and ".join(NeededInfo), " fields.")
    DataBrevet = LoadBiblioFile(BiblioPath, ndf)
    print("Hi this is Hal processor. Bibliographic data of ", ndf, " patent universe found.")
else: #Retrocompatibility #Je me demande si c'est utile depuis la V3....
    print("please use Comptatibilizer")
#    for ndf in [fic2 for fic2 in os.listdir(ResultBiblioPath) if fic2.count('Description')==0]:
#        if ndf.startswith('Families'):
#            typeSrc = 'Families'
#        else:
#            typeSrc = ''
#        if ('Description'+ndf in os.listdir(ResultBiblioPath)) or ('Description'+ndf.lower() in os.listdir(ResultBiblioPath)): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
#            ficBrevet = LoadBiblioFile(ResultBiblioPath, ndf)

typeSrc = ''
print("Nice, ", len(DataBrevet["brevets"]), " patents found. On cherche les auteurs...")

NumAut = 0
for brevet in DataBrevet["brevets"]:
    SavBrevet = False # Commutateur pour éviter de requêter 15 fois pour un brevet
    for Auteur in brevet['inventor'] :
        Auteur = Auteur.title()
        NumAut +=1 
        query = "%s[Author - Full]" %(Auteur)
        DocsAuteur = pubmed.query(query, max_results=500)
        IramFull = """"""# le contenu du fichier IRAMUTEQ complet
        for article in DocsAuteur:
        #    print(type(article))
        #    print(article.toJSON())
            Affi = getAffiliation(article.pubmed_id.split('\n')[0], Auteur) # the first pubmed_id is the article. Others are citations
            print (Affi)
            if " france" in Affi.lower():
                RepStockage = RepDir + "//" + Auteur.title().replace(' ', '').replace('"', '') +str(NumAut)
                if "AcadCorpora" not in os.listdir(configFile.ResultPath):
                    os.makedirs(RepDir)
                if Auteur.title().replace(' ', '').replace('"','') +str(NumAut) not in os.listdir(RepDir):
                        try:
                            os.makedirs(RepStockage+"//publis")
                            os.makedirs(RepStockage+"//abstracts")
                        except:
                            pass
                Num = 0 #le numéro de doc pour sauvegarde
                if 'abstract' in article.keys():
                    if not SavBrevet:
                        ChercheAbstractBrevet(brevet, RepStockage )
                        SavBrevet = True
                    
            else:
                
                print ("pas glop", Affi)
                
       
#        ScoreAuteur = 0
#        ListePaysAffiliation = list()  #Les pays de l'affiliation des documents
#                  for document in DocsAuteur['docs']:
#                        if isinstance(document, dict):
#                            if 'abstract_s' in document.keys(): #pas toutes les entréees HAL ont un abstract
#                                Num +=1
#                                if  'producedDate_s' in document.keys():
#                                    Date = document['producedDate_s']
#                                else:
#                                    Date = 1000
#                                if 'title_s' in document.keys():
#                                    Titre =  document['title_s']
#                                else:
#                                    Titre = "Pas de titre"
#                                Entete= "**** *auteur_" + Auteur.title().replace(" ", "").replace('"','') + " *date_"+ str(Date) + '\n'
#                                Contenu =  '\n'.join(document['abstract_s'])
#                                ndf = str(Date) + '-' + str(Num) + '.txt'
#                                # On stocke chaque résumé dans un fichier dans le rep abstract
#                                with codecs.open(RepStockage+ '\\abstracts\\' + ndf, 'w', 'utf8') as fic:
#                                    fic.write(Entete + Contenu)
#                                IramFull += Entete + Contenu + "\n"
#                                
#                    #Pour chaque auteur la somme des titres résumé dans le format Iramuteq
#                    with codecs.open(RepStockage+'\\IRAM' +Auteur.title().replace(' ', '').replace('"','') +str(NumAut)+'.txt', 'w', 'utf8') as fic:
#                        fic.write(IramFull)
#                        
#                    #la suite est adaptée du script de récup des résumés 
#                    #si on a trouvé un match dans scolar, on récupère l'abstract
                        
                                                    
                        #OPS limitation ?
                        #OPS includes character-coded full text only for EP, WO, AT, CH, CA, GB and ES.
                        #http://forums.epo.org/open-patent-services-and-publication-server-web-service/topic3728.html



#                    if data is not None and data.ok:
#                        contenu = content.replace(typeSrc, "")
#
#                        patentCont = data.json()
#                        Langs = MakeIram2(brevet, ndb +'.txt', patentCont, RepDir+ '//'+ typeSrc + contenu+'//', contenu)

#        NumAut = 0 # Numero d'auteurs
#        if len(GoodPotentielAuteur)>0:
#            for auteur in GoodPotentielAuteur:
#                IramFull ="""""" #the complete IramuTeq File
#                NumAut+=1
#                Publis = []
#                # la librairie a seulement téléchargé titre et année dans les ref biblio
#                # on complète
#                for publi in auteur.publications:
#                    Publis.append(publi.fill())
#                    
#                DocsAuteur['docs'][1]['submittedDate_s']
#                if "AcadCorpora" not in os.listdir(configFile.ResultPath):
#                    os.makedirs(RepDir)
#                if Auteur.title().replace(' ', '') +str(NumAut) not in os.listdir(RepDir):
#                    os.makedirs(RepStockage+"\\publis")
#                    os.makedirs(RepStockage+"\\abstracts")
#                Num = 0 # Numero de Publis retrouvées
#                # récupération des publications
#                for pub in Publis:
#                    Num+=1
#                    if 'year' not in pub.bib.keys():
#                        pub.bib['year'] = 1000
#                    if 'title' not in pub.bib.keys():    
#                        pub.bib['title'] = "Titre inconnu"
#                    if 'eprint' in pub.bib.keys():
#                        try:
#                            req = requests.get(pub.bib['eprint'], allow_redirects=True)
#                            #recupération de l'extension de la ressource
#                            pathURl = urlparse(pub.bib['eprint'])
#                            extension = os.path.splitext(pathURl.path)[1]
#                            if extension is None or extension =='': #on force le pdf
#                                extension='.pdf'
#                            # création du nom de la ressource
#                            ndf = pub.bib['title'].title().replace(' ', '')+ '-' + str(pub.bib['year']) + '-' + str(Num) + extension 
#                            with open(RepStockage+ '\\publis\\' + ndf, 'wb') as fic:
#                                fic.write(req.content)
#                        except:
#                            pass
#                    elif 'url' in pub.bib.keys():
#                        #use unpayload here...
#                        pass
#                    else:
#                        pass
#                    if 'abstract' in pub.bib.keys():
#                        #formatage IRAMUTEQ
#                        Entete= "**** *auteur_" + Auteur.replace(" ", "") + " *date_"+ str(pub.bib['year']) + '\n'
#                        Contenu = pub.bib['title'] + '\n' +  pub.bib['abstract'].text
#                        ndf = str(pub.bib['year']) + '-' + str(Num) + '.txt'
#                        # On stocke chaque résumé dans un fichier dans le rep abstract
#                        with codecs.open(RepStockage+ '\\abstracts\\' + ndf, 'w', 'utf8') as fic:
#                            fic.write(Entete + Contenu)
#                        IramFull += Entete + Contenu + "\n"
#                        #Pour chaque auteur la somme des titres résumé dans le format Iramuteq
#                with codecs.open(RepStockage+'\\IRAM' +Auteur.title().replace(' ', '') +str(NumAut)+'.txt', 'w', 'utf8') as fic:
#                    fic.write(IramFull)
#                    
 