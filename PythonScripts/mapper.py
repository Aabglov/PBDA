#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import sys


for record in sys.stdin:
    data = record.replace('\n','').split(",")
    try:
        value = [float(x) for x in data[2:13]]
        outString = data[0] + ',' + data[1] + '\t' + str(value).replace('[',' ').replace(']','')
        print(outString)
        #print(value)
    except: # ValueError
        pass
sys.exit()
    
    
