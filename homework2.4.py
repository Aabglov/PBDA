import sys
import os
import numpy
import pickle
import operator
import urllib.request
import zipfile

# ALL FILES IN THE SAME DIRECTORY AS SCRIPT
cm_path = 'cm.txt'
oth_path = 'itoth.txt'

cm_name = 'cm_oth_dict_hm.pckl'
oth_name = 'oth_dict_hm.pckl'


    
# GLOBALS
comm_dict = {}
oth_dict = {}


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
        f = open(cm_path,'rb')
        f.close()
    except:
        print('{c} not found, downloading local version...'.format(c=cm_path))
        download('cm')

    try:
        f = open(oth_path,'rb')
        f.close()
    except:
        print('{o} not found, downloading local version...'.format(o=oth_path))
        download('oth')
        

def findPAC(name,oth_dict):
    for k in oth_dict.keys():
        if name in k.lower():
            print(k,len(oth_dict[k]))

def download(dict_id):
    
    if dict_id == 'cm':
        url = 'ftp://ftp.fec.gov/FEC/2014/cm14.zip'
        path = 'cm.zip'
        extract = cm_path
        
    elif dict_id == 'oth':
        url = 'ftp://ftp.fec.gov/FEC/2014/oth14.zip'
        path = 'oth.zip'
        extract = oth_path
        
        
    urllib.request.urlretrieve(url,path)
    with zipfile.ZipFile(path) as zf:
        zf.extractall()


#####################################################
def createDict(filename,key_ind,val_ind):
    D = {}
    with open(filename) as f:
        for string in f:
            data = string.split("|")
            key = data[key_ind]
            value = data[val_ind]
            D[key] = value
    return D


def createOthDict(filename):
    oth_dict = {}
    with open(filename) as f:
        for string in f:
            data = string.split("|")
            try:    
                comm = comm_dict[data[0]]
            except:
                comm = 'NA'
            cont = data[7]
            amount = float(data[14])
            if cont not in oth_dict:
                oth_dict[cont] = {comm:amount}
            else:
                if comm not in oth_dict[cont]:
                    oth_dict[cont][comm] = amount
                else:
                    oth_dict[cont][comm] += amount
    return oth_dict


def getTopTen(pac,oth_dict):
    d = oth_dict[pac]
    return dict(sorted(d.items(),key=operator.itemgetter(1),reverse=True)[:10])
        

def getDict(filename,dict_id):
    try:
        print('attempting to load {d} dictionary'.format(d=dict_id))
        var = load(filename)
        print('load successful')
    except:
        print('\nload failed,')
        if dict_id == 'oth':
            print('creating oth_dict ....')
            var = createOthDict(oth_path)
        elif dict_id == 'cm':
            print('creating commDict ....')
            var = createDict(cm_path,0,1)
        save(var,filename)
        print('saved {d} dictionary'.format(d=dict_id))
    return var


##########################################


if __name__ == '__main__':
    DEBUG = True
    
    checkFiles()

    comm_dict = getDict(cm_name,'cm')
    oth_dict = getDict(oth_name,'oth')

    # SANITY CHECKING -- ENSURE GLOBALS ASSIGNED CORRECTLY
    if DEBUG:
        print('Size of commDict:',len(comm_dict.keys()))
        print('Size of othDict:',len(oth_dict.keys()))

    if DEBUG:
        findPAC('koch',oth_dict)
    pac = 'KOCH INDUSTRIES INC POLITICAL ACTION COMMITTEE (KOCHPAC)'
    print('Top donations made by {p}'.format(p=pac))
    pac_cont = getTopTen(pac,oth_dict)
    for k,v in pac_cont.items():
        print('{k}: ${v}'.format(k=k,v=v))
    
