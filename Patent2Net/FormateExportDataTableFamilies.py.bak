# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

@author: dreymond
"""

import json
import os
import sys
import cPickle as pickle
#import bs4
from P2N_Lib import UrlInventorBuild, UrlApplicantBuild, UrlIPCRBuild, UrlPatent, LoadBiblioFile, RenderTemplate
from P2N_Config import LoadConfig

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

if IsEnableScript and GatherFamilly:
    rep = ndf.replace('Families', '')
    ndf = 'Families'+ndf
    # the list of keys for filtering for datatable
    clesRef = ['label', 'title', 'year','priority-active-indicator',
    'prior-Date', #'prior-dateDate', # dates of priority claims
    'IPCR11', 'kind', 'applicant', 'country', 'inventor', 'representative', 'IPCR4',
    'IPCR7', "Inventor-Country", "Applicant-Country", "equivalents", "CPC", u'references', u'CitedBy', 'prior', 'family lenght', 'CitO', 'CitP']

    print "\n> Hi! This is DataTable Families formater", ndf
    if 'Description'+ndf in os.listdir(ListBiblioPath):
        with open(ListBiblioPath+'//'+ndf, 'r') as data:
            dico = LoadBiblioFile(ListBiblioPath, ndf)
    else: #Retrocompatibility
        print "please use Comptatibilizer"
        sys.exit()
    LstBrevet = dico['brevets']
    if dico.has_key('requete'):
        requete = dico["requete"]
        print "Using ", ndf," file. Found ", len(dico["brevets"]), " patents! Formating to HMTL tables"

    LstExp = []
    LstExp2 = []
    #just for testing last fnction in gathered should deseapear soon


    for brev in LstBrevet:
        #brev = CleanPatent(brev)

        tempo = dict() # this one for DataTable
        tempo2 = dict() #the one for pitable
        countryInv= [] #new field
        countryApp = []
    #    tempo = CleanPatent(brev)
    #    brevet= SeparateCountryField(tempo)
        #cleaning classification
        for key in brev.keys():
            if isinstance (brev[key], list):
                brev[key] = filter(None, brev[key])  #hum this should be done at the gathering processes
                if "NEANT" in brev[key]:
                    for nb in range(brev[key].count('NEANT')):
                            brev[key].remove('NEANT')
                if "empty" in brev[key]:
                    for nb in range(brev[key].count('empty')):
                            brev[key].remove('empty')
            if brev[key] =='empty':
                brev[key] =''
    #        elif isinstance (brev[key], str) or isinstance (brev[key], unicode):
    #            if "NEANT" in brev[key]:
    #                for nb in range(brev[key].count('NEANT')):
    #                        brev[key].remove('NEANT')
    #            if "empty" in brev[key]:
    #                for nb in range(brev[key].count('empty')):
    #                        brev[key].remove('empty')
            else:
                pass
    #    for cle in cles:
    #        if cle=='date':
    #            brev[cle] = unicode(datetime.date.today().year)
    #        elif cle=="dateDate":
    #            brev[cle] = datetime.date.today()
    #        else:
    #            brev[cle] = u'empty'
        for key in clesRef:
# Issue #6 - by cvanderlei in 3-jan-2017
            if key in brev:
                if key =='inventor' or key =='applicant':
                    if isinstance(brev[key], list) and len(brev[key])>1:
                        brev[key] = [thing for thing in brev[key] if thing is not None]
                        tempo[key] = ', '.join(brev[key]).title().strip()
                    elif isinstance(brev[key], list) and len(brev[key]) == 1:
                        tempo[key] = brev[key][0].title().strip()
                    elif isinstance(brev[key], list) and len(brev[key]) == 0:
                        tempo[key] = u''
                    else:
                        tempo[key] = brev[key].title().strip()

                elif key =='title':
                    if isinstance(brev[key], list):
                        tempo[key] = unicode(brev[key]).capitalize().strip()
                    else:
                        tempo[key] = brev[key].capitalize().strip()
                elif isinstance(brev[key], list) and key=='references':
                    tempo[key] = sum(brev[key])
                elif isinstance(brev[key], list) and key=='priority-active-indicator':
                    tempo[key] = max(brev[key])
                elif isinstance(brev[key], list) and key=='representative':
                    if len(brev[key])==0:
                        tempo[key] = 0
                    else:
                        tempo[key] = max(brev[key])
                elif isinstance(brev[key], list) and key=='family lenght':
                    tempo[key] = max(brev[key])
                else:
                    if isinstance(brev[key], list) and len(brev[key])>1:

                        try:
                            tempo[key] = ', '.join(brev[key])
                        except:
                            print "pas youp ", key, brev[key]
                    elif isinstance(brev[key], list) and len(brev[key]) == 1:
                        if brev[key][0] is not None:
                            tempo[key] = brev[key][0]
                        else:
                            tempo[key] = u''
                    elif brev[key] is None:
                        tempo[key] = u''
                    else:
                        tempo[key] = brev[key]
            else:
                tempo[key] = u''
    #   tempo[url]

        tempo['inventor-url'] = UrlInventorBuild(brev['inventor'])
        tempo[u'applicant-url']= UrlApplicantBuild(brev['applicant'])
        for nb in [1, 3, 4, 7, 11]:
            tempo[u'IPCR'+str(nb)+'-url']= UrlIPCRBuild(brev['IPCR'+str(nb)])

        tempo['equivalents-url'] =  [UrlPatent(lab) for lab in brev['equivalents']]
        tempo['label-url'] = UrlPatent(brev['label'])
        LstExp.append(tempo)
        if 'references' not in tempo.keys():
            print
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
    print "entering formating html process"
    dicoRes = dict()
    dicoRes['data'] = LstExp
    contenu = json.dumps(dicoRes, indent = 3) #ensure_ascii=True,

    compt  = 0
    Dones = []
    Double = dict() #dictionnary to manage multiple bib entries (same authors and date)

    with open(ResultPathContent + '//' +ndf+'.json', 'w') as resFic:
        resFic.write(contenu)

    RenderTemplate(
        "ModeleFamille.html",
        ResultPathContent + '//' + ndf+'.html',
        fichier=ndf+'.json',
        fichierPivot=ndf+'Pivot.html',
        requete=requete.replace('"', '')
    )

    with open("searchScript.js", 'r') as Source:
        js = Source.read()
        js = js.replace('***fichierJson***', ndf+'.json')
        js = js.replace('{ "data": "application-ref"},', '')
        with open(ResultPathContent + '//' + 'searchScript.js', 'w') as resFic:
            resFic.write(js)

    #os.system('start firefox -url '+ URLs.replace('//','/') )
