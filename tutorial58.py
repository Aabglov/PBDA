import sys
import os
import numpy as np
import pickle
import operator
from itertools import islice
import urllib
import zipfile


# GLOBALS
nasdaq_path = 'NASDAQ.csv'

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
        f = open(nasdaq_path,'rb')
        f.close()
    except:
        print('{n} not found, check the path and try again'.format(n=nasdaq_path)) #downloading local version...'.format(c=power_path))
        sys.exit()
        #download('pow')




def download(dict_id):
    path = 'nasdaq.zip'
    try:
        print('extracting {p} ......'.format(p=path))
        with zipfile.ZipFile(path) as zf:
            zf.extractall()
    except:
        if dict_id == 'pow':
            url = '????????????????'
            extract = nasdaq_path
            
        urllib.urlretrieve(url,path)
        print('extracting {p} ......'.format(p=path))
        with zipfile.ZipFile(path) as zf:
            zf.extractall()


#####################################################
def nasdaqData(filename,save_beta,save_err,p,debug=False):
    q = p+1
    pred = range(1,q)
    size = 1000
    empty = np.matrix(np.zeros((size,1)))
    A = np.matrix(np.zeros((q,q)))
    x = np.matrix(np.ones((q,1)))
    z = np.matrix(np.zeros((q,1)))
    s = 0
    n = 0
    try:
        return load(save_beta), load(save_err)
    except:
        print("{s} not found, calculating.....".format(s=save_beta))
        with open(filename) as f:
            names = f.readline().split(',')
            while True:
                block = list(islice(f,size))
                if not block:
                    break
                # WAY faster to do matrix multiplication on batches than to calculate
                # line by line
                data = np.matrix([[float(v) for v in b.split(',')] for b in block])
                y = data[:,0]
                d = data.shape[0]
                x = np.concatenate((np.ones((d,1)),data[:,pred]),axis=1).T
                A += x*x.T
                z += x*y
                s += np.sum(np.square(y))
                n += data.shape[0]
        beta = np.linalg.solve(A,z)
        avg_y = z[0]/n
        sigma = (s/n) - (avg_y**2)
        sigma_reg = (s - (z.T * beta))/(n-q)
        R = (sigma-sigma_reg)/sigma
        #print(R)
        f.close()
        save(beta,save_beta)
        save(R,save_err)
        #print('Beta for p={p}: {b}'.format(p=p,b=beta))
        return beta,R

##def calcErr(filename,beta,p,debug=False):
##    q = p+1
##    pred = range(1,q)
##    A = np.matrix(np.zeros((q,q)))
##    x = np.matrix(np.ones((q,1)))
##    z = np.matrix(np.zeros((q,1)))
##    err = 0
##    print("calculating error for P={p}....".format(p=p))
##    with open(filename) as f:
##        names = f.readline().split(',')
##        while True:
##            block = list(islice(f,1000))
##            if not block:
##                break
##            # WAY faster to do matrix multiplication on batches than to calculate
##            # line by line
##            data = np.matrix([[float(v) for v in b.split(',')] for b in block])
##            y = data[:,0]
##            d = data.shape[0]
##            x = np.concatenate((np.ones((d,1)),data[:,pred]),axis=1)
##            # Need to add the sum since this difference is now a vector.
##            # Also, using np.square for element-wise squaring of vector.
##            err += float(sum(np.square(y - x.dot(beta))))
##    return err

                    

##########################################


        

if __name__ == '__main__':
    DEBUG = True
    
    checkFiles()
    beta_1,err_1 = nasdaqData(nasdaq_path,'beta_1.pckl','err_1.pckl',1,DEBUG)
    beta_27,err_27 = nasdaqData(nasdaq_path,'beta_27.pckl','err_27.pckl',27,DEBUG)
    print(err_1)
    print(err_27)
    #print(calcErr(nasdaq_path,beta_1,1,DEBUG))
