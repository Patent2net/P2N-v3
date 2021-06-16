from Patent2Net.app.request import new_single_req_without_date_split
import sys
import os
from subprocess import Popen
from Patent2Net.app.data.fusion_list import FusionList
from Patent2Net.app.data.process_list import ProcessList
from Patent2Net.app.dex import read_dex
from Patent2Net.P2N_Config import LoadConfig
from Patent2Net.app.fusion import getFusion

def main():
    
    if len(sys.argv) > 1:
        fusionFile = sys.argv[1]
        dex = read_dex()
        fustion = getFusion(fusionFile, dex['in_progress'], dex['done'])

        os.chdir("/home/p2n/P2N-V3/Patent2Net")
        
        main = fustion["content"]["main"]
        
        command = ['python', 'FusionPatentList2.py']
        command.append(fustion["content"]["folders"])
        command.append(main)

        run_spliter = Popen(command)
        run_spliter.wait()

        new_single_req_without_date_split(main)

if __name__ == "__main__":
    main()