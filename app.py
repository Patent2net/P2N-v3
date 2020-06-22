# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:58:37 2020

@author: Admin
"""
import os
from flask import Flask, render_template, request


# static_folder call the emplacement of all the content who will work with the HTML. template_folder the emplacement of the HTML. In theory they don't have to be at Root.
app = Flask(__name__, static_url_path='', static_folder='.', template_folder='.') 
@app.route('/' , methods=['GET','POST'])
@app.route('/form' , methods=['GET','POST'])
def form():
    #open the page P2N.html as default page
    return render_template("Patent2Net/templates/Request_Form/P2N.html")


@app.route('/confirmation', methods=['GET','POST'])
def CqlCreator():
    form_result = request.form
    result = form_result['p2n_req']

    #Pleaceholder file who give the model of the file
    f_in = open("placeholder.cql", "rt")
    
    #create an output file with the name requested in the form by the user
    f_out = open("./RequestsSets/%s.cql" %form_result['p2n_req'] ,"wt")
    

#for each line in the input file    
    #read the values given in the form and replace the corresponding string in the output
    for name in f_in:
    	f_out.write(name.replace('RequestName', form_result['p2n_req'] ) \
                 .replace('RequestFamily', form_result['p2n_family']) \
                     .replace('RequestImage',form_result['p2n_image']) \
                    .replace('RequestNetwork',form_result['p2n_network']) \
                    .replace('RequestFreeplane',form_result['p2n_freeplane']) \
                    .replace('RequestBibfile',form_result['p2n_bibfile']) \
                    .replace('RequestMap',form_result['p2n_map']) \
                    .replace('RequestTable',form_result['p2n_tables']) \
                    .replace('RequestCarrot',form_result['p2n_carrot']) \
                    .replace('RequestIramuteq',form_result['p2n_iramuteq'])\
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
    
    
    return render_template('Patent2Net/templates/Request_Form/confirmationP2N.html',variable= result )


@app.route('/index' , methods=['GET','POST'])
def index():
    return render_template("index.html")

"""
@app.route('/lentille' , methods=['GET','POST'])
def result():
    #open the result page newly created
    return render_template("DATA/Lentille.html")
"""
#Permet d'accéder à l'app à partir d'un autre environnement (dans notre cas de figure le localhost)
app.run(debug=True,use_reloader=False, host='0.0.0.0') 
