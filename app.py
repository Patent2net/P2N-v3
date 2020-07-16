# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:58:37 2020

@author: Admin
"""
import os
import glob
from flask import Flask, render_template, request, send_file
import zipfile
import io
import pathlib

# static_folder call the emplacement of all the content who will work with the HTML. template_folder the emplacement of the HTML. In theory they don't have to be at Root.
app = Flask(__name__, static_url_path='', static_folder='.', template_folder='.') 


""" P2N Docker App Version: """

version = "0.371"


""" Definition of the differents app pages  """
#Home page

@app.route('/home' , methods=['GET','POST'])
@app.route('/' , methods=['GET','POST'])
def home():
    return render_template("Patent2Net/templates/Request_Form/P2N.html" ,variable_vers= version)




#Single Request form

@app.route('/single_request' , methods=['GET','POST'])
@app.route('/form' , methods=['GET','POST'])
def form():
    #open the page P2N.html as default page
    return render_template("Patent2Net/templates/Request_Form/Request.html")



#Single Request form confirmation route
@app.route('/confirmation', methods=['GET','POST'])
def CqlCreator():
    form_result = request.form

    #Pleaceholder file who give the model of the file
    f_in = open("placeholder.cql", "rt")
    
    #create an output file with the name requested in the form by the user
    f_out = open("./RequestsSets/%s.cql" %form_result['p2n_req'] ,"wt")
    

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
           


    #Return values of the form for testing the acquisition (Verification of working script)
    with open ('result.txt', 'w') as fp:
        for p in form_result.items():
            fp.write("%s:%s\n" % p)
    
    #close input and output files
    f_in.close()
    f_out.close()
    
    #Launch the P2N research
    command="p2n run --config=../RequestsSets/%s.cql"%(form_result['p2n_req'])
    os.system(command)
    
    
    return render_template('Patent2Net/templates/Request_Form/ConfirmationP2N.html',variable= form_result['p2n_req'] )



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
@app.route('/download', methods=['GET','POST'])
def request_zip():
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

@app.route('/updateP2N', methods=['GET','POST'])
def gitupdater():
    #Launch the P2N research
    commandupdate="git pull"
    os.system(commandupdate)
    return render_template("Patent2Net/templates/Request_Form/P2N.html" ,variable_vers= version)


@app.route('/mass', methods=['GET','POST'])
def mass():
    for file in os.listdir("./RequestsSets"):
        if file.endswith(".cql"):
                command="p2n run --config=../RequestsSets/%s"%(file)
                os.system(command)
    return render_template('Patent2Net/templates/Request_Form/ConfirmationP2N.html')

#Authorize the app to be accessed in a different environment (localhost in our case)
app.run(debug=True, host='0.0.0.0') 
