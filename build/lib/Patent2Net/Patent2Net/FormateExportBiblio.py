# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

@author: dreymond
"""

import json

import pickle
import os
import codecs

#import bs4
from Patent2Net.P2N_Lib import LoadBiblioFile, Decoupe, UnNest3, UrlInventorBuild, UrlApplicantBuild, UrlIPCRBuild
from Patent2Net.P2N_Config import LoadConfig

import datetime
aujourd = datetime.date.today()

configFile = LoadConfig()
requete = configFile.requete
ndf = configFile.ndf
Gather = configFile.GatherContent
GatherBiblio = configFile.GatherBiblio
GatherPatent = configFile.GatherPatent
IsEnableScript = configFile.FormateExportBiblio
GatherFamilly = configFile.GatherFamilly

ListBiblioPath = configFile.ResultBiblioPath
ResultPathContent = configFile.ResultPath
temporPath = configFile.temporPath


if IsEnableScript:
    # the list of keys for filtering for datatable
    clesRef = ['label', 'title', 'year','priority-active-indicator',
    'IPCR11', 'kind', 'applicant', 'country', 'inventor', 'representative', 'IPCR4',
    'IPCR7', "Inventor-Country", "Applicant-Country", "equivalents", "CPC", 'references', 'Citations', 'CitedBy']

    prefixes = [""]
    if GatherFamilly:
        prefixes.append("Families")

    for prefix in prefixes:
        ndf = prefix + configFile.ndf

        if 'Description'+ndf in os.listdir(ListBiblioPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
            LstBrevet = LoadBiblioFile(ListBiblioPath, ndf)
            with open(ListBiblioPath +'//Description'+ndf, 'rb') as ficRes:
                DataBrevet = pickle.load(ficRes)
        else: #Retrocompatibility
            with open(ListBiblioPath+'//'+ndf, 'rb') as data:
                LstBrevet = pickle.load(data)

        ##next may need clarifying update

        data = LstBrevet
        LstBrevet = data['brevets']
        if 'requete' in data:
            requete = data["requete"]
        if 'number' in data:
            print("Found ", data["number"], " patents! Formating to HMTL tables")

        LstExp = []

        compt  = 0
        Dones = []
        Double = dict() #dictionnary to manage multiple bib entries (same authors and date)
        with codecs.open(ResultPathContent + '//'  +ndf+'.bib', 'w', 'utf-8') as resFic:
            cleBib = ['year', 'kind', 'title', 'inventor', 'IPCR11', 'label', 'country']
            for bre in LstBrevet:
                if len(cleBib) == len([cle for cle in cleBib if cle in list(bre.keys())]):
                    Gogo = True #checkin consistency
        #==============================================================================
        #            for cle in cleBib:
                   # some cleaning in old version of gathered. Should be ok in V2
        #                 Gogo = Gogo * (bre[cle] is not None)
        #                 Gogo = Gogo * (u'None' not in bre[cle])
        #                 Gogo = Gogo * ( bre[cle] != u'')
        #==============================================================================
                    if Gogo>0:
                        if "A" in ' '.join(bre['kind']) or "B" in ' '.join(bre['kind']) or "C" in ' '.join(bre['kind']): #filter patent list again their status... only published
                            if bre['dateDate'] is not None or bre['dateDate'] != 'None' or bre['dateDate'] != '' or 'None' not in bre['dateDate'] or None in bre['dateDate']:
                                if len(bre['year'])>0 and not isinstance(bre['date'], list):
                                    teatime=bre['date'].split('-')
                                    bre['dateDate'] = datetime.date(int(teatime[0]), int(teatime[1]), int(teatime[2]))
                                elif len(bre['year'])>0:
                                    teatime=bre['date'][0].split('-')
                                    bre['dateDate'] = datetime.date(int(teatime[0]), int(teatime[1]), int(teatime[2]))

        #                        # hum last test prooves that they is a bug in collector for dateDate field
                            if isinstance(bre['dateDate'], list):
                                Date = bre['dateDate'][0] #first publication (hope so)
                            else:
                                Date = bre['dateDate']
        #                    else:
        #                        if isinstance(bre['year'], list):
        #                            temp= bre['year'][0] #first publication
        #                            temp = temp.split('-')
        #                            Date = datetime.date(int(temp[0]), int(temp[1]), int(temp[2]))
        #                        else:
        #                            temp = bre['year']
        #                            temp = temp.split('-')
        #                            Date = datetime.date(int(temp[0]), int(temp[1]), int(temp[2]))

                            if isinstance(bre['inventor'], list):
                                try:
                                    entryName=bre['inventor'][0].split(' ')[0]+'etAl'+str(Date.year)
                                except:
                                    print()
                                tempolist = [nom.replace(' ', ', ', 1).title() for nom in bre['inventor']]
    # Issue #7 - by cvanderlei in 4-jan-2016
                                try:
                                    Authors = str(' and '.join(tempolist))
                                except UnicodeDecodeError:
                                    Authors = ''
                            else:
                                entryName=bre['inventor'].split(' ')[0]+'etAl'+str(Date.year)
                                Authors = bre['inventor'].replace(' ', ', ', 1).title()
                            entryName = entryName.replace("'", "")
                            if entryName in Dones:
                                if entryName in Double:
                                    Double[entryName] += 1
                                else:
                                    Double[entryName] = 1
                                entryName+=str(Double[entryName])
                            if isinstance(bre['country'], list):
                                if len(bre['country']) ==1:
                                    bre['country'] = bre['country'][0]
                            Dones.append(entryName)
    # Issue #6 - by cvanderlei in 6-jan-2017
                            try:
                                resFic.write('@Patent{'+entryName+',\n')
                            except UnicodeDecodeError:
                                resFic.write('@Patent{""\n')
                            resFic.write('\t author={' + Authors + '},\n')
                            try:
                                resFic.write("\t title = {"+str(bre['title']).capitalize() +"},\n")
                            except: #damm unicode
                                resFic.write("\t title = {""},\n")
                            resFic.write("\t year = {" +str(Date.year)+ "},\n")
                            resFic.write("\t month = {" +str(Date.month)+ "},\n")
                            resFic.write("\t day = {" +str(Date.day)+ "},\n")
                            resFic.write("\t number = {" +str(bre['label'])+ "},\n")
                            resFic.write("\t location = {" +str(bre['country'])+ "},\n")
                            if isinstance(bre['IPCR11'], list):
                                resFic.write("\t IPC_class = {" + str(', '.join(bre['IPCR11'])) + "},\n")
                            else:
                                resFic.write("\t IPC_class = {" + str(bre['IPCR11']) + "},\n")
                            resFic.write("\t url = {" +"http://worldwide.espacenet.com/searchResults?compact=false&ST=singleline&query="+str(bre['label'])+"&locale=en_EP&DB=EPODOC" + "},\n")
                            resFic.write("\t urlyear = {" +str(aujourd.year)+ "},\n")
                            resFic.write("\t urlmonth = {" +str(aujourd.month)+ "},\n")
                            resFic.write("\t urlday = {" +str(aujourd.day)+ "},\n")
                            resFic.write("}\n \n")

                    compt +=1

        print(compt, ' bibliographic data added in ', ndf +'.bib file')
        print("Other bibliographic entry aren't consistent nor A, B, C statuses")
