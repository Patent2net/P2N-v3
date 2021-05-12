import sys
import os
from subprocess import Popen
from Patent2Net.app.data.fusion_list import FusionList
from Patent2Net.app.data.process_list import ProcessList
from Patent2Net.P2N_Config import LoadConfig

def main():
    
    config = LoadConfig()
    target_path = get_target_path()

    ProcessList(config.ndf).reset()
    FusionList(config.ndf).reset()

    
    run_spliter = Popen(['python', 'Patent2Net/scripts/run_spliter.py', target_path])
    run_spliter.wait()
    process_list = Popen(['python', 'Patent2Net/scripts/process_list.py', target_path])
    process_list.wait()
    fusion_patents = Popen(['python', 'Patent2Net/scripts/fusion_patents.py', target_path])
    fusion_patents.wait()
    
    destination = os.path.join("..", target_path.replace(".cql", "") + "_fusion.cql")
    config = "--config=" + destination
    Popen(['p2n', 'run', config])

def get_target_path():
    if len(sys.argv) > 1:
            for arg in sys.argv:
                if ".cql" in arg.lower():
                    return arg


if __name__ == "__main__":
    main()