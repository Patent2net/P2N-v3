# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

@author: dreymond
"""

import json
import os
import collections
import pickle
import sys
import codecs
from Patent2Net.P2N_Lib import DecoupeOnTheFly, LoadBiblioFile, RenderTemplate # UnNest3#, UrlInventorBuild, UrlApplicantBuild
from Patent2Net.P2N_Config import LoadConfig

import datetime
aujourd = datetime.date.today()

configFile = LoadConfig()
requete = configFile.requete
ndf2 = configFile.ndf
Gather = configFile.GatherContent
GatherBiblio = configFile.GatherBiblio
GatherPatent = configFile.GatherPatent
GatherFamilly = configFile.GatherFamilly
IsEnableScript = configFile.FormateExportPivotTable

 #should set a working dir one upon a time... done it is temporPath
ListBiblioPath = configFile.ResultBiblioPath
ResultListPath = configFile.ResultListPath
ResultPathContent = configFile.ResultPath
temporPath = configFile.temporPath

rep = ndf2

if IsEnableScript:
    # the list of keys for filtering for pivitable
    #clesRef = ['label', 'citations', 'title', 'year','priority-active-indicator',
    #'IPCR11', 'kind', 'applicant', 'country', 'inventor', 'representative', 'IPCR4',
    #'IPCR7', "Inventor-Country", "Applicant-Country",  "CPC", 'Citations', 'references'] # "equivalents", "CitedBy"
    clesRef = ['label', 'title', 'year','priority-active-indicator',
    'IPCR11', 'kind', 'applicant', 'country', 'inventor', 'representative', 'IPCR4',
    'IPCR7', "Inventor-Country", "Applicant-Country", #"equivalents", "CPC",
    'references',  # the number of refences into the document len(CitP) + len(CitO)
    'Citations',   # the number of citations granted by the document
    #u'CitedBy',     # the list of docs (patents) cititng this patent
    #'CitP',         # the patents cited by this patent
    #'CitO'          # the other docs cited by this patent
    ] #"citations"

    #filterFile = [fi for fi in os.listdir(ListBiblioPath) if fi.count('Expanded')]
    srcFile = [fi.replace('Description', '') for fi in os.listdir(ListBiblioPath)]

    for ndf in set(srcFile):
        if 'Description'+ndf in os.listdir(ListBiblioPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
            DataBrevet = LoadBiblioFile(ListBiblioPath, ndf)
            print("\n> Hi! This is FormateExportPivotTable")
        else: #Retrocompatibility... prévious test is ugly: there is an issue with filename in lowercase (sometimes)
            print("please use Comptatibilizer")
            DataBrevet = LoadBiblioFile(ListBiblioPath, ndf) #so I try to laod it....

        if isinstance(DataBrevet, collections.Mapping):
            #data = DataBrevet
            LstBrevet = DataBrevet['brevets']
            if 'number' in DataBrevet:
                print("Found ", DataBrevet["number"], " patents! Formating into HMTL Pivot tables")
            else:
                print("Found ", len(DataBrevet["brevets"]), " patents! Trying to format into HMTL Pivot tables")
        else:
            print("Please delete you data directory... incompatible old stuff in it")
            print("or try Comptatibilizer before")
        LstExp = []
        LstExp2 = []
        #just for testing las fnction in gathered should deseapear soon
        if ndf.count('Families')>0:
        #clesRef2 = ['label', 'year',  'priority-active-indicator', 'kind', 'applicant', 'country', 'inventor',  "CPC", 'IPCR4', 'IPCR7', "Inventor-Country", "Applicant-Country", 'Citations'] #'citations','representative',
            clesRef2 = ['label', 'year',#'priority-active-indicator',
            'prior-Date', 'family lenght',
             'kind', 'applicant', 'country', 'inventor', 'representative',  'IPCR4', #"equivalents","CPC",
            'IPCR7', "Inventor-Country", "Applicant-Country",
         #   u'references',  # the number of refences into the document len(CitP) + len(CitO)
          #  u'Citations',   # the number of citations granted by the document
            #u'CitedBy',     # the list of docs (patents) cititng this patent
            #'CitP',         # the patents cited by this patent
            #'CitO'          # the other docs cited by this patent
            ] #"citations"
        else:
            clesRef2 = ['label', 'year',#'priority-active-indicator',
        'prior-Date',
         'kind', 'applicant', 'country', 'inventor', 'representative', 'IPCR4', # "CPC", "equivalents", excluded du to explosing amount of monovaluated entries
        'IPCR7', "Inventor-Country", "Applicant-Country",
       #u'references',  # the number of refences into the document len(CitP) + len(CitO)
        #u'Citations',   # the number of citations granted by the document
        #u'CitedBy',     # the list of docs (patents) cititng this patent
        #'CitP',         # the patents cited by this patent
        #'CitO'          # the other docs cited by this patent
        ] #"citations"
        compt = 0
        LstExp2 = []
        for brev in LstBrevet:
        #    filtering against keys in clesRefs2 for pivottable
            compt+=1
            tempo2=dict()
            for ket in clesRef2:
# Issue #6 - by cvanderlei in 2-jan-2017
                if ket in brev:
                    tempo2[ket] = brev[ket] #filtering against clesRef2
                    if ket =="Citations": #special filter... I missed something somewhere
                        if isinstance(brev[ket], list):
                            if "empty" in brev[ket] or "Empty" in brev[ket]:
                                tempo2[ket] = 0
                            else:
                                print(tempo2[ket])
                        elif isinstance(brev[ket], str) or isinstance(brev[ket], str):
                                if brev[ket].lower() =='empty' or brev[ket] == '':
                                    tempo2[ket] = 0
                        else:
                            pass
                    elif isinstance(brev[ket], list) and ket=='references':
                        tempo2[ket] = sum(brev[ket])
                    elif isinstance(brev[ket], list) and ket=='priority-active-indicator':
                        tempo2[ket] = max(brev[ket])
                    elif isinstance(brev[ket], list) and ket=='representative':
                        if len(brev[ket])==0:
                            tempo2[ket] = 0
                        else:
                            tempo2[ket] = max(brev[ket])
                    elif isinstance(brev[ket], list) and ket=='family lenght':
                        tempo2[ket] = max(brev[ket])
                    else:
                        pass
                else:
                    tempo2[ket] = 0
    #        print compt
            #next function will split each patent wich as multivaluated entries in a list of patents for each multivaluated one (hope its clear :-) )
            tempoBrev = DecoupeOnTheFly(tempo2, [])
            LstExp2.extend([res for res in tempoBrev if res not in LstExp2])
    #        for thing in pat:
    #            LstExp2.append(byteify(thing))
    #        try:
    #            contenu2 = json.dumps(LstExp2,  indent = 3) #,
    #        except:
    #            print "error, compt=", compt
    #            contenu2 = json.dumps(LstExp2,  indent = 3, ensure_ascii=True) #,

        print("Expanded to ", len(LstExp2), " lines with monomavue colums")
    #    with open(ListBiblioPath + '//Expanded' + ndf, 'w') as SavFic:
    #        pickle.dump(LstExp2, SavFic) if "Families" not in ndf:

    #    Exclude = []
        print("entering formating html process")
    #    dicoRes = dict()
    #    dicoRes['data'] = LstExp
        #contenu = json.dumps(dicoRes, indent = 3) #ensure_ascii=True,

    # just create the file
        contenu2=""
        with codecs.open(ResultPathContent + '//' + ndf+'Pivot.json', 'w', "utf8") as resFic:
            # encode and append line by line to avoid memory error
            try:
                resFic.write(contenu2)
                for contenu2 in json.JSONEncoder(indent = 3).iterencode(LstExp2):
                    #with codecs.open(ResultPathContent + '//' + ndf+'Pivot.json', 'a', "utf8") as resFic:
                    resFic.write(contenu2)

            except:
                resFic.write(contenu2)
                contenu2 = json.dumps(LstExp2,  indent = 3, ensure_ascii=False, encoding='utf8') #,
                #with codecs.open(ResultPathContent + '//' + ndf+'Pivot.json', 'w', "utf8") as resFic:
                resFic.write(contenu2)

        FichierHtml=ndf+'.html'
        if ndf.startswith('Families'):
            ModelePivot = "ModeleFamillePivot.html"
        else:
            ModelePivot = "Pivot.html"
        RenderTemplate(
            ModelePivot,
            ResultPathContent + '//' + ndf+'Pivot.html',
            fichier=ndf+'Pivot.json',
            requete=DataBrevet['requete'].replace('"', ''),
            FichierHtml=FichierHtml,
            FichierHtmlFamille='Families'+FichierHtml
        )

    #os.system('start firefox -url '+ URLs.replace('//','/') )
