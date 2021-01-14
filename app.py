# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:58:37 2020

@author: Admin
"""
import os
#import glob
from flask import Flask, render_template, request, send_file, Response
from flask_cors import CORS

#import time
import json
import zipfile
import io
import pathlib
import queue
#from urllib import parse
import requests

# static_folder call the emplacement of all the content who will work with the HTML. template_folder the emplacement of the HTML. \
#    In theory they don't have to be at Root.

app = Flask(__name__, static_url_path='', static_folder='.', template_folder='.') 

CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

class Config:
    num_bars = 3
    prog_inc = 10
    update_rate = 1

# Instantiate app_config
app_cfg = Config

import logging
from logging.handlers import RotatingFileHandler


class MessageAnnouncer:

    def __init__(self):
        self.listeners = []

    def listen(self):
        self.listeners.append(queue.Queue(maxsize=5))
        return self.listeners[-1]

    def announce(self, msg):
        # We go in reverse order because we might have to delete an element, which will shift the
        # indices backward
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]


announcer = MessageAnnouncer()
def AnnonceProgres(Appli, valActu, valMax):
    if valActu and valMax:
        valActu = "%.2f" % valActu 
        try:
            requests.get('http://localhost:5000/announce?appli=%s&ValActu=%s&valMax=%s' %(Appli, valActu, valMax) )
        except:
            pass
    else:
        pass # must be a error
#☻    print ('annnonce envoyée: ', pipo)

def AnnonceLog(Appli, texte):

    try:
        requests.get('http://localhost:5000/announce?appli=%s&log=%s' %(Appli+'Log', texte) )
    except:
        pass

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
@app.route('/home' , methods=['GET','POST'])
@app.route('/' , methods=['GET','POST'])
def home():
    return render_template("Patent2Net/templates/Request_Form/P2N.html" , num_bars = 1)




@app.route('/progress' , methods=['GET','POST'])
def progress():
        #Launch the P2N research
        #os.system(cmd)
        form_result =  request.args
        AppLab = [lab for lab in lstAppl if form_result [lab] and lab not in ['p2n_dir']]
        app_cfg.num_bars = len(AppLab)
        return render_template('Patent2Net/templates/Request_Form/progress2.html', num_bars = app_cfg.num_bars, label = AppLab)

#    return render_template("Patent2Net/templates/Request_Form/Progress.html" , num_bars = 1)


#Single Request form

@app.route('/single_request' , methods=['GET','POST'])
@app.route('/form' , methods=['GET','POST'])
def form():
    #open the page P2N.html as default page
    return render_template("Patent2Net/templates/Request_Form/Request.html", num_bars = 1, label =[''])


#Single Request form confirmation route
@app.route('/confirmation', methods=['GET'])
def confirmation():
    # print (request.url)
    form_result =  request.args#dict(parse.parse_qsl(parse.urlsplit(request).query))

  # ['p2n_req','p2n_gather_biblio', "p2n_filtering", 'p2n_family','p2n_content','p2n_image','p2n_network','p2n_tables','p2n_carrot','p2n_iramuteq','p2n_cluster', ]

  
    AppLab = [labels [lab] for lab in lstAppl if form_result [lab] and lab not in ['p2n_dir']]
    

    
    app_cfg.num_bars = len(AppLab) - len([truc for truc in labels.keys() if not form_result [truc]] )
    return render_template('Patent2Net/templates/Request_Form/Progress2.html', num_bars = app_cfg.num_bars, label = AppLab)

@app.route('/confirmation', methods=['POST'])    
def CqlCreator():
    form_result = request.form

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
    AppLab = [lab for lab in lstAppl if lab not in ['p2n_dir', 'p2n_filtering'] and form_result [lab]]
        
    app_cfg.num_bars = len(AppLab) - len([truc for truc in AppLab if not form_result [truc]] )
    return render_template('Patent2Net/templates/Request_Form/Request.html', num_bars = app_cfg.num_bars, label = AppLab)

# @app.route('/progressBar' , methods=['GET','POST'])

# def progressBar():
#     def stream():
#         messages = announcer.listen()  # returns a queue.Queue
#         while True:
#             msg = messages.get()  # blocks until a new message arrives
#             yield msg

#     return Response(stream(), mimetype='text/event-stream')

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
    
    #msg = format_sse(data=json.dumps({"0":ValActu, "1":valMax}), event =Appli )
        dico = dict()
        dico[Appli] = ValActu
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
    return render_template("Patent2Net/templates/Request_Form/Get_Started.html")


# Get started page form interaction
@app.route('/get_started/stocked', methods=['GET','POST'])
def EpoCreator():
    epo_result= request.form
    print(epo_result)
    
    W_epo = open("./cles-epo.txt","wt")
    
    W_epo.write(epo_result['p2n_epo'])
    W_epo.close()
    
    return render_template("Patent2Net/templates/Request_Form/Get_Started.html")



#Access to the already existing index.html
@app.route('/index' , methods=['GET','POST'])
@app.route('/results' , methods=['GET','POST'])
def index():
    return render_template("index.html")


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
    os.system("./update.sh")
    return render_template("Patent2Net/templates/Request_Form/P2N.html" ,variable_vers= version)


@app.route('/mass', methods=['GET','POST'])
def mass():
    for file in os.listdir("./REQUESTS"):
        if file.endswith(".cql"):
                command="p2n run --config=../REQUESTS/%s"%(file)
                os.system(command)
    return render_template('Patent2Net/templates/Request_Form/ConfirmationP2N.html')

@app.route('/cqlList', methods=['GET','POST'])
def cqlList():
    lstReq = [fi for fi in os.listdir("./REQUESTS") if fi.endswith(".cql")]
    cpt = 0
    
    os.chdir("/home/p2n/P2N-V3/Patent2Net")
    

    app_cfg.num_bars = 12
    render_template('Patent2Net/templates/Request_Form/Mass2.html', num_bars = app_cfg.num_bars, label = labels.values())
    
    for file in lstReq:
            lstScripts = ["OPSGatherPatentsv2.py", "PatentListFiltering.py", 
                          "OPSGatherAugment-Families.py", "PatentListFiltering.py", "preProcessNormalisationNames.py",
                          "FormateExportCountryCartography.py", "FormateExportAttractivityCartography.py",
                          "FormateExportBiblio.py", "FormateExportDataTableFamilies.py", "FormateExportDataTable.py",
                          "FormateExportPivotTable.py", "P2N-Nets-new.py", "P2N-FreePlane.py", "OPSGatherAugment-Families.py",
                          "OPSGatherContentsV2-Iramuteq.py", "FusionIramuteq2.py", "OPSGatherAugment-Families.py",
                          "FusionCarrot2.py", "P2N-Indexer.py", "OPSGatherContentsV2-Images.py", "FusionImages.py",
                          "IPC-WS-metrics.py", "ClusterPreProcess.py", "P2N-Cluster.py", "Interface2.py"]
            cpt +=1
            AnnonceProgres (Appli = 'cql-files', valMax = len(lstReq), valActu = cpt)
            for cmd in lstScripts:
                command="python " + cmd + " ../REQUESTS/%s"%(file)               
                
                os.system(command)
                
    return render_template('Patent2Net/templates/Request_Form/Mass2.html', num_bars = app_cfg.num_bars, label = labels.values())

#Authorize the app to be accessed in a different environment (localhost in our case)
if __name__ == "__main__":
    # execute only if run as a script
    handler = RotatingFileHandler('p2n.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.run(debug=True, host='0.0.0.0', port=5000) 
