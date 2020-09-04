# -*- coding: utf-8 -*-
# (c) 2015 David Reymond
import os
from Patent2Net.P2N_Lib import LoadBiblioFile

def read(path, slot):

    filename = 'Description' + slot
    if filename in os.listdir(path):
        data = LoadBiblioFile(path, slot)
        return data
