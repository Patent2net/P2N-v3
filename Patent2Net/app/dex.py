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
        
        write_dex()

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

start_progress("test")
set_progress_key("test", "prepare", 0, 100)

set_progress_key("test", "get", 20, 100)


set_progress_key("test", "final", 70, 100)