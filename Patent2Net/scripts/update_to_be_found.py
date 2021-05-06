from p2n.config import OPSCredentials
from Patent2Net.P2N_Lib import PatentSearch
from Patent2Net.P2N_Config import LoadConfig
from Patent2Net.app.dex import set_data_to_be_found
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

if __name__ == "__main__":
    configFile = LoadConfig()

    requete = configFile.requete
    ndf = configFile.ndf

    targetDirectory = REQUEST_AUTO_FOLDER + ndf

    if not os.path.exists(targetDirectory):
        os.makedirs(targetDirectory)
        lstFicOk = []
    else:
        lstFicOk = os.listdir(targetDirectory)

    toBeFound= checkRequest(requete)

    if toBeFound>2000:
        Need = True
        print ('wow ', toBeFound, ' (or more) patents to retreive... A good reason to use this script')
    else:
        Need = False
        print ("no need to split, gather directly your request '", requete, "' with p2n" )

    set_data_to_be_found(ndf, Need, toBeFound, lstFicOk)
