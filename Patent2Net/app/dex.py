import json
import sys, os

# ---------------------------- #
# NEW DEX SYSTEME - 23/04/2021 #
# ---------------------------- #

dex = {
    "in_progress": [],
    "done": []
}
dex_location = os.path.dirname(os.path.realpath(__file__)) + '/../../dex.json'
print(dex_location)


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
                print(in_progress_elmt)
                update_global_progress(in_progress_elmt)

    except IOError:
        print("WRITE DEFAULT")
        write_dex()

def write_dex():
    global dex

    f = open(dex_location, "w")
    f.write(json.dumps(dex))
    f.close()

def get_current_dex():
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

# state: "P2N_RUN" | "SPLITER_NEED_RUN" | "SPLITER_RUN" | "SPILTER_YEAR_INPUT" 
def set_state(directory, state):
    request_directory = normalize_request_directory(directory)
    request_directory["state"] = state

def set_in_progress(directory):
    global dex
    normalize()

    in_progress = dex["in_progress"]
    if directory not in in_progress:
        in_progress.append(directory)

    write_dex()

def set_done(directory):
    global dex
    normalize()

    in_progress = dex["in_progress"]
    done = dex["done"]

    if directory in in_progress:
        in_progress.remove(directory)
    if directory not in done:
        done.append(directory)

    write_dex()

# DATA

def set_directory_request_data(directory, key, value):
    normalize()
    request_directory = normalize_request_directory(directory)

    request_directory["data"][key] = value

    write_dex()


def get_directory_request_data(directory, key, default = None):
    normalize()
    request_directory = normalize_request_directory(directory)

    if key not in request_directory["data"] or request_directory["data"][key] == None:
        return default

    return request_directory["data"][key]


# GLOBAL PROGRESS

def update_global_progress(directory):
    global dex, global_progress
    normalize()

    progress_directory = get_directory_request_data(directory, "progress", {})

    print("progress_directory: " + str(progress_directory))

    done_step_count = 0
    progress_step_count = 0
    total_step_count = len(progress_directory)

    for step_key in progress_directory:
        step = progress_directory[step_key]
        print(step_key, step)
        if step["value"] != None and step["max_value"] != None:
            print(step["value"], step["max_value"])
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
    global global_progress

    return global_progress


# UTILS

def set_data_progress(directory, key, value, max_value):
    global dex
    normalize()
    
    progress_directory = get_directory_request_data(directory, "progress", {})

    if key not in progress_directory:
        progress_directory[key] = {}

    progress_directory[key]["value"] = value
    progress_directory[key]["max_value"] = max_value

    set_directory_request_data(directory, "progress", progress_directory)
    update_global_progress(directory)

def get_data_progress(directory):
    return get_directory_request_data(directory, "progress", None)

read_dex()
