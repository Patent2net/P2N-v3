# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 07:53:30 2014

@author: dreymond
"""


import os, codecs
from Patent2Net.P2N_Lib import ReturnBoolean, GenereListeFichiers

with open("..//requete.cql", "r") as fic:
    contenu = fic.readlines()
    for lig in contenu:
        #if not lig.startswith('#'):
            if lig.count('request:')>0:
                requete=lig.split(':')[1].strip()
            if lig.count('DataDirectory:')>0:
                ndf = lig.split(':')[1].strip()
            if lig.count('FusionIramuteq2')>0:
                IsEnableScript = ReturnBoolean(lig.split(':')[1].strip())

rep = ndf
ResultListPath = '..//DATA//'+rep+'//PatentBiblios'#Lists'
ResultPathContent = '..//DATA//'+rep+'//PatentContents'
temporPath = '..//DATA//'+rep+'//tempo'
ResultBiblioPath= '..//DATA//'+rep+'//PatentBiblios'



if IsEnableScript:
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
            
    for content in ['Abstract', 'Claims', 'Description', 'FamiliesAbstract', 'FamiliesClaims', 'FamiliesDescription' ]: 
        
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
                        data = absFic.read().strip()
                        ficRes.write(data +'\n')
                        cpt+=1
            print(str(cpt) + ' ' + ling + ' ' + content + ' merged') 
        print("Done. use it with whatever you want :-) or IRAMUTEQ. See DATA/"+ndf+"/PatentContents")  
