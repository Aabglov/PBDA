import sys
import os
import numpy
import operator
import pickle
import urllib.request
import zipfile


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
####
 
it_path = 'itcont.txt'





def checkFiles():
    try:
        f = open(it_path,'r')
        f.close()
    except:
        print('{c} not found, downloading local version...'.format(c=it_path))
        download()


def download():
    try:
        path = 'indiv14.zip'
        with zipfile.ZipFile(path) as zf:
            zf.extractall()
    except:        
        url = 'ftp://ftp.fec.gov/FEC/2014/indiv14.zip'
        path = 'indiv14.zip'
        extract = path
        urllib.request.urlretrieve(url,path)
        with zipfile.ZipFile(path) as zf:
            zf.extractall()



if __name__ == '__main__':
    
    checkFiles()

    
    try:
        D = load('D.pckl')
        print('local copy of D found, using that...')
    except:
        D = {}
        n = 0
        with open(it_path) as f:
            for string in f:
                data = string.split("|")
                name = data[7]
                cont = data[14]
                if name in D:
                    D[data[7]] += int(data[14])
                else:
                    D[data[7]] = int(data[14])
                n+=1
                if not n % 5000:
                    print(n)
        print('Saving data....')
        save(D,'data.pckl')


    sorted_sums = sorted(D.items(),key=operator.itemgetter(1))
    for s in sorted_sums:
        if s[1] >= 10000:
            print(s)
