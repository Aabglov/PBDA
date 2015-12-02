#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

countyDict = {}
p = 9
for string in sys.stdin:
    data = string.replace("\n","").split("\t")
    key = data[0].split(',')[0]
    lst = data[1].split(',')
    value = [float(x) for x in lst]
    for i in range(p):
        value[i] *= value[p]
    if countyDict.get(key) is None:
        countyDict[key] = value
    else:
        pairedData = zip(countyDict[key],value)
        countyDict[key] = [a+b for a,b in pairedData]

for key,val in iter(countyDict.items()):
    means = [round(x/val[p],3) for x in val]
    string = key
    for mean in means:
        string+=','+str(mean)
    print(string)
sys.exit()
    
    
