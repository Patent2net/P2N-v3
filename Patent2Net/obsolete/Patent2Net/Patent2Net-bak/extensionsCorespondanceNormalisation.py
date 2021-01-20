# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 10:06:10 2020

@author: david
"""

import pandas as pd
import sister
import numpy as np
import os
# plongement lexicaux - words embenddings
# embedder = sister.MeanEmbedding(lang="en")
from  fuzzywuzzy import process
import pickle
from tqdm import tqdm
# Lecture du fichier de référence
from Patent2Net.P2N_Lib_Acad import  Nettoie, NoPunct
df = pd.read_csv('../Patent2Net/Resources/StanNorm2.csv', dtype=str, sep=';', encoding='utf-8')



        
#df2 = pd.read_csv('../Patent2Net/Resources/test.csv', dtype=str, sep=';', encoding='utf-8')

# loading patent file in P2N format to normalisze applicants
with open('tempoInconnus', 'rb') as ficRes:
    lstANorm = pickle.load(ficRes)

# with open('tempoInconnusP7-Large', 'rb') as ficRes:
#     lstANorm2 = pickle.load(ficRes)
Vus = []
# resulting files in case of recursive call to this script
# the applicant names contained here will be ignored !!!!
if "ExtendedStan.csv" in os.listdir('../Patent2Net'):
    df2 = pd.read_csv('../Patent2Net/ExtendedStan.csv', dtype=str, sep=';', encoding='utf-8')
    Vus =+ list(set(df2['Variation Name'].tolist() ))
else:
    pass
if "NotFound.csv" in os.listdir('../Patent2Net'):
    df3= pd.read_csv('../Patent2Net/NotFound.csv', dtype=str, sep=';', encoding='utf-8', header=None)
    Vus =+ df3[0].to_list()
else:
    pass


#lstANorm +=lstANorm2
lstANorm = list(set(lstANorm))
Norm = list(set(df['Norm'].tolist()))
Vari = list(set(df['Variation Name'].tolist()))


with tqdm(total=len(lstANorm), desc="computing", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
    
        
    for ch, ch1 in lstANorm:
        pbar.update(1)
        
        ch= ch.upper()
        ch = Nettoie(ch)
        try:
            ch = NoPunct(ch)
        except:
            print(ch)
            next
        if isinstance(ch, list):
            ch=ch[0]
        ch = ch.strip()
        if len(df.index[df['Variation Name'].str.strip() == ch] ) == 0:
            if ch not in Vus and len(ch)>2 and len(ch.split(' '))>2: 
               # if ch not in Norm and ch not in Vari:
                    #if ch not in process.extractOne(ch, df['Variation Name'].tolist()) or ch not in process.extractOne(ch, df['Norm'].tolist()):
                    toto= process.extractOne(ch, df['Variation Name'].str.upper().tolist())
                    #p
                    
                    if len(toto)>0 and toto [1]>85 and len(toto[0])>2:
                        indx =  df.index[df['Variation Name'] == toto[0]]
                        if len(indx) >0:
                            ligne = df['Norm'].iloc[indx].to_list()[0] + ';' + ch + '\n'
                            with open('ExtendedStan.csv', 'a') as ficRes:
                                ficRes.write(ligne)
                        else:
                            #print (ch, ' --> ', toto)
                            with open('NotFound.csv', 'a') as ficRes:
                                ficRes.write(ch + '\n')
                    else:
                        with open('NotFound.csv', 'a') as ficRes:
                            ficRes.write(ch + '\n')
                        print (ch)
             
                # else:
                #     pass
                
    # df ['delta'] = df['centroid'].apply(lambda x: fuzzy.norm(embedder(ch)-x))
    # print()
    # indx = df.index[df['delta'] == df ['delta'].min()]
    # if len(indx)>0:
    #     print ('ard')
    #     print (ch, ' --> ', df['Norm'].iloc[indx].tolist()[0])
    # else:
    #     print (ch, ' --> ', df['Norm'].iloc[indx].tolist()[0])

                    