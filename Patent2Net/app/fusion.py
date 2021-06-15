
from Patent2Net.app.dex import get_current_dex
import os
import json
from os import listdir
from os.path import isfile, join

fusion_folder = os.path.dirname(os.path.realpath(__file__)) + "/../../FusionsSets/"

def createFusion(main, folders, rules):

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
        try:      
            with open(fusion_folder + f) as f:
                fusion = json.load(f) 
                f.close()

                print(fusion)
 
        except IOError:
            print("Error for reading fusion file " + f)


def listFusions():
    fusion_folder = os.path.dirname(os.path.realpath(__file__)) + "/../../FusionsSets/"
    fusions = listdir(fusion_folder)

    def mapFusions(fusion_name):
        dex = get_current_dex()
        return getFusion(fusion_name, dex["in_progress"], dex["done"])

    result = map( mapFusions , fusions)
    return(list(result))



def getFusion(fusion_name, in_progress_list, done_list):
    try:      
        with open(fusion_folder + fusion_name) as f:
            fusion = json.load(f) 
            f.close()

            return {
                "name": fusion_name,
                "content": fusion,
                "in_progress": fusion["main"] in in_progress_list,
                "done": fusion["main"] in done_list
            }

    except IOError:
        print("Error for reading fusion file " + fusion_name)