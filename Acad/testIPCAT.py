# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 11:34:27 2019

@author: dreymond
"""

# DOC de l'API : https://www.wipo.int/ipc/itos4ipc/ITSupport_and_download_area/Documentation/IPC_Internet_URL_Web_Services_specification/IPC_Internet_Publication_URLs_and_Services_V7.0.pdf

import requests
from requests.utils import requote_uri

#from xml.etree import ElementTree
# Eléments de paramétrage
version="20190101" #valid scheme version
language="en" # or fr, es, de, ru
number="5" #from 1 to 5
level= "subgroup" # or class, subclass, maingroup
#the text to be classified
text= u"""It is hard to observe dynamics of technological change of a complex product  because  of  the  diversity  of  component  and  system  technologies composing the complex product. In spite of this difficulty, companies need to identify  their  competitive  advantages  and  disadvantages  in  technology development.  The  aim  of  this  study  is  to  propose  a  method  to  observe  the dynamic changes in technology development of the complex product. Existing studies  provide  methods  to  observe  this  changes,  but  those  provide  either overall view or focus on specific changes. The method developed in this study not only shows overall trends but also makes it possible to make comparisons among companies. The  analysis  results  using  this  tool  may  help  to  get information about the changes without the aid of experts, and the information also may be used to mitigate bias when using experts."""

# Call the service
urlCat="https://www.wipo.int/classifications/ipc/ipcpub/search/fullipccat/"\
    +version+"/"+language+"/"+level+"/"+number+"/none/"+text+"/"
urlCat=requote_uri(urlCat)
req = requests.get(urlCat)
data2 = req.text
result=req.json()
##result contains the predicted IPC symbols within the catalog version
urlDer = "http://www.wipo.int/classifications/ipc/ipccat?&hierarchiclevel="+level.upper()+"&lang="+language +\
"&numberofpredictions="+number+"&text="+text
urlDer = requote_uri(urlDer)
requeste=requests.get(urlDer)
# Là on obtient du XML
# une information supplémentaire est le score cf. doc p. 27 de 0 à 1600
# avec le même résultat qu'avec la première URL qui est lui au format json
data3 = requeste.text 
#☺result=json.loads(data3)
#Et on retrouve bien pour le premier (result) le résultat affiché dans les prédictions pour 
#le même texte passé à l'interface Web : https://www.wipo.int/classifications/ipc/ipcpub/

#2	G06Q 10/06	
#2	G06Q 10/10	
#2	G06Q 10/00	
#2	G06Q 50/18	
#2	G06Q 30/00