"""
Created on May 2020

@author Romaric Gauzi

Allows you to run a separate request list in a sub-folder of RequestsAuto
"""
import os
import json
import zipfile
import io
import pathlib
import queue
import requests

from Patent2Net.app.message_announcer import AnnonceProgres
from Patent2Net.P2N_Config import LoadConfig
from Patent2Net.app.data.process_list import ProcessList
from subprocess import Popen

if __name__ == "__main__":
    configFile = LoadConfig()

    RequestOrig = configFile.requete
    directory = configFile.ndf

    auto_directory = "./RequestsAuto/" + directory

    os.chdir("/home/p2n/P2N-V3/")
    cpt = 0
    lstReq = [fi for fi in os.listdir(auto_directory) if fi.endswith(".cql")]
    
    progress_list = ProcessList(directory)
    progress_list.start(lstReq, [])

    for file in lstReq:
        # command="python OPSGatherPatentsv2.py ../RequestsAuto/%s"%(file)
        # os.system(command)

        print("Start process for " + file)

        os.chdir("/home/p2n/P2N-V3/Patent2Net/")
        command="python OPSGatherPatentsv2.py ../RequestsAuto/" + directory + "/%s"%(file)
        os.system(command)
        # config = "--config=../RequestsAuto/%s"%(file)
        # p = Popen(['p2n', 'run', config])

        progress_list.add_done(file)

    progress_list.end()
