# -*- coding: utf-8 -*-
"""
Created on November, 17 2016

@author: cvanderlei
This script create the file "P2N_VersionXXX.info" and update them.

Example P2N_Version_2_17-NOV-2016
"""

import time, os
VersionName = 'P2N_Version(2)'+time.strftime("%d-%b-%Y", time.localtime())+'.info'
VersionFile = open(VersionName, 'w')
VersionFile.close()

