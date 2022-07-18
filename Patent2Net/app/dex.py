import json
import os

from Patent2Net.app.event import send_new_event
from Patent2Net.app.events.progress_value_change import ProgressValueChange
from Patent2Net.app.events.split_end import SplitEnd
from Patent2Net.app.events.split_result_added import SplitResultAdded
from Patent2Net.app.events.split_start import SplitStart
from Patent2Net.app.events.to_be_found_change import ToBeFoundChange

# ---------------------------- #
# NEW DEX SYSTEME - 23/04/2021 #
# ---------------------------- #

"""
This file is used to update the dex.json file.
The dex.json file records the local state of the application, including the status of the requests

3 fields are available in the dex.json:
- in_progress: List of current requests
- done: List of completed queries
- requests: Status of requests done or in progress

Each status of a request is composed of:
- a state that is defined when the query is created (P2N_RUN or SPLITER_RUN)
- data that is an object or any type of data can be recorded in relation to the current query

"""

dex = {
    "in_progress": [],
    "done": []
}
#dex_location = '../dex.json' # os.path.dirname(os.path.realpath(__file__)) +
dex_location = os.path.dirname(os.path.realpath(__file__)) + '/../../dex.json'
print(dex_location)
print ('youp ', os.path.dirname(os.path.realpath(__file__)))


global_progress = {}

# DEX

def read_dex():
    global dex

    try:      
        with open(dex_location) as f:
            dex = json.load(f) 
            f.close()

            normalize()
            for in_progress_elmt in dex["in_progress"]:
                update_global_progress(in_progress_elmt)

    except IOError:
        print("¨pb dex.json file")
        write_dex()

def write_dex():
    global dex

    f = open(dex_location, "w")
    f.write(json.dumps(dex))
    f.close()

def get_current_dex():
    """Recover the current state of the application
    
    :returns: a dictionary with all value of current dex
    :rtype: dict
    """
    global dex
    read_dex()
    return dex

# NORAMALIZE

def normalize():
    global dex
    if "in_progress" not in dex:
        dex["in_progress"] = []
    if "done" not in dex:
        dex["done"] = []
    if "requests" not in dex:
        dex["requests"] = {}

    return dex

def normalize_request_directory(directory):
    requests = dex["requests"]
    if directory not in requests:
        requests[directory] = {
            "state": None,
            "data": {}
        }
    return requests[directory]

# STATES

def set_state(directory, state):
    """Allows you to define the state of one request in progress  
    

    :param directory: The name of the directory of the request
    :type directory: str
    :param state: The new state for this request
    :type state: str
        (P2N_RUN | SPLITER_RUN)
    """

    print("STATE HAS CHANGE: " + directory + " - " + state)
    request_directory = normalize_request_directory(directory)
    request_directory["state"] = state

    write_dex()

def get_state(directory):
    """Allows you to retrieve the current state of a directory

    :param directory: The name of the directory of the request
    :type directory: str
    :returns: the current state of a directory
    :rtype: str
    """
    request_directory = normalize_request_directory(directory)
    return request_directory["state"]

def set_in_progress(directory):
    """Allows you to define a request as in progress
    
    :param directory: The name of the directory of the request to set in progress
    :type directory: str
    """

    global dex
    normalize()

    in_progress = dex["in_progress"]
    if directory not in in_progress:
        in_progress.append(directory)

    write_dex()

def set_done(directory):
    """Allows you to define a request as done
    
    :param directory: The name of the directory of the request to set done
    :type directory: str
    """

    global dex
    normalize()
    #print("coucou")
    #print(dex)
    in_progress = dex["in_progress"]
    done = dex["done"]

    if directory in in_progress:
        in_progress.remove(directory)
    if directory not in done:
        done.append(directory)

    write_dex()


def delete_request(directory):
    in_progress = dex["in_progress"]
    done = dex["done"]
    requests = dex["requests"]

    if directory in in_progress:
        in_progress.remove(directory)
    if directory in in_progress:
        done.remove(directory)
    if directory in requests:
        del requests[directory]

    write_dex()

# DATA

def set_directory_request_data(directory, key, value):
    """Allows to associate a value to a key on the data object of a request
    
    :param directory: The name of the directory of the request to which the data will be associated
    :type directory: str
    :param key: The key to which the data will be associated
    :type key: str
    :param value: The value returned if the data does not exist
    :type value: str
    """
    normalize()
    request_directory = normalize_request_directory(directory)

    request_directory["data"][key] = value

    write_dex()


def get_directory_request_data(directory, key, default = None):
    """Allows to get a value associated to a key on the data object of a query

    :param directory: The name of the query directory to which the data is associated
    :type directory: str
    :param key: The key to which the data is associated
    :type key: str
    :param default: The data to be saved
    :type default: str 
        (default is None)
    :returns: the data
    :rtype: dict
    """
    normalize()
    request_directory = normalize_request_directory(directory)

    if key not in request_directory["data"] or request_directory["data"][key] == None:
        return default

    return request_directory["data"][key]

def get_directory_request_data_all(directory):
    """Retrieves all data associated with a directory 
    
    :param directory: The name of the directory
    :type directory: str
    :returns: the data
    :rtype: dict
    """
    request_directory = normalize_request_directory(directory)
    return request_directory["data"]

def delete_directory_request_data(directory, key):
    """Delete the data 
    
    :param directory: The name of the directory
    :type directory: str
    :param key: The key of the data to be deleted
    :type key: str
    """
    normalize()
    request_directory = normalize_request_directory(directory)
    
    if key in request_directory["data"]:
        del request_directory["data"][key]
        write_dex()


# GLOBAL PROGRESS

def update_global_progress(directory):
    """"
    Allows to calculate the global progress of a request and to save it in the cache for future retrieval. 
    This value is not written in the text 
    """
    global dex, global_progress
    normalize()

    progress_directory = get_directory_request_data(directory, "progress", {})

    done_step_count = 0
    progress_step_count = 0
    total_step_count = len(progress_directory)

    for step_key in progress_directory:
        step = progress_directory[step_key]
        if step["value"] != None and step["max_value"] != None:
            if float(step["value"]) >= float(step["max_value"]):
                done_step_count += 1
            else:
                progress_step_count += 1
    
    global_progress[directory] = {
        "done_step_count": done_step_count,
        "progress_step_count": progress_step_count,
        "total_step_count": total_step_count
    }

def get_global_progress():
    """Allows you to retrieve the global progress of a request saved in the cache"""
    global global_progress

    return global_progress


# UTILS

"""
These functions make it easier to update the data of the requests

Future functions are available in Patent2Net/app/data/
They are grouped by object and by key of the modified data
"""

def set_data_progress(directory, key, value, max_value):
    progress_directory = get_directory_request_data(directory, "progress", {})

    if key not in progress_directory:
        progress_directory[key] = {}

    progress_directory[key]["value"] = value
    progress_directory[key]["max_value"] = max_value

    set_directory_request_data(directory, "progress", progress_directory)
    update_global_progress(directory)

    send_new_event( ProgressValueChange(directory, key, value, max_value) )


def get_data_progress(directory):
    return get_directory_request_data(directory, "progress", None)

def set_data_to_be_found(directory, need_spliter, amount, lstFicOk):    
    set_directory_request_data(directory, "to_be_found", {
        "need_spliter": need_spliter,
        "amount": amount,
        "lstFicOk": lstFicOk
    })

    send_new_event( ToBeFoundChange(directory, need_spliter, amount) )

def get_data_to_be_found(directory):
    return get_directory_request_data(directory, "to_be_found", None)

def delete_data_to_be_found(directory):
    delete_directory_request_data(directory, "to_be_found")
    

def set_data_spliter_start_date(directory, date):
    set_directory_request_data(directory, "spliter_start_date", date)

def get_data_spliter_start_date(directory):
    return get_directory_request_data(directory, "spliter_start_date", None)


def add_spliter_result(directory, name, date, find):
    spliter_result = get_directory_request_data(directory, "spliter_result", {})

    if "requests" not in spliter_result:
        spliter_result["requests"] = []
    spliter_result["requests"].append({
        "name": name,
        "date": date,
        "find": find
    })

    set_directory_request_data(directory, "spliter_result", spliter_result)

    send_new_event( SplitResultAdded(directory, name, date, find) )

def set_spliter_cumulative(directory, cumulative):
    spliter_result = get_directory_request_data(directory, "spliter_result", {})
    spliter_result["cumulative"] = cumulative
    set_directory_request_data(directory, "spliter_result", spliter_result)

def set_spliter_result_start(directory):
    spliter_result = get_directory_request_data(directory, "spliter_result", {})
    spliter_result["start"] = True
    set_directory_request_data(directory, "spliter_result", spliter_result)

    send_new_event( SplitStart(directory) )

def set_spliter_result_end(directory):
    spliter_result = get_directory_request_data(directory, "spliter_result", {})
    spliter_result["end"] = True
    set_directory_request_data(directory, "spliter_result", spliter_result)

    send_new_event( SplitEnd(directory) )

def delete_data_spliter(directory):
    delete_directory_request_data(directory, "spliter_result")
        

read_dex()
