# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

@author: dreymond
"""

import json
import os
import pickle
#import bs4
from Patent2Net.P2N_Lib import UrlInventorBuild, UrlApplicantBuild, UrlIPCRBuild, UrlPatent, LoadBiblioFile, RenderTemplate
from Patent2Net.P2N_Config import LoadConfig

import datetime
aujourd = datetime.date.today()

configFile = LoadConfig()
requete = configFile.requete
ndf = configFile.ndf
Gather = configFile.GatherContent
GatherBiblio = configFile.GatherBiblio
GatherPatent = configFile.GatherPatent
GatherFamilly = configFile.GatherFamilly
IsEnableScript = configFile.FormateExportDataTable

 #should set a working dir one upon a time... done it is temporPath
ListBiblioPath = configFile.ResultBiblioPath
temporPath = configFile.temporPath
ResultPathContent = configFile.ResultPath

GlobalPath = configFile.GlobalPath

import copy
if IsEnableScript:
    # the list of keys for filtering for datatable
    print ('Processing', ndf)
    clesRef = ['label', 'title', 'year','priority-active-indicator',
    'IPCR11', 'kind', 'applicant', 'applicant-old',# following the normalization process
    'applicant-nice', 
    'country', 'inventor', 'inventor-old',
    'inventor-nice',
    'representative', 'IPCR4',
    'IPCR7', "Inventor-Country", "Applicant-Country", "equivalents", "CPC",
    'prior-Date', #'prior-dateDate', # dates of priority claims
    'references',  # the number of refences into the document len(CitP) + len(CitO)
    'Citations',   # the number of citations granted by the document
    'CitedBy',     # the list of docs (patents) cititng this patent
    'CitP',         # the patents cited by this patent
    'CitO'          # the other docs cited by this patent
    ] #"citations"


    if 'Description'+ndf in os.listdir(ListBiblioPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
        dico = LoadBiblioFile(ListBiblioPath, ndf)

    else: #Retrocompatibility
        with open(ListBiblioPath+'//'+ndf, 'r') as data:
            dico = pickle.load(data)

    LstBrevet = dico['brevets']
    if 'requete' in dico:
        requete = dico["requete"]
    if 'number' in dico:
        print("Found ", dico["number"], " patents! Formating to HMTL tables")
    else:
        print("Found ", len(LstBrevet), " patents! Formating to HMTL tables")
    LstExp = []
    LstExp2 = []
    #just for testing las fnction in gathered should deseapear soon

    ##next may need clarifying update

    for brev in LstBrevet:
        #brev = CleanPatent(brev)

        tempo = dict() # this one for DataTable
        tempo2 = dict() #the one for pitable
        countryInv= [] #new field
        countryApp = []
    #    tempo = CleanPatent(brev)
    #    brevet= SeparateCountryField(tempo)
        #cleaning classification
    #    cles = [key for key in brev.keys() if brev[key]==None or brev[key] == [u'None', None] or brev[key] == [None]]
    #    for cle in cles:
    #        if cle=='date':
    #            brev[cle] = unicode(datetime.date.today().year)
    #        elif cle=="dateDate":
    #            brev[cle] = datetime.date.today()
    #        else:
    #            brev[cle] = u''
    
        memo= copy.copy(brev)
        if brev['label'] == "FR2953836":
            pass
        for cle in list(brev.keys()):
            if isinstance(brev[cle], list):
                brev[cle] = [cont for cont in brev[cle] if cont is not None]
                if cle not in ['prior-dateDate', 'dateDate', 'auct', 'auctAppli', 'type', 'typeCollab', 'family lenght','Citations', 'references']:
                    brev[cle] = [cont for cont in brev[cle] if cont.lower() != 'empty' or cont != '' ]
                else:
                    brev[cle] = [cont for cont in brev[cle] if cont != '' ]
            elif brev[cle]  is not None or brev[cle] .lower() != 'empty' or brev[cle]  != '':
                brev[cle] = brev[cle]
        for key in clesRef:
            if key =='inventor' or key =='applicant':
                if isinstance(brev[key], list) and len(brev[key])>1:
                    brev[key] = [thing for thing in brev[key] if thing is not None]
                    tempo[key] = ', '.join(brev[key]).title().strip()
                elif isinstance(brev[key], list) and len(brev[key]) == 1:
                    tempo[key] = brev[key][0].title().strip()
                elif isinstance(brev[key], list) and len(brev[key]) == 0:
                    tempo[key] = ''
                else:
                    tempo[key] = brev[key].title().strip()

            elif key =='title':
                if isinstance(brev[key], list):
                    tempo[key] = str(brev[key]).capitalize().strip()
                else:
                    tempo[key] = brev[key].capitalize().strip()
            else:
                try:
                    if isinstance(brev[key], list) and len(brev[key])>1:
                        try:
                            tempo[key] = ', '.join(brev[key])
                            
                        except:
                            brev[key] = [str(truc) for truc in brev[key]]
                            #☺tempo[key] = ', '.join(brev[key])
                            
                    elif isinstance(brev[key], list) and len(brev[key]) == 1:
                        if brev[key][0] is not None:
                            tempo[key] = brev[key][0]
                        else:
                            tempo[key] = ''
                    elif brev[key] is None:
                        tempo[key] = ''
                    else:
                        tempo[key] = brev[key]
                except:
                    tempo[key] = "0" #hum this is fully arbttrary...
    #   tempo[url]

        tempo['inventor-url'] = UrlInventorBuild(brev['inventor'])
        tempo['applicant-url']= UrlApplicantBuild(brev['applicant'])
        for nb in [1, 3, 4, 7, 11]:
            tempo['IPCR'+str(nb)+'-url']= UrlIPCRBuild(brev['IPCR'+str(nb)])
        
        tempo['equivalents-url'] =  [UrlPatent(lab) for lab in brev['equivalents']]
        tempo['label-url'] = UrlPatent(brev['label'])
        LstExp.append(tempo)
    #    filtering against keys in clesRefs2 for pivottable
    #    tempo2=dict()
    #    clesRef2 = ['label', 'year',  'priority-active-indicator', 'kind', 'applicant', 'country', 'inventor',  'IPCR4', 'IPCR7', "Inventor-Country", "Applicant-Country", 'Citations', u'references', 'CitedBy', ] #'citations','representative',
    #    for ket in clesRef2:
    #        tempo2[ket] = brev[ket] #filtering against clesRef2
    #
    #        if isinstance(brev[ket], list):
    #            tempo2[ket] = UnNest(brev[ket])
    #        else:
    #            tempo2[ket] = brev[ket]

    Exclude = []
    print("entering formating html process")
    dicoRes = dict()
    dicoRes['data'] = LstExp
    contenu = json.dumps(dicoRes, indent = 3) #ensure_ascii=True,
    import pandas as pd
    df = pd.DataFrame(dicoRes["data"])
    df.to_excel(ResultPathContent + '//' +ndf+'.xlsx', sheet_name=ndf)
    compt  = 0
    Dones = []
    Double = dict() #dictionnary to manage multiple bib entries (same authors and date)

    with open(ResultPathContent + '//' +ndf+'.json', 'w') as resFic:
        resFic.write(contenu)
    #outfile =  ndf + '.xlsx'
    
    outfile = ResultPathContent + '//' + ndf + '.html'
    RenderTemplate(
        "Modele.html",
        outfile,
        GlobalPath=GlobalPath,
        fichier=ndf+'.json',
        fichierPivot=ndf+'Pivot.html',
        fichieXls = ndf+".xlsx",
        requete=requete.replace('"', ''),
        CollectName=ndf,
        Request=requete,
        #TotalPatents=totalPatents,
       # TotalFamily=nbFam,
       # HasFamily=GatherFamilly,
       # TotalsPerType=totalsPerType,
       # TotalsPerFamilyType=totalsPerFamilyType
    )

    with open("scriptSearch.js", 'r') as Source:
        js = Source.read()
        js = js.replace('***fichierJson***', ndf+'.json')
        js = js.replace('{ "data": "application-ref"},', '')
        with open(ResultPathContent + '//' + 'scriptSearch.js', 'w') as resFic:
            resFic.write(js)

    #os.system('start firefox -url '+ URLs.replace('//','/') )
