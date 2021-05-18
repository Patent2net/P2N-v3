# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:58:37 2020

@author: Admin
"""
import os
#import glob
from flask import Flask, render_template, request, send_file, Response, send_from_directory, jsonify, redirect, url_for
from flask_cors import CORS

#import time
import json
import zipfile
import io
import pathlib
import queue
#from urllib import parse
import requests
import asyncio
import epo_ops

from Patent2Net.app.dex import get_current_dex, read_dex, set_in_progress, set_done, set_data_progress, get_data_progress, get_global_progress, set_state, get_state, get_directory_request_data_all, delete_data_to_be_found, get_data_to_be_found, set_data_spliter_start_date, delete_data_spliter
from Patent2Net.app.events.progress_value_change import ProgressValueChange
from Patent2Net.app.events.to_be_found_change import ToBeFoundChange
from Patent2Net.app.events.split_end import SplitEnd
from Patent2Net.app.event import EventListener
from Patent2Net.P2N_Config import LoadConfig
from Patent2Net.AutomRequestSpliterTime import autom_request_spliter_time
from Patent2Net.P2N_Lib import PatentSearch
from p2n.config import OPSCredentials
import threading
import subprocess
from subprocess import Popen

from p2n.util import run_script

# static_folder call the emplacement of all the content who will work with the HTML. template_folder the emplacement of the HTML. \
#    In theory they don't have to be at Root.

app = Flask(__name__, static_url_path='', static_folder='./Patent2Net/static/', template_folder='./Patent2Net/templates_flask') 

CORS(app)

os.environ['PYTHONPATH'] = os.getcwd()
os.environ['REQUESTS_CA_BUNDLE'] = 'Patent2Net/cacert.pem'
app.config['CORS_HEADERS'] = 'Content-Type'

class Config:
    num_bars = 3
    prog_inc = 10
    update_rate = 1
    

# Instantiate app_config
app_cfg = Config

import logging
from logging.handlers import RotatingFileHandler
from Patent2Net.app.message_announcer import MessageAnnouncer

announcer = MessageAnnouncer()
eventListener = EventListener()

def format_sse(data: str, event=None) -> str:
    """Formats a string and an event name in order to follow the event stream convention.

    >>> format_sse(data=json.dumps({'abc': 123}), event='Jackson 5')
    'event: Jackson 5\\ndata: {"abc": 123}\\n\\n'

    """
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg


# @app.route('/announcer')
# def ping():
#     Appli = request.args.get("appli")
#     ValActu = request.args.get("ValActu")
#     valMax = request.args.get("valMax")
    
#    #msg = format_sse(data=json.dumps({"0":ValActu, "1":valMax}), event =Appli )
#     dico = dict()
#     dico[Appli] = ValActu
#     msg="data:" + json.dumps(dico) + "\n\n"
#     announcer.announce(msg=msg)
#     return {}, 200





#messages = sseclient.SSEClient('http://localhost:30000/listen')

""" P2N Docker App Version: """

version = "0.5"
#list of application controled actually (approximativelly)

lstAppl = ['cql-files', 'p2n_req','p2n_gather_biblio', "p2n_filtering", 'p2n_family','p2n_content',
           'p2n_image','p2n_network','p2n_tables','p2n_carrot','p2n_iramuteq','p2n_cluster',
           'p2n_indexer']
lstAppl2 = [truc + 'Log' for truc in lstAppl]

labels = { 'p2n_req' : "Gathering patent list",
              'p2n_gather_biblio' : "Gathering bibliographic metadata", 
              "p2n_filtering" : "Filtering patents", 
              'p2n_family' : "Gathering families",
              'p2n_content' : "Gathering content",
              'p2n_image' :  "Gathering images",
              'p2n_network' : "Processing networks",
              'p2n_tables' : "Processing tables",
              'p2n_carrot' :  "Preparing carrot2 files",
              'p2n_iramuteq' : "Processing IRAMuTeQ files",
              'p2n_cluster' : "Clustering",
              'p2n_indexer': "Indexing documents",
              'cql-files': "Processing request file",  
              }

# unused: "p2n_filtering", "
""" Definition of the differents app pages  """
#Home page





#---------------------------------------
# App Routes
#---------------------------------------
# @app.route('/home' , methods=['GET','POST'])
# @app.route('/' , methods=['GET','POST'])
# def home():
#     return render_template("P2N.html" , num_bars = 1)




@app.route('/progress' , methods=['GET','POST'])
def progress():
        #Launch the P2N research
        #os.system(cmd)
        form_result =  request.args
        AppLab = [lab for lab in lstAppl if lab not in ['p2n_dir', 'cql-files', 'p2n_indexer'] and  form_result [lab]]
        app_cfg.num_bars = len(AppLab)
        return render_template('progress2.html', num_bars = app_cfg.num_bars, label = AppLab)

#    return render_template("Patent2Net/templates/Request_Form/Progress.html" , num_bars = 1)


#Single Request form

# GET request : Affiche le formulaire de requete

@app.route('/single_request' , methods=['GET','POST']) # ancienne url
@app.route('/form' , methods=['GET','POST']) # ancienne url
def form():
    # return render_template("Request.html", num_bars = 1, label =[''], dex = dex)
    return redirect("/app/requests", code=301)

# POST requests : Créer une requete

@app.route('/confirmation', methods=['POST']) # ancienne url
def confirmation_post():
    form_result = request.form
    p2n_dir = form_result['p2n_dir']

    #Pleaceholder file who give the model of the file
    f_in = open("placeholder.cql", "rt")
    
    #create an output file with the name requested in the form by the user
    f_out = open("./RequestsSets/%s.cql" %form_result['p2n_dir'] ,"wt")
    

    #for each line in the input file    
    #read the values given in the form and replace the corresponding string in the output
    for name in f_in:
    	f_out.write(name.replace('RequestName', form_result['p2n_req'] ) \
                .replace('RequestDirectory', form_result['p2n_dir']) \
                .replace('RequestFamily', form_result['p2n_family']) \
                .replace('RequestImage',form_result['p2n_image']) \
                .replace('RequestNetwork',form_result['p2n_network']) \
                .replace('RequestFreeplane',form_result['p2n_freeplane']) \
                .replace('RequestBibfile',form_result['p2n_bibfile']) \
                .replace('RequestMap',form_result['p2n_map']) \
                .replace('RequestTable',form_result['p2n_tables']) \
                .replace('RequestCarrot',form_result['p2n_carrot']) \
                .replace('RequestIramuteq',form_result['p2n_iramuteq'])\
                .replace('RequestCluster',form_result['p2n_cluster'])\
                )
        
    # if form_result['p2n_iramuteq'] or form_result['p2n_cluster'] or form_result['p2n_carrot']:
    #     form_result['p2n_content'] = True
    #     form_result['p2n_gather_biblio'] = True
    # if form_result['p2n_tables'] or form_result['p2n_freeplane'] or form_result['p2n_network'] or form_result['p2n_map']:
    #     form_result['p2n_gather_biblio'] = True  
    #     form_result['p2n_content'] = False
    #Return values of the form for testing the acquisition (Verification of working script)
    with open ('result.txt', 'w') as fp:
        for p in form_result.items():
            fp.write("%s:%s\n" % p)

    # print (app_cfg.num_bars, ' --> ',  lstAppl)
    #close input and output files
    f_in.close()
    f_out.close()
    
    # #Launch the P2N research
    command="p2n run --config=../RequestsSets/%s.cql"%(form_result['p2n_dir'])
    os.system(command) 
    #subprocess.call('python ./Patent2Net/OPSGatherPatentsv2.py --config="./RequestsSets/%s.cql"')
#    progress(command, form_result)
    #
    
    print ('starting')
    
    #form_result['p2n_filtering'] = True #
    AppLab = [lab for lab in lstAppl if lab not in ['p2n_dir', 'p2n_filtering', 'p2n_indexer'] and form_result [lab]]
        
    app_cfg.num_bars = len(AppLab) - len([truc for truc in AppLab if  truc not in ['p2n_dir', 'cql-files', 'p2n_indexer'] and not form_result [truc]] )
   
    return render_template('Request.html', num_bars = app_cfg.num_bars, label = AppLab)


# @app.route('/requests', methods=['POST'])    
# def post_request_test():
#     form_result = request.form
#     p2n_dir = form_result['p2n_dir']

#     # NEW PROGRESS SYSTEME - 23/04/2021
    
#     labels_keys = labels.keys()
#     active_labels_keys = [label_key for label_key in labels_keys if label_key not in ['p2n_dir', 'p2n_filtering', 'p2n_indexer'] and label_key in form_result and form_result [label_key]]

#     start_progress(p2n_dir)

#     for label_key in active_labels_keys:
#         set_progress_key(p2n_dir, label_key, None, None)

#     return redirect('requests/' + p2n_dir)

#Single Request form confirmation route
@app.route('/confirmation', methods=['GET'])
def confirmation():
    form_result =  request.args

    # ['p2n_req','p2n_gather_biblio', "p2n_filtering", 'p2n_family','p2n_content','p2n_image','p2n_network','p2n_tables','p2n_carrot','p2n_iramuteq','p2n_cluster', ]

    AppLab = [labels [lab] for lab in lstAppl if lab not in ['p2n_dir', 'cql-files', 'p2n_indexer'] and  form_result [lab]]
    
    app_cfg.num_bars = len(AppLab) - len([truc for truc in labels.keys() if truc not in ['p2n_dir', 'cql-files', 'p2n_indexer'] and not form_result [truc]] )
    return render_template('Progress2.html', num_bars = app_cfg.num_bars, label = AppLab)



# API v1

@app.route('/api/v1/requests', methods=['GET'])
def get_requests():
    dex = get_current_dex()
    return get_success_response(
        "",
        {
            "done": dex["done"],
            "in_progress": dex["in_progress"],
            "global_progress": get_global_progress()
        }
    )

@app.route('/api/v1/requests', methods=['POST'])
def post_request():
    form_result = request.form
    if 'p2n_dir' not in form_result:
        return get_error_response("p2n_dir is required")
    if 'p2n_req' not in form_result:
        return get_error_response("p2n_req is required")
    if 'p2n_options' not in form_result:
        return get_error_response("p2n_options is required")

    p2n_dir = form_result['p2n_dir']
    p2n_req = form_result['p2n_req']
    p2n_options = form_result['p2n_options'].split(',')
    p2n_auto = 'p2n_auto' in form_result and form_result['p2n_auto'] == "true"

    #Pleaceholder file who give the model of the file
    f_in = open("placeholder.cql", "rt")
    
    # #create an output file with the name requested in the form by the user
    target_path = "./RequestsSets/%s.cql" %form_result['p2n_dir']
    f_out = open(target_path ,"wt")

    def get_option_value(name):
        return 'True' if name in p2n_options else 'False'

    #for each line in the input file    
    #read the values given in the form and replace the corresponding string in the output
    for name in f_in:
    	f_out.write(name.replace('RequestName', p2n_req ) \
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
                )
    
    #Return values of the form for testing the acquisition (Verification of working script)
    with open ('result.txt', 'w') as fp:
        for p in form_result.items():
            fp.write("%s:%s\n" % p)

    #close input and output files
    f_in.close()
    f_out.close()

    config = "--config=../RequestsSets/%s.cql"%(form_result['p2n_dir'])
    
    labels_keys = labels.keys()
    active_labels_keys = [label_key for label_key in labels_keys if label_key not in ['p2n_dir', 'p2n_filtering', 'p2n_indexer'] and label_key in p2n_options]

    for label_key in active_labels_keys:
        set_data_progress(p2n_dir, label_key, None, None)


    if (p2n_auto == True):
        process_multi(p2n_dir, target_path)
        return get_success_response("Spliter start", { "p2n_dir": p2n_dir })
    else:
        process_single(p2n_dir, config)
        return get_success_response("Request send", { "p2n_dir": p2n_dir })

   
def process_single(p2n_dir, config):
    print("PROGRESS SINGLE: " + p2n_dir)

    set_in_progress(p2n_dir)
    set_state(p2n_dir, "P2N_RUN")
    p = Popen(['p2n', 'run', config])
    
def process_multi(p2n_dir, target_path):
    print("PROGRESS MULTI: " + p2n_dir)

    set_in_progress(p2n_dir)
    set_state(p2n_dir, "SPLITER_RUN")
    delete_data_to_be_found(p2n_dir)
    p = Popen(['python', 'Patent2Net/scripts/update_to_be_found.py', target_path])



@app.route('/api/v1/requests/<p2n_dir>', methods=['GET'])
def get_one_request(p2n_dir):
    dex = get_current_dex()

    configFile = LoadConfig(p2n_dir + ".cql")

    return get_success_response("", {
        "done": p2n_dir in dex["done"],
        "state": get_state(p2n_dir),
        "data": get_directory_request_data_all(p2n_dir),
        "progress": get_data_progress(p2n_dir),
        "directory": p2n_dir,
        "cql": {
            "requete": configFile.requete,
            "ndf": configFile.ndf,
            "options": {
                "GatherContent": configFile.GatherContent,
                "GatherBiblio": configFile.GatherBiblio,
                "GatherPatent": configFile.GatherPatent,
                "GatherFamilly": configFile.GatherFamilly
            }
        }
    })

@app.route('/api/v1/requests/<p2n_dir>/split', methods=['POST'])
def split_request(p2n_dir):
    form_result = request.form

    read_dex()
    to_be_found = get_data_to_be_found(p2n_dir)

    if not to_be_found:
        return get_error_response("Patent amount for this request not found")

    if "date" not in form_result:
        return get_error_response("date parameter is required")

    date = form_result["date"]
    target_path = "./RequestsSets/%s.cql" %p2n_dir

    if to_be_found["need_spliter"]:
        set_data_spliter_start_date(p2n_dir, int(date))
        # p = Popen(['python', 'Patent2Net/scripts/run_spliter.py', target_path])

        # Popen(['python', 'Patent2Net/scripts/start_auto.py', target_path])

        return get_success_response("Spliter running", {})

    return get_error_response("Spliter not needed for this directory")

@app.route('/api/v1/requests/<p2n_dir>/interface', methods=['POST'])
def update_one_request_interface(p2n_dir):
    print(p2n_dir)
    os.chdir("/home/p2n/P2N-V3/")
    os.chdir("/home/p2n/P2N-V3/Patent2Net")

    command="python Interface2.py ../RequestsSets/%s"%(p2n_dir) + ".cql"           
    os.system(command)

    return get_success_response("OK", {
        "directory": p2n_dir
    })

@app.route('/api/v1/events', methods=['POST'])
def events():
    """
    The events received allow to inform about a change of state already active
    The list of events can be found in /Patent2Net/app/events/
    """
    data = request.json
    name = data["name"]
    print(data)

    if name == ToBeFoundChange.NAME:
        event = ToBeFoundChange.deserialize(data)

        if event.need_spliter == False:
            config = "--config=../RequestsSets/%s.cql"%(event.directory)
            process_single(event.directory, config)

    eventListener.push_event(data)

    return get_success_response("ok", {})

@app.route('/api/v1/listen', methods=['GET'])
def listen_hook():

    def stream():
        events = eventListener.listen()  # returns a queue.Queue
        while True:
            event = events.get()  # blocks until a new message arrives
            print(event)
            msg = msg="data:" + json.dumps(event) + "\n\n"
            yield msg
            
    res = Response(stream(), mimetype='text/event-stream')

    return res


def get_error_response(message, code = 400):
    return Response(response=json.dumps({ "code": code, "message": message }), status=code, mimetype="application/json")

def get_success_response(message, data):
    response = ({ "code": 200, "message": message, "data": data })
    return Response(response=json.dumps(response), status=200, mimetype="application/json")


@app.route('/announce')
def annonce():
    # expects a requests.get('http://localhost:5000/annonce?appli=0&ValActu='+str(random.randint(0,101))+'&valMax=30') 
    # appli is the emiter application should be in this list lstAppl = ['p2n_req','p2n_gather_biblio', 'p2n_content', 'p2n_family','p2n_image','p2n_network','p2n_tables','p2n_carrot','p2n_iramuteq','p2n_cluster']
    # valActu the actual step in progress
    # valMax the max value to reach
    # this will be pass to the AnnonceProgres function
    
    # FIX needed. After providing announce feature for log, the code below is silly....
    appli = request.args.get("appli")
    if appli in lstAppl:
        Appli = lstAppl.index(appli)
        ValActu = request.args.get("ValActu")
        valMax = request.args.get("valMax")


        dex = get_current_dex()
        for element in dex["in_progress"]:
            set_data_progress(element, appli, ValActu, valMax)
    
    #msg = format_sse(data=json.dumps({"0":ValActu, "1":valMax}), event =Appli )
        dico = dict()
        dico[Appli] = ValActu
        dico["data"] = {}
        dico["data"][appli] = {
            "value": ValActu,
            "max_value": valMax
        }

        msg="data:" + json.dumps(dico) + "\n\n"
    else:
        Appli =  lstAppl.index(appli.replace('Log', ''))#.replace('Log', '')
        txt = request.args.get("log")
        dico = dict()
        dico[Appli] = 'LOG'+txt
        msg="data:" + json.dumps(dico) + "\n\n"
    announcer.announce(msg=msg)
    return {}, 200



@app.route('/listen', methods=['GET'])
def listen():

    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg
    res = Response(stream(), mimetype='text/event-stream')

    return res



@app.route('/get_started', methods=['GET','POST'])
def started():
    # return render_template("Get_Started.html")
    return redirect("/app/get_started", code=301)


# Get started page form interaction
@app.route('/get_started/stocked', methods=['GET','POST'])
def EpoCreator():
    epo_result= request.form
    print(epo_result)
    
    W_epo = open("./cles-epo.txt","wt")
    
    W_epo.write(epo_result['p2n_epo'])
    W_epo.close()
    
    # return render_template("Get_Started.html")
    redirect("/app/get_started", code=301)



#Access to the already existing index.html
@app.route('/index' , methods=['GET','POST'])
@app.route('/results' , methods=['GET','POST'])
def index():
    return redirect("/app/index", code=301)


# Download def for when clicking on "Download Data"
@app.route('/downloadDat', methods=['GET','POST'])
def requestData_zip():
    base_path = pathlib.Path('./DATA/')
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in base_path.iterdir():
            z.write(f_name)
    data.seek(0)
    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='DATA.zip'
    )

@app.route('/downloadReq', methods=['GET','POST'])
def requestReqSet_zip():
    base_path = pathlib.Path('./RequestsSets/')
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in base_path.iterdir():
            z.write(f_name)
    data.seek(0)
    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='RequestsSets.zip'
    )

@app.route('/updateP2N', methods=['GET','POST'])
def gitupdater():
    #Launch the P2N research
    # commandupdate="git pull"
    # os.system(commandupdate)
    # os.system("python setup.py build")
    # os.system("python setup.py install")
    os.chdir("/home/p2n/P2N-V3/")
    os.system("./update.sh")
    return render_template("P2N.html" ,variable_vers= version)


# @app.route('/mass', methods=['GET','POST'])
# def mass():
#     for file in os.listdir("./RequestsAuto"):
#         if file.endswith(".cql"):
#                 command="p2n run --config=../REQUESTS/%s"%(file)
#                 os.system(command)
#     return render_template('Patent2Net/templates/Request_Form/ConfirmationP2N.html')

@app.route('/cqlList', methods=['GET','POST'])
def cqlList(): 
    if request.method == 'GET':
        app_cfg.num_bars = 12
        return render_template('Mass2.html', num_bars = app_cfg.num_bars, label = labels.values())

    if request.method == 'POST':
        # processList(app_cfg)
        return "done"

    return render_template('Mass2.html', num_bars = app_cfg.num_bars, label = labels.values())


@app.route('/DATA/<path:filename>')
def data_static(filename):
    return send_from_directory("DATA", filename)

@app.route('/Patent2Net/media/<path:filename>')
def media_static(filename):
    return send_from_directory("Patent2Net/media", filename)

@app.route('/dex.js')
def dex():
    return send_file("dex.js")

@app.route('/doc/<path:path>')
def doc_static(path):
    return send_from_directory("doc/", path)

@app.route('/app/static/<path:filename>', methods=['GET'])
def request_app_static(filename):
    return send_from_directory("web_app/build/static/", filename)

# Redirection vers l'app Request

@app.route('/', defaults={'path': None})
@app.route('/app', defaults={'path': None})
@app.route('/app/', defaults={'path': None})
@app.route('/app/<path:path>', methods=['GET'])
def request_app(path):
    return send_file("web_app/build/index.html")


#Authorize the app to be accessed in a different environment (localhost in our case)
if __name__ == "__main__":
    # execute only if run as a script
    # handler = RotatingFileHandler('p2n.log', maxBytes=10000, backupCount=1)
    # handler.setLevel(logging.INFO)
    # app.logger.addHandler(handler)

    app.run(debug=False, host='0.0.0.0', port=5000) 



def popen_and_call(on_exit, popen_args):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    on_exit when the subprocess completes.
    on_exit is a callable object, and popen_args is a list/tuple of args that 
    would give to subprocess.Popen.
    """
    def run_in_thread(on_exit, popen_args):
        proc = subprocess.Popen(popen_args)
        proc.wait()
        on_exit()
        return
    thread = threading.Thread(target=run_in_thread, args=(on_exit, popen_args))
    thread.start()
    # returns immediately after the thread starts
    return thread