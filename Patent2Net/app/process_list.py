import os
import json
import zipfile
import io
import pathlib
import queue
import requests

from Patent2Net.app.message_announcer import AnnonceProgres 
from subprocess import Popen

def processListv1():  
    os.chdir("/home/p2n/P2N-V3/")
    cpt = 0
    lstReq = [fi for fi in os.listdir("./RequestsAuto") if fi.endswith(".cql")]
    os.chdir("/home/p2n/P2N-V3/Patent2Net")
    
    lstScripts1 = [
        "OPSGatherPatentsv2.py", 
        "PatentListFiltering.py", 
        "OPSGatherAugment-Families.py", 
        "PatentListFiltering.py", 
        "preProcessNormalisationNames.py",
        "OPSGatherContentsV2-Iramuteq.py", 
        "OPSGatherContentsV2-Images.py"
    ]         
                          
    lstScripts2 = [
        "FormateExportCountryCartography.py",
        "FormateExportAttractivityCartography.py",
        "FormateExportBiblio.py",
        "FormateExportDataTableFamilies.py",
        "FormateExportDataTable.py",
        "FormateExportPivotTable.py",
        "P2N-Nets-new.py",
        "P2N-FreePlane.py"
    
    ] 
    lstScripts3 = [
        "FusionIramuteq2.py", 
        "FusionCarrot2.py",
        "FusionImages.py",
        "P2N-Indexer.py", 
        "IPC-WS-metrics.py",
        "ClusterPreProcess.py",
        "P2N-Cluster.py",
        "Interface2.py"
    ]

    for file in lstReq:
        cpt +=1
        AnnonceProgres (Appli = 'cql-files', valMax = 100, valActu = cpt*100/len(lstReq))
        for cmd in lstScripts1:
            command="python " + cmd + " ../RequestsAuto/%s"%(file)               
        for cmd in lstScripts2:
            command="python " + cmd + " ../RequestsAuto/%s"%(file)               
            #♥ can be launched in parallel
            os.system(command)
        for cmd in lstScripts3:
            command="python " + cmd + " ../RequestsAuto/%s"%(file)               
            os.system(command)


os.environ['PYTHONPATH'] = os.getcwd()


async def process_list_v2(autoDirectory):
    os.chdir("/home/p2n/P2N-V3/")
    lstReq = [fi for fi in os.listdir("./RequestsAuto/" + autoDirectory) if fi.endswith(".cql")]
    
    for file in lstReq:
        print("Start process for " + file)

        command="p2n run --config=../RequestsAuto/%s"%(file)
        os.system(command) 

    return True


if __name__ == "__main__":
    os.chdir("/home/p2n/P2N-V3/")
    cpt = 0
    lstReq = [fi for fi in os.listdir("./RequestsAuto") if fi.endswith(".cql")]
    
    for file in lstReq:
        # command="python OPSGatherPatentsv2.py ../RequestsAuto/%s"%(file)
        # os.system(command)

        print("Start process for " + file)

        
        command="p2n run --config=../RequestsAuto/%s"%(file)
        os.system(command) 
        # config = "--config=../RequestsAuto/%s"%(file)
        # p = Popen(['p2n', 'run', config])

