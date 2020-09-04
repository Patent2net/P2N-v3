# -*- coding: utf-8 -*-
#
# Created on Mon Aug 24 15:34:15 2015
#
# @author: Celso
#
# Objective: Crate a FreePlane (mindmap) file

import os
import shutil
from Patent2Net.P2N_Lib import LoadBiblioFile
from Patent2Net.P2N_FreePlaneLib import LoadDescs, nodecolor, Ipc1Text, CalcSizeIpc1
from Patent2Net.P2N_FreePlaneLib import Ipc3Text, CalcSizeIpc3, Ipc4Text, CalcSizeIpc4, Ipc7Text, CalcSizeIpc7, CalcSizeIpc11, Ipc11Text
from Patent2Net.P2N_Config import LoadConfig

DataBrevets1 = []

ListIpc1 = []
ListIpc3 = []
ListIpc4 = []
ListIpc7 = []

Stop  = False
nIpc1 = ''
nIpc3 = ''
nIpc4 = ''
nIpc7 = ''

nodeside = 'right'
nodetext = ''
ncolor = '#ff0000'
ecolor = '#0000ff'
nsize = '10'

configFile = LoadConfig()
requete = configFile.requete
Gather = configFile.GatherContent
GatherBiblio = configFile.GatherBiblio
IsEnableScript = configFile.FreePlane
P2NFamilly = configFile.GatherFamilly
rep = configFile.ndf

ResultListPath = configFile.ResultListPath
ResultBiblioPath = configFile.ResultBiblioPath

if IsEnableScript:
    LoadDescs()

    prefixes = [""]
    if P2NFamilly:
        prefixes.append("Families")

    for prefix in prefixes:
        ndf = prefix + configFile.ndf
        try:
            with open(ResultBiblioPath+'//'+ndf, 'r') as fic:
                DataBrevets1 = LoadBiblioFile(ResultBiblioPath, ndf)
                BrevetsTotal = str(len(DataBrevets1['brevets']))
        except:
            print("Error: there are no data to generate de FreePlane file")
        # End of Load patent file
        #

        ### ugly code to patch classification extraction inconsistency
        for bre in DataBrevets1['brevets']:
            if isinstance(bre['classification'], list):
                if '' in bre['classification']:
                    bre['classification'].remove('')
            bre['IPCR11'] =  bre['classification']

            lstIPC = [ipc[0] for ipc in bre['classification']]
            for ipc in lstIPC:
                # need to be sure we have lists, not strings
                if isinstance(bre['IPCR11'], str):
                    bre['IPCR11'] = [bre['IPCR11']]
                for ipc11 in bre['IPCR11']:
                    for car, ipc in [(1, 'IPCR1'), (3, 'IPCR3'), (4, 'IPCR4'), (6, 'IPCR7')]:
                        # need to be sure we have lists, not strings
                        if isinstance(bre[ipc], str):
                            bre[ipc] = [bre[ipc]]
                        if ipc11[0:car].replace('/', '') not in bre[ipc]:
                            bre[ipc].append(ipc11[0:car].replace('/', ''))
        ## end of patch

        requeteHtml = requete.replace('<','&lt;').replace('>','&gt;')

        MindMapPath = '..//DATA//'+rep+'//'+rep+ '.html_files'
        try:
            os.makedirs(MindMapPath)
        except:
            pass

        fictemp=open(MindMapPath+'//'+ndf+'FP.mm', 'w')

        fictemp.write('''<map version="freeplane 1.3.0"> \n''')
        fictemp.write('''<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net --> \n''')
        fictemp.write('''<node TEXT="Project: ''' + ndf + ''' " BACKGROUND_COLOR="#FFFF33"> \n''')
        #fictemp.write('''<edge STYLE="sharp_bezier" COLOR="#808080" WIDTH="thin"/> \n''')
        #fictemp.write('''<icon BUILTIN="info"/> \n''')
        fictemp.write('''<hook NAME="MapStyle"> \n''')
        fictemp.write('''   <properties show_note_icons="true"/>\n''')
        fictemp.write('''</hook> \n''')

        # New hook
        fictemp.write('''<hook NAME="AutomaticEdgeColor" COUNTER="5"/> \n''')
        fictemp.write('''<richcontent TYPE="NOTE"> \n''')
        fictemp.write('''<html> \n''')
        fictemp.write('''  <head> \n''')
        fictemp.write('''  </head> \n''')
        fictemp.write('''  <body> \n''')
        fictemp.write('''    <p> \n''')
        fictemp.write('''      Chave de pesquisa: ''' + requeteHtml + ''' \n''')
        fictemp.write('''    </p> \n''')
        fictemp.write('''    <p> \n''')
        fictemp.write('''      Total de patentes encontradas: ''' + BrevetsTotal + ''' \n''')
        fictemp.write('''    </p> \n''')
        fictemp.write('''  </body> \n''')
        fictemp.write('''</html> \n''')
        fictemp.write('''</richcontent> \n''')

        # New node

        for i in DataBrevets1['brevets']:
            for j in i['IPCR1']:
                if ListIpc1.count(j) == 0 and j !='':
                    # Node level IPC1
                    nIpc1 = j
                    ListIpc1.append(nIpc1)
                    if nodeside == 'right':
                        nodeside = 'left'
                    else:
                        nodeside = 'right'
                    ncolor = nodecolor(ncolor)
                    nsize, ncount1 = CalcSizeIpc1(nIpc1,DataBrevets1)
                    nodetext = Ipc1Text(nIpc1) + " (" + ncount1 + " Patents)"
                    fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''"  BACKGROUND_COLOR="''' + ncolor + '''" STYLE="bubble" MAX_WIDTH="200"> \n''')
                    fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
                    fictemp.write('''<font NAME="Serif" SIZE="'''+ nsize + '''"/> \n''')

                    ListIpc3 = []
                    for k in DataBrevets1['brevets']:
                        for l in k['IPCR3']:
                            if ListIpc3.count(l) == 0 and l !='' and l.count(nIpc1,0,1) == 1:
        # Node level IPC3
                                nIpc3 = l
                                ListIpc3.append(nIpc3)
                                nsize, ncount3 = CalcSizeIpc3(nIpc3,DataBrevets1,ncount1)
                                nodetext = Ipc3Text(nIpc3) + " (" + ncount3 + " Patents)"
        #                        fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="#F9F4F4" STYLE="bubble" MAX_WIDTH="300">\n''')
                                fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''"  BACKGROUND_COLOR="''' + ncolor + '''" STYLE="bubble" MAX_WIDTH="300">\n''')
                                fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                                fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
                                ListIpc4 = []
                                for m in DataBrevets1['brevets']:
                                    for n in m['IPCR4']:
                                        if ListIpc4.count(n) == 0 and n !='' and n.count(nIpc3,0,3) == 1:
            # Node level IPC4
                                            nIpc4 = n
                                            ListIpc4.append(nIpc4)
                                            nsize, ncount4 = CalcSizeIpc4(nIpc4,DataBrevets1,ncount3)
                                            nodetext = Ipc4Text(nIpc4) + " (" + ncount4 + " Patents)"
        #                                    fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="#FFFFFF" STYLE="bubble" MAX_WIDTH="300">\n''')
                                            fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="''' + ncolor + '''" STYLE="bubble" MAX_WIDTH="300">\n''')
                                            fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                                            fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
                                            ListIpc7 = []
                                            for o in DataBrevets1['brevets']:
                                                for p in o['IPCR7']:
                                                    if ListIpc7.count(p) == 0 and p !='' and p.count(nIpc4,0,4) == 1:
                        # Node level IPC7
                                                        nIpc7 = p
                                                        ListIpc7.append(nIpc7)
                                                        nsize, ncount7 = CalcSizeIpc7(nIpc7,DataBrevets1,ncount4)
                                                        nodetext = Ipc7Text(nIpc7) + " (" + ncount7 + " Patents)"
        #                                                fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="#FFFFFF" STYLE="fork" MAX_WIDTH="300">\n''')
                                                        fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="''' + ncolor + '''" STYLE="bubble" MAX_WIDTH="300">\n''')
                                                        fictemp.write('''<font SIZE="'''+ '10' + '''"/> \n''')
                                                        fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')

                                                        ListIpc11 = []
                                                        for q in DataBrevets1['brevets']:
                                                            for r in q['IPCR11']:
                                                                if ListIpc11.count(r) == 0 and r !='' and r.count(nIpc7,0,7) == 1:  # and r[len(r)-2:len(r)] != '00': -- removed in 23-jun-17 to enable tha map show all records
                                    # Node level IPC11
                                                                    nIpc11 = r
                                                                    ListIpc11.append(nIpc11)
                                                                    nameLink = nIpc11.replace('/','%2F')
                                                                    nsize, ncount11 = CalcSizeIpc11(nIpc11,DataBrevets1,ncount7)
                                                                    nodetext = Ipc11Text(nIpc11) + " (" + ncount11 + " Patents)"
                                                                    fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="''' + ncolor + '''" STYLE="bubble" MAX_WIDTH="300" LINK="https://worldwide.espacenet.com/searchResults?ST=singleline&amp;locale=en_EP&amp;submitted=true&amp;DB=&amp;query=ipc%3D''' + nameLink + '''&amp;Submit=Search">\n''')
                                                                    fictemp.write('''<font SIZE="'''+ '10' + '''"/> \n''')
                                                                    fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
    # Abstracts
                                                                    for q1 in DataBrevets1['brevets']:
                                                                        if q1['IPCR11'].count(nIpc11) != 0:
                                                                            # I had to remove this from str(q1['title'], 'utf8', 'replace'
                                                                            nodetext = q1['label'] + ": " + str(q1['title']).replace('"','').replace('& ','AND ').replace('&','')
                                                                            nameLink = q1['label']
                                                                            try:
                                                                                fictemp1=open( '..//DATA//'+rep+'//PatentContents//' + prefix + 'Abstract//en-'+q1['label']+'.txt', 'r')
                                                                                abstractLines = fictemp1.readlines()
                                                                                textAbstract = abstractLines[1].replace('<','').replace('>','').replace('\\','')
    # Issue #6 - by cvanderlei in 6-jan-2017
                                                                                fictemp1.close()
                                                                            except:
                                                                                textAbstract = '(abstract not available)'
                                                                            try:
                                                                                fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="''' + ncolor + '''" STYLE="fork" MAX_WIDTH="300" LINK="https://worldwide.espacenet.com/searchResults?ST=singleline&amp;locale=en_EP&amp;submitted=true&amp;DB=&amp;query=''' + nameLink + '''&amp;Submit=Search">\n''')
                                                                            except UnicodeEncodeError:
                                                                                fictemp.write('''<node TEXT="'''+ q1['label'] +''': (description not available)''' + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="''' + ncolor + '''" STYLE="fork" MAX_WIDTH="300" LINK="https://worldwide.espacenet.com/searchResults?ST=singleline&amp;locale=en_EP&amp;submitted=true&amp;DB=&amp;query=''' + nameLink + '''&amp;Submit=Search">\n''')
                                                                            fictemp.write('''<font SIZE="'''+ '10' + '''"/> \n''')
                                                                            fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
                                                                            fictemp.write('''<richcontent TYPE="NOTE"> \n''')
                                                                            fictemp.write('''<html> \n''')
                                                                            fictemp.write('''  <head> \n''')
                                                                            fictemp.write('''  </head> \n''')
                                                                            fictemp.write('''  <body> \n''')
                                                                            fictemp.write('''    <p> \n''')
                                                                            fictemp.write('''      Abstract: (''' + q1['year'][0] + ''') \n''')
                                                                            fictemp.write('''    </p> \n''')
                                                                            fictemp.write('''    <p> \n''')
                                                                            fictemp.write('''       ''' + textAbstract + ''' \n''')
                                                                            fictemp.write('''    </p> \n''')
                                                                            fictemp.write('''  </body> \n''')
                                                                            fictemp.write('''</html> \n''')
                                                                            fictemp.write('''</richcontent> \n''')
                                                                            fictemp.write('''</node> \n''')
    # End of Abstracts
                                                                    fictemp.write('''</node> \n''')
                                        # End node level IPC11

                                                        fictemp.write('''</node> \n''')
                            # End node level IPC7
                                            fictemp.write('''</node> \n''')
                # End node level IPC4
                                fictemp.write('''</node> \n''')
        # End node level IPC3
                    fictemp.write('''</node> \n''')
        # End node level IPC1

        # Close ORIGINAL node
        fictemp.write('''</node> \n''')

        #Clsoe map
        fictemp.write('''</map> \n''')

        fictemp.write(''' \n''')
        fictemp.write(''' \n''')
        fictemp.write(''' \n''')
        fictemp.write(''' \n''')
        fictemp.write(''' \n''')
        fictemp.write(''' \n''')
        fictemp.write(''' \n''')

        fictemp.close()

        print("Mindmap file writen in " + '..//DATA//'+rep)

        fictemp=open( '..//DATA//'+rep+'//'+ndf+ 'FP.html', 'w')

        fictemp.write('''<?xml version="1.0" encoding="us-ascii"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> \n''')
        fictemp.write('''<html><head><title>Project:'''+ndf+'''</title><style type="text/css"> \n''')
        fictemp.write('''/**/\n''')
        fictemp.write('''body { margin-left:0px; margin-right:0px; margin-top:0px; margin-bottom:0px; height:100% } \n''')
        fictemp.write('''html { height:100% } \n''')
        fictemp.write('''/**/  \n''')
        fictemp.write('''          </style></head><body><script src="'''+rep+'''.html_files/deployJava.js"></script><script> \n''')
        fictemp.write('''	        var attributes = { \n''')
        fictemp.write('''	            code:"org.freeplane.main.applet.FreeplaneApplet",  width:"100%", height:"100%"} ; \n''')
        fictemp.write('''	        var parameters = { \n''')
        fictemp.write('''	        jnlp_href: "'''+rep+'''.html_files/freeplane_applet.jnlp", \n''')
        fictemp.write('''	        browsemode_initial_map:"./'''+rep+'''.html_files/'''+ndf+'''FP.mm", \n''')
        fictemp.write('''	        selection_method:"selection_method_direct" \n''')
        fictemp.write('''	        } ; \n''')
        fictemp.write('''	        parameters["location_href"] = window.location.href; \n''')
        fictemp.write(''' \n''')
        fictemp.write('''	        deployJava.runApplet(attributes, parameters, "1.5"); \n''')
        fictemp.write('''	    </script></body></html> \n''')
        fictemp.write(''' \n''')
        fictemp.close()

        # OSCmd = 'COPY .\\extensions\mapsOnLine\\*.* ..\\DATA\\' +rep+'\\'+ rep+'.html_files\\'
        # os.system(OSCmd)
        src = './/extensions//mapsOnline'
        dest = '..//DATA//' +rep+'//'+ rep+'.html_files'
        src_files = os.listdir(src)
        for file_name in src_files:
            full_file_name = os.path.join(src, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, dest)
