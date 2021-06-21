
from Patent2Net.P2N_Config import LoadConfig
from subprocess import Popen
from Patent2Net.app.dex import get_current_dex
import os
import json
from os import listdir
from os.path import isfile, join

fusion_folder = os.path.dirname(os.path.realpath(__file__)) + "/../../FusionsSets/"

def createFusion(main, folders, rules, fusion_request, p2n_options, labels):

    from Patent2Net.app.request import create_request_file
    create_request_file(main, fusion_request, p2n_options, labels, no_patent=True)

    fusion_location = os.path.dirname(os.path.realpath(__file__)) + "/../../FusionsSets/%s.json"%main

    fusion = {
        "main": main,
        "folders": folders,
        "rules": rules
    }

    f = open(fusion_location, "w")
    f.write(json.dumps(fusion))
    f.close()


def checkFusions():
    for f in listdir(fusion_folder):
        dex = get_current_dex()
        fusion = getFusion(f, dex["in_progress"], dex["done"])

        if not fusion["done"]:

            if "none_in_progress" in fusion["content"]["folders"]:
                is_in_progress = False
                
                for folder in fusion["content"]["folders"]:
                    if folder in dex["in_progress"] and not is_in_progress:
                        is_in_progress = True
    
                if (not is_in_progress):

                    os.chdir("/home/p2n/P2N-V3/")
                    Popen(['python', 'Patent2Net/scripts/start_fusion.py', f])



def listFusions():
    fusion_folder = os.path.dirname(os.path.realpath(__file__)) + "/../../FusionsSets/"
    fusions = listdir(fusion_folder)

    def mapFusions(fusion_name):
        dex = get_current_dex()
        return getFusion(fusion_name, dex["in_progress"], dex["done"])

    def filterNoneFusions(fusion):
        if fusion:
            return True
        return False

    result = map( mapFusions , fusions)
    result_filter = filter(filterNoneFusions, result)    

    return(list(result_filter))



def getFusion(fusion_name, in_progress_list, done_list):
    try:      
        with open(fusion_folder + fusion_name) as f:
            fusion = json.load(f) 
            f.close()

            configFile = LoadConfig(fusion["main"] + ".cql")

            if configFile:
                return {
                    "name": fusion_name,
                    "content": fusion,
                    "in_progress": fusion["main"] in in_progress_list,
                    "done": fusion["main"] in done_list,
                    "cql": {
                        "requete": configFile.requete,
                        "ndf": configFile.ndf,
                        "options": {
                            "GatherContent": configFile.GatherContent,
                            "GatherBiblio": configFile.GatherBiblio,
                            "GatherPatent": configFile.GatherPatent,
                            "GatherFamilly": configFile.GatherFamilly
                        }
                    }
                }
            return None

    except IOError:
        print("Error for reading fusion file " + fusion_name)


os.chdir("/home/p2n/P2N-V3/Patent2Net/")
Popen(['python', '../Patent2Net/scripts/start_fusion_cron.py'])
os.chdir("/home/p2n/P2N-V3/")