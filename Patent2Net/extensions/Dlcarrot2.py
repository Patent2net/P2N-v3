# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 13:24:47 2020
As:
1. the download url for binary distribution of carrot2 (hereafter a "hard coded" url of last version at the time of this script) is a redirection.
2. method for extracting url from html code in bash is out of my knowledge

this script is aimed to download carrot2 zip binary file.
@author: david
"""

import requests, sys
from bs4 import BeautifulSoup

if len(sys.argv)>1:
    dir = sys.argv[1]
else:
    dir = ''
url = 'https://github.com/carrot2/carrot2/releases/download/release%2F4.0.4/carrot2-4.0.4.zip'
with requests.get(url, stream = True) as req:

    fichier ='carrot2.zip'

    with open(dir+'/'+fichier, 'wb') as fic:
        for chunk in req.iter_content(chunk_size = 16*1024):
            fic.write(chunk)
