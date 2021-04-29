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

def read_dex():
    global dex

    try:      
        with open(dex_location) as f:
            dex = json.load(f) 
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
    normalize()
    return dex

def normalize():
    global dex
    if "in_progress" not in dex:
        dex["in_progress"] = []
    if "done" not in dex:
        dex["done"] = []
    if "progress" not in dex:
        dex["progress"] = {}
    if "global_progress" not in dex:
        dex["global_progress"] = {}

    write_dex()

def start_progress(directory):
    global dex
    normalize()

    in_progress = dex["in_progress"]
    if directory not in in_progress:
        in_progress.append(directory)
        dex["progress"][directory] = {}
        
    write_dex()

def set_progress_key(directory, key, value, max_value):
    global dex
    normalize()

    progress = dex["progress"]
    if directory in progress:
        progress_directory = dex["progress"][directory]

        if key not in progress_directory:
            progress_directory[key] = {}

        progress_directory[key]["value"] = value
        progress_directory[key]["max_value"] = max_value

        update_global_progress(directory)

        write_dex()

def update_global_progress(directory):
    global dex
    normalize()

    progress = dex["progress"]
    if directory in progress:
        progress_directory = progress[directory]

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
        
        dex["global_progress"][directory] = {
            "done_step_count": done_step_count,
            "progress_step_count": progress_step_count,
            "total_step_count": total_step_count
        }

def done_progress(directory):
    global dex
    normalize()

    in_progress = dex["in_progress"]
    done = dex["done"]

    if directory in in_progress:
        in_progress.remove(directory)
    if directory not in done:
        done.append(directory)

    write_dex()

read_dex()