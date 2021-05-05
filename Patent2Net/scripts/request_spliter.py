
from p2n.config import OPSCredentials
from Patent2Net.P2N_Lib import PatentSearch
from Patent2Net.P2N_Config import LoadConfig
import os
import epo_ops
import datetime
import sys

Months= {'jan':31, 'fev':29, 'mar':31, 'apr':30, 'may':31, 'jun':30, 'jui':31, 
        'aug':31, 'sep':30, 'octo':31, 'nov': 30, 'dec': 31}
IPC ={"A", "B", "C", "D", "E", "F", "G", "H"}
REQUEST_AUTO_FOLDER = 'RequestsAuto/'

os.environ['REQUESTS_CA_BUNDLE'] = 'Patent2Net/cacert.pem'
global key
global secret

c = OPSCredentials(credentials_file='cles-epo.txt')
key, secret = c.read()

def checkRequest(req):
    ops_client = epo_ops.Client(key, secret)
    #  data = ops_client.family('publication', , 'biblio')
    ops_client.accept_type = 'application/json'
    try:
        lstBrevets2, nbTrouves = PatentSearch(ops_client, req)
        return nbTrouves
    except:
        return 0

def autom_request_is_needed(RequestOrig, directory):
    targetDirectory = REQUEST_AUTO_FOLDER + directory

    if not os.path.exists(targetDirectory):
        os.makedirs(targetDirectory)
        lstFicOk = []
    else:
        lstFicOk = os.listdir(targetDirectory)

    toBeFound= checkRequest(RequestOrig)

    if toBeFound>2000:
        Need = True
        print ('wow ', toBeFound, ' (or more) patents to retreive... A good reason to use this script')
    else:
        Need = False
        print ("no need to split, gather directly your request '", requete, "' with p2n" )

    return Need, lstFicOk, toBeFound

def run_autom_request(RequestOrig, directory, dateDeb, lstFicOk):
    today = datetime.datetime.today()

    targetDirectory = REQUEST_AUTO_FOLDER + directory
    Request = RequestOrig + ' AND PD=date' 
    DataDir = directory + '/segments/' + directory

    jourOk, moisOk, ipcOk = False, False, False

    Total =0
    nbFiles = 0

    fic =open("Patent2Net/REQUESTS/requestModel.cql", 'r')#requestModel.cql
    DataReq = targetDirectory
    data = fic.read()
    fic.close()

    for AN in range(dateDeb, today.year+1,1):  
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
            with open(DataReq+"/"+NameFic, "w") as ficRes: #+"-"+ipc
                print(ficRes.name.split('/')[1])
                if ficRes.name.split('/')[1] not in lstFicOk:
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
                        with open(DataReq+"/"+NameFic, "w") as ficRes: #+"-"+ipc 
                        
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
                                with open(DataReq+"/"+NameFic, "w") as ficRes: #+"-"+ipc    
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
                                    with open(DataReq+"/"+str(AN)+mois+'-'+jour+'-'+ipc+'Request.cql', "w") as ficRes: #+"-"+ipc    
                                            ficRes.write(data2)
                                    nbFiles +=1
                                    print (ficRes.name, 'file written, ', Trouves,' patents expected and ', Total, ' cumulative.' )
                            
    print ("[request_spliter] request splitted in ", nbFiles, " files")
                
    print ("[request_spliter] Gathering with P2N all this request should lead to ", Total, " patents")

    return targetDirectory

if __name__ == "__main__":
    configFile = LoadConfig()

    requete = configFile.requete
    ndf = configFile.ndf

    Need, lstFicOk, toBeFound = autom_request_is_needed(requete, ndf)

    if Need:
        dateDeb = int(input ("[request_spliter] Please enter the stardate year for gathering you request: "))

        run_autom_request(requete, ndf, dateDeb, lstFicOk)