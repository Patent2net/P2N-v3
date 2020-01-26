# -*- coding: utf-8 -*-
"""
Created on Mon Dec 07 17:27:54 2015 in variable 'Request'), and day, moth, ipc as parameters also.
Requests.cql files are built in ..\RequestsAuto". 
The request spliter check bet splitting level in the following order: (Year month day ipc) to limit the amount of produced files.

Once done, runP2NSpecial must be adapted to use the directory in witch all requests are placed. Running it will use p2n adquire
to gatter patent lists.
 FusionPatList is expected to be called then to generate one datadirectory folder and a request file (requete.cql) configured to
gather the missing data (biblio, contents and famillies) and used with runP2Nsingle.bat
@author: dreymond
"""
from p2n.config import OPSCredentials
from Patent2Net.P2N_Lib import PatentSearch
import os
import epo_ops

jourOk, moisOk, ipcOk = False, False, False
RequestOrig = 'PN=BR' 
Request = RequestOrig + ' AND PD=date' 

DataDir = 'Autom'
fic =open("requestModelcql")
DataReq = "..\RequestsAuto"
data = fic.read()
fic.close()

lstFicOk = os.listdir("..\RequestsAuto")

Months= {'jan':31, 'fev':29, 'mar':31, 'apr':30, 'may':31, 'jun':30, 'jui':31, 
         'aug':31, 'sep':30, 'octo':31, 'nov': 30, 'dec': 31}
IPC ={"A", "B", "C", "D", "E", "F", "G", "H"}

os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'
global key
global secret

# put your credential from epo client in this file...
# chargement clés de client
c = OPSCredentials(credentials_file='../cles-epo.txt')
key, secret = c.read()


def checkRequest(req):
    ops_client = epo_ops.Client(key, secret)
#        data = ops_client.family('publication', , 'biblio')
    ops_client.accept_type = 'application/json'
    try:
        lstBrevets2, nbTrouves = PatentSearch(ops_client, req)
        return nbTrouves
    except:
        return 0
Total =0
nbFiles = 0
toBeFound= checkRequest(RequestOrig)

if toBeFound>2000:
    print ('wow ', toBeFound, ' patents to retreive... A good reason to use this script')
    Need = True
else:
    print ("no need to split, gather directly your request '", RequestOrig, "' with p2n" )
    Need = False

if Need:
    for AN in range(1970, 2021,1):
        
        Trouves = checkRequest(Request.replace('=date', '='+str(AN)))
        if 2000>Trouves>0:
            Total += Trouves
            # a request for that year is ok
            monthOk = False
            ipcOk = False
            Request2 = Request.replace('=date', '='+str(AN))
            data2 = data.replace("***requete***", Request2)
            data2 = data2.replace("***dataDir***", DataDir+str(AN))
            NameFic = str(AN)+'Request.cql'
            with open(DataReq+"\\"+NameFic, "w") as ficRes: #+"-"+ipc    
                if ficRes.name.split('\\')[2] not in lstFicOk:
                    ficRes.write(data2)
                nbFiles +=1
                print (ficRes.name, 'file written, ', Trouves,' patents expected and ', Total, ' cumulative.' )
        if Trouves == 0:
            monthOk = False
            ipcOk = False
            jourOk = False
            #nothing to do 
        if Trouves >= 2000:
            # we have to split by monthes
            monthOk = True
            jourOk = False
                
            cpt= 0 #used as monthes
            
            for month in Months.keys():
                cpt +=1
                if len(str(cpt))<2: # monthes are numbered thanks to cpt (ugly isn't it ?)
                    mois = '0'+str(cpt)
                else:
                    mois = str(cpt)
                Request2 = Request.replace('=date', '='+str(AN)+mois)
                Trouves = checkRequest(Request2)
                if 2000>Trouves>0:
                    Total += Trouves
                    # OK less than 2000 and more than 0 go ahead for that request
                    ipcOk = False
                    jourOk = False
                    data2 = data.replace("***requete***", Request2)
                    data2 = data2.replace("***dataDir***", DataDir+str(AN)+mois)
                    NameFic = str(AN)+mois+'Request.cql'
                    if NameFic not in lstFicOk:
                        with open(DataReq+"\\"+NameFic, "w") as ficRes: #+"-"+ipc 
                        
                            ficRes.write(data2)
                        nbFiles +=1
                        print (ficRes.name, 'file written, ', Trouves,' patents expected and ', Total, ' cumulative.' )
                if Trouves == 0:
                    ipcOk = False
                    jourOk = False
                    #nothing to do 
                if Trouves >= 2000:
                    monthOk = True
                    jourOk = True
                    ipcOk = False
                    # spliting days for that month
                    for day in range(1, Months[month]+1):
                        if len(str(day))<2:
                            jour = '0'+str(day)  
                        else:
                            jour = str(day)
                        Request2 = Request.replace('=date', '='+str(AN)+mois+jour)
                        Trouves = checkRequest(Request2)
                        if 2000>Trouves>0:
                            Total += Trouves
                            # go ahead for that day
                            ipcOk = False
                            data2 = data.replace("***requete***", Request2)
                            data2 = data2.replace("***dataDir***", DataDir+str(AN)+mois+jour)
                            NameFic = str(AN)+mois+jour+'Request.cql'
                            if NameFic not in lstFicOk:
                                with open(DataReq+"\\"+NameFic, "w") as ficRes: #+"-"+ipc    
                                        ficRes.write(data2)
                                nbFiles +=1
                                print (ficRes.name, 'file written, ', Trouves,' patents expected and ', Total, ' cumulative.' )
                        if Trouves == 0:
                            ipcOk = False
                            jourOk = False
                            #nothing to do 
                        if Trouves >= 2000:
                            monthOk = True
                            jourOk = True
                            # bad days for EPO... we need to split again    
                            # last solution IPC splitting
                            # for that day only
                            for ipc in IPC:
                                Request3 = Request2 + " AND IC=" + ipc
                                Trouves = checkRequest(Request3)
                                if Trouves>2000:
                                    print ("thats bad... the request : " + Request3 + " should be splitted and the limits of this script are reached")
                                    break
                                Total += Trouves
                                data2 = data.replace("***requete***", Request3)
                                data2 = data2.replace("***dataDir***", DataDir+str(AN)+mois+jour+ipc)
                                if NameFic not in lstFicOk:
                                    with open(DataReq+"\\"+str(AN)+mois+'-'+jour+'-'+ipc+'Request.cql', "w") as ficRes: #+"-"+ipc    
                                            ficRes.write(data2)
                                    nbFiles +=1
                                    print (ficRes.name, 'file written, ', Trouves,' patents expected and ', Total, ' cumulative.' )
                            
    print ("request splitted in ", nbFiles, " files")
                
    print ("Gathering with P2N all this request should lead to ", Total, " patents")
                
            
            
            

        