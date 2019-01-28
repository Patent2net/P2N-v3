# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 14:38:28 2019

@author: david
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 16:38:24 2018

@author: claro
"""

import requests

YOUR_EMAIL = "clarougalliano@outlook.com" # you should put your own email address here

def unpaywall(doi, retry=0, pdfonly=True):
    """Find legal open access version of paper"""


    r = requests.get("https://api.unpaywall.org/v2/{}".format(doi), params={"email":YOUR_EMAIL})
    
    if r.status_code == 404:
        print("Invalid/unknown DOI {}".format(doi))
        return None
    
    if r.status_code == 500:
        print("Unpaywall API failed. Try: {}/3".format(retry+1))
        
        if retry < 3:
            return unpaywall(doi, retry+1)
        else:
            print("Retried 3 times and failed. Giving up")
            return None
    
    best_loc = None
    try:
        best_loc = r.json()['best_oa_location']
    except json.decoder.JSONDecodeError:
        print("Response was not json")
        print(r.text)
    except KeyError:
        print("best_oa_location not set")
        print(r.text)
    except:
        print("Something weird happened")
        print(r.text)
        return None
        
    
    if not r.json()['is_oa'] or best_loc is None:
        print("No OA paper found for {}".format(doi))
        return None
        
    if(best_loc['url_for_pdf'] is None and pdfonly is True):
        print("No PDF found..")
        print(best_loc)
        return None
    else:
        return best_loc['url']
    
    return best_loc['url_for_pdf']

DOI = "https://doi.org/10.1016/j.jacc.2004.10.055"
DOI2 ="https://doi.org/10.2202/2152-2812.1030"
UrlArt = unpaywall(DOI2)
print (UrlArt)