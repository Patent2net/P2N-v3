# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 07:41:54 2019

@author: dreymond
"""


import codecs
import os, sys

from tqdm import tqdm

import pandas as pd
import string
import re
import unidecode
from tqdm import tqdm


xlsx = pd.ExcelFile('./Resources/EntitésPubliquesNorm.xlsx')
Public = []
TypeAppl = dict()
#df = pd.read_csv('../Patent2Net/Resources/STANNORM2.csv', dtype=str, sep=';', encoding='utf-8')
df = pd.read_excel('../Patent2Net/Resources/StanNORM2.xlsx', dtype=str, encoding='utf-8')

with pd.ExcelWriter('./Resources/EntitésPubliquesNorm2.xlsx') as writer:
    
    for sheet in xlsx.sheet_names:
       dicotemp = xlsx.parse(sheet).to_dict(orient='list')
       
       for cle, val in dicotemp.items():
            tempoRes = []
            with tqdm(total=len(val), desc="computing", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
            
                for appli in val:
                    pbar.update(1)
                    appli=appli.strip()

                    

                    indx = df.index[df['Variation Name'] == appli] | df.index[df['Norm'] == appli]
                    if len(indx)==0:
                        indx = df.index[df['Variation Name'] == appli.upper()] | df.index[df['Norm'] == appli.upper()]
                        if len(indx)==0:
                            print (appli)
                            # these should only be column titles
                            #tempoRes.append(appli)                                    
                        else:                           
                            joliNom = df['Norm'].iloc[indx].to_list()[0]
                            tempoRes.append(joliNom)
                    else:
                        joliNom = df['Norm'].iloc[indx].to_list()[0]
                        tempoRes.append(joliNom)
            tempores = list(set(tempoRes))       
            tempores.sort()
            df2 = pd.DataFrame(tempores, columns = [cle])   
            print (cle)
            df2.to_excel(writer, sheet_name=cle, index = False)
    

       
