

import os
from subprocess import Popen
from Patent2Net.app.dex import delete_data_to_be_found, set_data_progress, set_in_progress, set_state
from Patent2Net.app.fusion import createFusion

def get_target_path(directory):
    return "./RequestsSets/%s.cql" %directory

def get_p2n_config(directory):
    return "--config=../RequestsSets/%s.cql" %directory


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
    Popen(['p2n', 'run', "-config=" + get_p2n_config(directory)])



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


def create_request_file(p2n_dir, p2n_req, p2n_options, labels, no_patent = False):
    f_in = open("placeholder.cql", "rt")

    # #create an output file with the name requested in the form by the user
    target_path = "./RequestsSets/%s.cql" %p2n_dir
    f_out = open(target_path ,"wt")

    def get_option_value(name):
        return 'True' if name in p2n_options else 'False'


    #for each line in the input file    
    #read the values given in the form and replace the corresponding string in the output
    for name in f_in:
        data = name.replace('RequestName', p2n_req ) \
            .replace('RequestDirectory', p2n_dir) \
            .replace('RequestFamily', get_option_value('p2n_family')) \
            .replace('RequestImage', get_option_value('p2n_image')) \
            .replace('RequestNetwork', get_option_value('p2n_network')) \
            .replace('RequestFreeplane', get_option_value('p2n_freeplane')) \
            .replace('RequestBibfile', get_option_value('p2n_bibfile')) \
            .replace('RequestMap', get_option_value('p2n_map')) \
            .replace('RequestTable', get_option_value('p2n_tables')) \
            .replace('RequestCarrot', get_option_value('p2n_carrot')) \
            .replace('RequestIramuteq', get_option_value('p2n_iramuteq'))\
            .replace('RequestCluster', get_option_value('p2n_cluster'))\

        if no_patent:
            data.replace('GatherPatent: True', 'GatherPatent: False' ) 

        f_out.write(data)
    
    #close input and output files
    f_in.close()
    f_out.close()


    labels_keys = labels.keys()
    active_labels_keys = [label_key for label_key in labels_keys if label_key not in ['p2n_dir', 'p2n_filtering', 'p2n_indexer'] and label_key in p2n_options]

    for label_key in active_labels_keys:
        set_data_progress(p2n_dir, label_key, None, None)


def create_patent_request_file(p2n_dir, p2n_req):

    fic =open("Patent2Net/REQUESTS/requestModel.cql", 'r')#requestModel.cql
    data = fic.read()
    fic.close()

    data2 = data.replace("***requete***", p2n_req)
    data2 = data2.replace("***dataDir***", p2n_dir)

    target_path = "./RequestsSets/%s.cql" %p2n_dir
    f_out = open(target_path ,"wt")
    f_out.write(data2)
    f_out.close()


def run_request(p2n_dir, p2n_auto):
    if (p2n_auto == True):
        new_single_req_with_split(p2n_dir)
    else:
        new_single_req_without_date_split(p2n_dir)   


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
