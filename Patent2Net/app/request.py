

import os
from subprocess import Popen
from Patent2Net.app.dex import delete_data_to_be_found, set_in_progress, set_state
from Patent2Net.app.fusion import createFusion

def get_target_path(directory):
    return "./RequestsSets/%s.cql" %directory


def new_single_req_with_split(directory):
    set_in_progress(directory)
    set_state(directory, "SINGLE_REQ_WITH_SPLIT")
    delete_data_to_be_found(directory)

    os.chdir("/home/p2n/P2N-V3/")
    Popen(['python', 'Patent2Net/scripts/update_to_be_found.py', get_target_path(directory)])


def new_single_req_without_date_split(directory):
    set_in_progress(directory)
    set_state(directory, "SINGLE_REQ_WITHOUT_SPLIT")

    os.chdir("/home/p2n/P2N-V3/")
    Popen(['p2n', 'run', get_target_path(directory)])



def new_csv_request(csv, directory, options, split = False):

    print("request csv")


def new_list_request(main, requestDirectories, split = False):

    print("request list")

    for directory in requestDirectories:
        if split:
            new_single_req_with_split(directory)
        else:
            new_single_req_without_date_split(directory)

    createFusion(main, requestDirectories, ['none_in_progress'])






# def process_single(p2n_dir, config):
#     print("PROGRESS SINGLE: " + p2n_dir)

#     set_in_progress(p2n_dir)
#     set_state(p2n_dir, "SINGLE_REQ_WITHOUT_SPLIT")
#     p = Popen(['p2n', 'run', config])


    
# def process_multi(p2n_dir, target_path):
#     print("PROGRESS MULTI: " + p2n_dir)

#     set_in_progress(p2n_dir)
#     set_state(p2n_dir, "SINGLE_REQ_WITH_SPLIT")
#     delete_data_to_be_found(p2n_dir)

#     p = Popen(['python', 'Patent2Net/scripts/update_to_be_found.py', target_path])
