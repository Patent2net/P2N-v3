# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 15:23:13 2020
P2N-Indexer
Beta test: need to fix communication way with carrot.
Need also SSE progress bar and process application.
@author: david
"""

import os
import detectlanguage
from elasticsearch import Elasticsearch
import time
from Patent2Net.P2N_Config import LoadConfig
from Patent2Net.P2N_Lib import LoadBiblioFile

try:
    with open('../DetectLanguageAPI.txt', 'r') as detectApiKey:
        detectlanguage.configuration.api_key = detectApiKey.read().strip()
except:
    detectlanguage.configuration.api_key = ""

configFile = LoadConfig()
requete = configFile.requete
ndf = configFile.ndf
Rep = configFile.ResultContentsPath
Bib = configFile.ResultBiblioPath

try:
    if os.getenv('DEBUG'):
        es = Elasticsearch(hosts=[{'host': "127.0.0.1", 'port': 9200}]) # this works only in debug mode
        # elastic is reach by docker inter dns name in the image as below
except:
    es = Elasticsearch(hosts=[{'host': "elasticsearch", 'port': 9200}])


if 'Description' + ndf in os.listdir(
        Bib):  # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
    DataBrevet = LoadBiblioFile(Bib, ndf)
    LstBrevet = DataBrevet['brevets']
elif 'Description' + ndf.title() in os.listdir(
        Bib):  # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
    DataBrevet = LoadBiblioFile(Bib, ndf.title())
    LstBrevet = DataBrevet['brevets']
else:  # Retrocompatibility
    print("please use Comptatibilizer")


def GenereListeFichiers(rep):
    """ prend un dossier en paramètre (chemin absolu) et génère la liste
    complète des fichiers TXT de l'arborescence"""
    listeFicFR = []
    listeFicEN = []
    listeFicUNK = []
    for root, subFolders, files in os.walk(rep):

        if len(subFolders) > 0:
            for sousRep in subFolders:
                temporar = GenereListeFichiers(os.path.normpath(rep + '//' + sousRep))
                listeFicFR.extend(temporar[0])
                listeFicEN.extend(temporar[1])
                listeFicUNK.extend(temporar[2])
        else:
            for fichier in files:
                if fichier.endswith('.txt') and fichier.lower().startswith('fr'):
                    listeFicFR.append(os.path.normpath(root + '//' + fichier))
                elif fichier.endswith('.txt') and fichier.lower().startswith('en'):
                    listeFicEN.append(os.path.normpath(root + '//' + fichier))
                else:
                    if fichier.endswith('.txt'):
                        listeFicUNK.append(os.path.normpath(root + '//' + fichier))

    return (list(set(listeFicFR)), list(set(listeFicEN)), list(set(listeFicUNK)))


# lstAbs = os.listdir(Rep+'//Abstract')
# getting labels from file names
lstAbs = [truc.split('-')[1].replace('.txt', '') for truc in os.listdir(Rep + '//Abstract') if '-' in truc]
lstAbs2 = [truc.replace('.txt', '') for truc in os.listdir(Rep + '//Abstract') if '-' not in truc]
# lstClaims = os.listdir(Rep+'//Claims')
# getting labels from file names
try:
    lstClaims = [truc.split('-')[1].replace('.txt', '') for truc in os.listdir(Rep + '//Claims') if '-' in truc]

    lstClaims2 = [truc.replace('.txt', '') for truc in os.listdir(Rep + '//Claims') if '-' not in truc]
except:
    lstClaims, lstClaims2 = [], []
# lstDesc = os.listdir(Rep+'//Description')
# getting labels from file names
try:
    lstDesc = [truc.split('-')[1].replace('.txt', '') for truc in os.listdir(Rep + '//Description') if '-' in truc]
    lstDesc2 = [truc.replace('.txt', '') for truc in os.listdir(Rep + '//Description') if '-' not in truc]
except:
    lstDesc, lstDesc2 = [], []
cpt = 0
for bre in LstBrevet:  # get patent list from request file
    cpt += 1
    if bre['label'] in lstAbs or bre[
        'label'] in lstAbs2:  # if abstract file exists for that label in PatentContent///Abstract
        fic = []
        for truc in os.listdir(Rep + '//Abstract'):
            if '-' in truc and truc.split('-')[1].replace('.txt', '') == bre['label']:
                fic.append(truc)
            elif truc.replace('.txt', '') == bre['label']:
                fic.append(truc)
            else:
                pass
        if len(fic) == 1:
            with open(Rep + '/Abstract/' + fic[0], 'r', encoding='utf8') as data:
                abstract = data.read()
        elif len(fic) > 1:
            fic = [truc for truc in fic if 'en' in truc]  # using english only
            if len(fic) > 0:
                with open(Rep + '/Abstract/' + fic[0], 'r', encoding='utf8') as data:
                    abstract = data.read()
            else:
                abstract = ''
        else:
            abstract = ''
    else:
        abstract = ''
    if bre['label'] in lstClaims or bre['label'] in lstClaims2:  # if Claims file exists
        # fic = [truc for truc in  os.listdir(Rep+'//Claims') if truc.split('-')[1].replace('.txt', '') == bre ['label']]
        fic = []

        for truc in os.listdir(Rep + '//Claims'):
            if '-' in truc and truc.split('-')[1].replace('.txt', '') == bre['label']:
                fic.append(truc)
            elif truc.replace('.txt', '') == bre['label']:
                fic.append(truc)
            else:
                pass

        if len(fic) == 1:
            with open(Rep + '/Claims/' + fic[0], 'r', encoding='utf8') as data:
                Claims = data.read()
        elif len(fic) > 1:
            fic = [truc for truc in fic if 'en' in truc]  # using english only
            if len(fic) > 0:
                with open(Rep + '/Claims/' + fic[0], 'r') as data:
                    Claims = data.read()
            else:
                Claims = ''
        else:
            Claims = ''
    else:
        Claims = ''
    if bre['label'] in lstDesc or bre['label'] in lstDesc2:  # if Description file exists
        # fic = [truc for truc in  os.listdir(Rep+'//Description') if truc.split('-')[1].replace('.txt', '') == bre ['label']]
        fic = []

        for truc in os.listdir(Rep + '//Description'):
            if '-' in truc and truc.split('-')[1].replace('.txt', '') == bre['label']:
                fic.append(truc)
            elif truc.replace('.txt', '') == bre['label']:
                fic.append(truc)
            else:
                pass
        if len(fic) == 1:
            with open(Rep + '/Description/' + fic[0], 'r', encoding='utf8') as data:
                Description = data.read()
        elif len(fic) > 1:
            fic = [truc for truc in fic if 'en' in truc]  # using english only
            if len(fic) > 0:
                with open(Rep + '/Description/' + fic[0], 'r') as data:
                    Description = data.read()
            else:
                Description = ''
        else:
            Description = ''
    else:
        Description = ''

    doc = {  # indexing a doc field:content
        # hacks should provide other views: citation equivalents or CIB counts... ?
        # I don't know how to do such for the moment
        "lang": "English",  # this is probably false
        'title': bre['title'],
        'abstract': abstract,
        'claims': Claims,
        'description': Description,
        'CitP': bre['CitP'],
        'date': bre['date'],
        'CitedBy': bre['CitedBy'],
        'CitO': bre['CitO'],
        'content': abstract + '\n' + Description + '\n' + Claims
    }
    # flattening contents to make index proper to each value
    listKeys = ['inventor', 'applicant', 'country', 'kind', 'classification']
    for cle in listKeys:
        counter = 0
        for cont in bre[cle]:
            if len(cont) > 0:
                doc[cle + str(counter + 1)] = cont

    res = es.index(index=ndf.lower(), id=cpt, body=doc)
    print(res['result'])

lstFr, lstEn, lstUnk = GenereListeFichiers(Rep)
print()
# making consistent indexes by language
FR = [truc.split('-')[1].replace('.txt', '') for truc in lstFr]  # Labels to match metadata
EN = [truc.split('-')[1].replace('.txt', '') for truc in lstEn]
OT = [truc.split('-')[1].replace('.txt', '') for truc in lstUnk]
cpt = dict()
for bre in LstBrevet:
    doc = {  # indexing a doc field:content
        # hacks should provide other views: citation equivalents or CIB counts... ?
        'title': bre['title'],
        'CitP': bre['CitP'],
        'date': bre['date'],
        'CitedBy': bre['CitedBy'],
        'CitO': bre['CitO']
    }
    listKeys = ['inventor', 'applicant', 'country', 'kind', 'classification', 'IPCR11', 'IPCR1', 'IPCR3', 'IPCR4',
                'IPCR7']
    for cle in listKeys:
        if len(cle) > 0:
            counter = 0
            for cont in bre[cle]:
                if len(cont) > 0:
                    doc[cle + "-" + str(counter + 1)] = cont

    if bre['label'] in FR:
        doc['lang'] = "French"
        indexLang = 'FR-' + ndf.lower()
        Files = [truc for truc in lstFr if
                 bre['label'] == truc.split('-')[1].replace('.txt', "") and "Consistent" not in truc]
        for fil in Files:
            champ = ""
            if "Families" in fil:
                champ = "Families"
            if "Claims" in fil:
                champ += "Claims"
            if "Description" in fil:
                champ += "Description"
            if "Abstract" in fil:
                champ += "Abstract"
            if len(champ) > 0:
                with open(fil, "r", encoding="utf8") as fichier:
                    donnes = fichier.read()
                    if len(donnes.split()) > 5:
                        doc[champ] = donnes
            else:
                print("file ignored ", fil, champ)

    if bre['label'] in EN:
        doc['lang'] = "English"
        indexLang = 'EN-' + ndf.lower()
        Files = [truc for truc in lstEn if
                 bre['label'] == truc.split('-')[1].replace('.txt', "") and "Consistent" not in truc]
        for fil in Files:
            champ = ""
            if "Families" in fil:
                champ = "Families"
            if "Claims" in fil:
                champ += "Claims"
            if "Description" in fil:
                champ += "Description"
            if "Abstract" in fil:
                champ += "Abstract"
            if len(champ) > 0:
                with open(fil, "r", encoding="utf8") as fichier:
                    donnes = fichier.read()
                    if len(donnes.split()) > 5:
                        doc[champ] = donnes
            else:
                print("file ignored ", fil, champ)

    elif bre['label'] in OT:
        file = [truc for truc in lstUnk if
                bre['label'] == truc.split('-')[1].replace('.txt', "") and "Consistent" not in truc][0]
        with open(file, 'r', encoding='utf8') as fichier:
            contenu = fichier.read()
        if len(contenu) > 0:
            phrase = contenu.split('.')[0]
            if len(phrase) > 0 and len(phrase.split()) > 5:  # more than 5 words
                try:
                    lang = detectlanguage.simple_detect(phrase)
                except:
                    time.sleep(2)
                    try:
                        lang = detectlanguage.simple_detect(phrase)
                    except:
                        lang = ''
            else:
                phrase = contenu.split('.')[1]
                try:
                    lang = detectlanguage.simple_detect(phrase)
                except:
                    time.sleep(2)
                    try:
                        lang = detectlanguage.simple_detect(phrase)
                    except:
                        lang = ''
        if len(lang) > 0:
            indexLang = lang.upper() + '-' + ndf.lower()
            doc['lang'] = lang.upper()
        else:
            indexLang = "UNK-" + ndf.lower()
            doc['lang'] = "UNKNOWN"
        Files = [truc for truc in lstUnk if bre['label'] == truc.split('-')[1].replace('.txt', "")]
        for fil in Files:
            champ = ""
            if "Families" in fil:
                champ = "Families"
            if "Claims" in fil:
                champ += "Claims"
            if "Description" in fil:
                champ += "Description"
            if "Abstract" in fil:
                champ += "Abstract"
            if len(champ) > 0:
                with open(fil, "r", encoding="utf8") as fichier:
                    donnes = fichier.read()
                    if len(donnes.split()) > 5:
                        doc[champ] = donnes
            else:
                print("file ignored ", fil, champ)

    if indexLang.split('-')[0] in cpt.keys():
        cpt[indexLang.split('-')[0]] += 1
    else:
        cpt[indexLang.split('-')[0]] = 1

    res = es.index(index=indexLang.lower(), id=cpt[indexLang.split('-')[0]], body=doc)

for lang in cpt.keys():
    print(lang.lower() + "-" + ndf.lower() + ' ' + res['result'] + ' ' + str(cpt[lang]) + ' documents indexed')
