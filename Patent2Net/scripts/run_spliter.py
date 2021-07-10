import datetime
import os

import epo_ops

from Patent2Net.P2N_Config import LoadConfig
from Patent2Net.P2N_Lib import PatentSearch
from Patent2Net.app.dex import delete_data_spliter, get_data_to_be_found, get_data_spliter_start_date, read_dex, \
    add_spliter_result, set_spliter_cumulative, set_spliter_result_start, set_spliter_result_end
from p2n.config import OPSCredentials

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

def main():
    configFile = LoadConfig()

    RequestOrig = configFile.requete
    directory = configFile.ndf

    today = datetime.datetime.today()

    read_dex()
    to_be_found = get_data_to_be_found(directory)

    if to_be_found == None:
        print("Vous devez d'abord verifier si la requete doit être découpé")
        return None

    need_spliter = to_be_found["need_spliter"]
    lstFicOk = to_be_found["lstFicOk"]

    if need_spliter != True:
        print("Cette requete n'a pas besoin d'etre découpé")
        return None
    
    dateDeb = get_data_spliter_start_date(directory)

    if dateDeb == None:
        print("Vous devez préciser la date de début pour découper la requete")
        return None

    targetDirectory = REQUEST_AUTO_FOLDER + directory
    if not os.path.exists(targetDirectory):
        os.makedirs(targetDirectory)

    Request = RequestOrig + ' AND PD=date' 
    DataDir = directory + '_segments_'
    
    delete_data_spliter(directory)
    set_spliter_result_start(directory)

    jourOk, moisOk, ipcOk = False, False, False

    Total =0
    nbFiles = 0

    fic =open("Patent2Net/REQUESTS/requestModel.cql", 'r')#requestModel.cql
    DataReq = targetDirectory
    data = fic.read()
    fic.close()

    print("Start for")
    for AN in range(dateDeb, today.year+1,1):  
        print(AN)
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
                add_spliter_result(directory, ficRes.name, str(AN), Trouves)
                set_spliter_cumulative(directory, Total)
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
                        add_spliter_result(directory, ficRes.name, str(AN), Trouves)
                        set_spliter_cumulative(directory, Total)
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
                                add_spliter_result(directory, ficRes.name, str(AN), Trouves)
                                set_spliter_cumulative(directory, Total)
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
                                    add_spliter_result(directory, ficRes.name, str(AN), Trouves)
                                    set_spliter_cumulative(directory, Total)

    set_spliter_result_end(directory)                        
    print ("[request_spliter] request splitted in ", nbFiles, " files")
                
    print ("[request_spliter] Gathering with P2N all this request should lead to ", Total, " patents")

if __name__ == "__main__":
    main()