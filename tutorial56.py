import sys
import os
import numpy as np
import pickle
import operator
from itertools import islice
import urllib
import zipfile


# GLOBALS
power_path = 'household_power_consumption.txt'

# PICKLE WRAPPERS
def save(var,name):
    f = open(name,'wb')
    pickle.dump(var,f)
    f.close()
    
def load(name):
    f = open(name,'rb')
    var = pickle.load(f)
    f.close()
    return var


def checkFiles():
    try:
        f = open(power_path,'rb')
        f.close()
    except:
        print('{c} not found, downloading local version...'.format(c=power_path))
        download('pow')




def download(dict_id):
    path = 'power.zip'
    try:
        print('extracting {p} ......'.format(p=path))
        with zipfile.ZipFile(path) as zf:
            zf.extractall()
    except:
        if dict_id == 'pow':
            url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip'
            extract = power_path
            
        urllib.urlretrieve(url,path)
        print('extracting {p} ......'.format(p=path))
        with zipfile.ZipFile(path) as zf:
            zf.extractall()


#####################################################
# pass file path and size of blocks
def powerData(filename,n,q=4,debug=False):
    try:
        return load('A.pckl')
    except:
        print("A.pckl not found, calculating.....")
        A = np.matrix(np.zeros((q,q)))
        w = np.ones((q,1))
        with open(filename) as f:
            block = list(islice(f,n))
            if not block:
                #break
                pass
            else:
                total = len(block)
                count = 0
                for l in block:
                    count += 1
                    data = l.split(';')
                    try:
                        # Get data values from block
                        w[1] = float(data[6])
                        w[2] = float(data[7])
                        w[3] = float(data[8])
                        A += w*w.T
                    except ValueError as v:
                        #if debug:
                        #    print("computePowerData:: non-fatal error :: {v}".format(v=v))
                        pass
                    if not count%100000 and debug:
                        print('{c} of {l} processed'.format(c=count,l=total))
        save(A,'A.pckl')
    return A

def calcValues(A,q=4):
    n = A[0,0]
    mean = np.asmatrix(A[1:q,0]/n)
    M = A[1:q,1:q]
    S = (M/n) - (mean * mean.T)
    s = np.sqrt(np.diag(S))
    D = np.diag(1./s)
    R = D * S * D 
    return n,mean,M,S,D,R

##########################################


        

if __name__ == '__main__':
    DEBUG = True
    
    checkFiles()
    q = 4
    num = 2049280
    
    A = powerData(power_path,num,q,DEBUG)
    n,mean,M,S,D,R  = calcValues(A,q)
    if DEBUG:
        print('n: ',n)
        print('\nmean:')
        print(mean)
        print('\nM:')
        print(M)
        print('\nS:')
        print(S)
        print('\nD:')
        print(D)
        print('\n')
    print("R: ")
    print(R)
    
