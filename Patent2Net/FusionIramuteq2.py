# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 07:53:30 2014

@author: dreymond
"""


import os, codecs
from Patent2Net.P2N_Lib import ReturnBoolean, GenereListeFichiers
from Patent2Net.P2N_Lib import LoadBiblioFile, AnnonceProgres
from Patent2Net.P2N_Config import LoadConfig
from zipfile import ZipFile , ZIP_DEFLATED

configFile = LoadConfig()
requete = configFile.requete
ndf = configFile.ndf
Gather = configFile.GatherContent
GatherBiblio = configFile.GatherBiblio
GatherPatent = configFile.GatherPatent
GatherFamilly = configFile.GatherFamilly
FusionIramuteq2 = configFile.FusionIramuteq2
 #should set a working dir one upon a time... done it is temporPath
ResultPath = configFile.ResultBiblioPath
temporPath = configFile.temporPath
ResultContentsPath = configFile.ResultContentsPath

#with open("..//requete.cql", "r") as fic:
#    contenu = fic.readlines()
#    for lig in contenu:
#        #if not lig.startswith('#'):
#            if lig.count('request:')>0:
#                requete=lig.split(':')[1].strip()
#            if lig.count('DataDirectory:')>0:
#                ndf = lig.split(':')[1].strip()
#            if lig.count('FusionIramuteq2')>0:
#                IsEnableScript = ReturnBoolean(lig.split(':')[1].strip())

rep = ndf
ResultListPath = '..//DATA//'+rep+'//PatentBiblios'#Lists'
ResultPathContent = '..//DATA//'+rep+'//PatentContents'
temporPath = '..//DATA//'+rep+'//tempo'
ResultBiblioPath= '..//DATA//'+rep+'//PatentBiblios'



if FusionIramuteq2:
    Rep = '..//DATA//'+ndf+'//PatentContents'
    temporar = GenereListeFichiers(Rep)
    
    #for det in ['FamiliesAbstract']:
    #    ind = 0
    #    for lang in ['FR', 'EN', 'UNK']:
    #        NomResult = lang+'_'+det.replace('Abstract', '') + '_' + ndf.title()+'.txt'
    #        ficRes = open(Rep+'//'+NomResult, "w")
    #        ficRes.write(complete(temporar[ind], lang, det))
    #        ind+=1
    #        ficRes.close()
    #
    #for det in ['Abstract']:
    #    ind = 0
    #    for lang in ['FR', 'EN', 'UNK']:
    #        NomResult = lang+'_'+det.replace('Abstracts', '') + '_' + ndf.title() +'.txt'
    #        ficRes = open(Rep+'//'+NomResult, "w")
    #        ficRes.write(complete2(temporar[ind], lang, det))
    #        ind+=1
    #        ficRes.close()
    num = 0
    consistent = dict()
    for content in ['Abstract', 'Claims', 'Description', 'FamiliesAbstract', 'FamiliesClaims', 'FamiliesDescription' ]: 
        num +=1
        lstfic = os.listdir(ResultPathContent+'//'+content)
        print(len(lstfic), " not so empty", content, " gathered. See ", ResultPathContent + '//'+ content+'// directory for files')
        print('Over the ', len(lstfic),  ' patents...'+ content)
        
        Langues = set()
        for fi in lstfic:
            Langues.add(fi[0:2])
        for ling in Langues:
            cpt =0
            with codecs.open(ResultPathContent+'//'+ling.upper()+ '_'+content +'_' +ndf+'.txt', "w", 'utf8') as ficRes:
                for fi in [fic2 for fic2 in lstfic if fic2.startswith(ling)]:
                    contenuFic = ResultPathContent+ '//'+ content+'//'+fi

                    with codecs.open(contenuFic, 'r', 'utf8') as absFic:
                        data = absFic.readlines()
                        ficRes.write(''.join (data) +'\n')
                        if ling in ['EN', 'FR'] and content in  ['Description', 'Claims']: # memo for all decription and claim (I haven't see a missing pair)
                            tempo = '**** *type_'+ content +' *'
                            if ling in consistent.keys():
                                if fi not in consistent [ling].keys():
                                    consistent [ling][fi] = dict()
                                
                                consistent [ling][fi][content] =  data [0].replace ( '**** *', tempo) + ''.join(data[1:]) + '\n'
                            else:
                                consistent [ling] =  dict ()
                                consistent [ling][fi] = dict()
                                consistent [ling][fi][content] =  data [0].replace ( '**** *', tempo) + ''.join(data[1:]) + '\n'
                        cpt+=1
                        
                
            print(str(cpt) + ' ' + ling + ' ' + content + ' merged') 
        print("Done. use it with whatever you want :-) or IRAMUTEQ. See DATA/"+ndf+"/PatentContents")  
        AnnonceProgres (Appli = 'p2n_iramuteq', valMax = 100, valActu = 50+num*50/6)
    
    lstfic = os.listdir(ResultPathContent+'//Abstract')
    for ling in ['EN', 'FR']:
        if ling in consistent.keys():
            lstToRetreive = [fic2.upper().replace('.TXT', '.txt').replace(ling, ling.lower()) for fic2 in lstfic if fic2.upper().replace('.TXT', '.txt') in consistent [ling].keys()]    
        else:
            lstToRetreive = []
        for fi in lstToRetreive:
            temporary1 = fi.split('-')[0] # lang code
            temporary2 = fi.split('-')[1].split('.')[0] # PatentNumber
            temporary3 = fi.split('-')[1].split('.')[1] # File extension
            contenuFic = ResultPathContent+ '//Abstract//'+temporary1 +'-' + temporary2.upper() + '.' + temporary3
            with codecs.open(contenuFic, 'r', 'utf8') as absFic:
                data = absFic.readlines()
                tempo = '**** *Type_Abstract'+ ' *'
                consistent [ling][fi.replace(ling.lower(), ling)]["Abstract"] =  data [0].replace ( '**** *', tempo) + ''.join(data[1:]) + '\n'
        
    
    if 'Consistent' not in os.listdir(ResultPathContent):
        for ling in ['EN', 'FR'] :

            if ling in consistent.keys():
                os.makedirs(ResultPathContent + '//Consistent//' + ling)
    for ling in consistent.keys() :
        toSave =  [truc for truc in consistent [ling].keys() if len(consistent [ling][truc].keys()) >2] 
        complete =""""""
        for ndf in toSave:
            data = consistent [ling] [ndf]['Abstract']  + consistent [ling] [ndf]['Description'] + consistent [ling] [ndf]['Claims'] 
            complete += data
            with codecs.open (ResultPathContent + '//Consistent//' + ling + '//' +ndf, "w", 'utf8') as ficRes:
                ficRes.write (data)
                         
        with codecs.open (ResultPathContent + '//Consistent//Iram_' + ling + '_' +rep +'.txt', "w", 'utf8') as ficRes:
            ficRes.write (complete)
        with ZipFile(ResultPathContent + '//Consistent//Iram_' + ling + '_' +rep +'.zip','w') as zip:
           zip.write(ResultPathContent + '//Consistent//Iram_' + ling + '_' +rep +'.txt', compress_type = ZIP_DEFLATED)
        #                         # for fi in consistent.keys():
    #     lstfic = os.listdir(ResultPathContent+'//Abstract')
    #     for fi in [fic2 for fic2 in lstfic if fic2.startswith(ling)]:
    #                 contenuFic = ResultPathContent+ '//'+ content+'//'+fi

    #                 with codecs.open(contenuFic, 'r', 'utf8') as absFic:
    #                     data = absFic.read().strip()
AnnonceProgres (Appli = 'p2n_iramuteq', valMax = 100, valActu = 100)