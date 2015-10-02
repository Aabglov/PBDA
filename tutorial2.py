import sys
import os
import numpy
import pickle
import operator
import urllib
import zipfile
import copy

# ALL FILES IN THE SAME DIRECTORY AS SCRIPT
cm_path = 'cm.txt'
oth_path = 'itoth.txt'

cm_name = 'cm_oth_dict.pckl'
oth_name = 'oth_dict.pckl'


    
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
        



def download(dict_id):
    
    if dict_id == 'cm':
        url = 'ftp://ftp.fec.gov/FEC/2014/cm14.zip'
        path = 'cm.zip'
        extract = cm_path
        
    elif dict_id == 'oth':
        url = 'ftp://ftp.fec.gov/FEC/2014/oth14.zip'
        path = 'oth.zip'
        extract = oth_path
        
        
    urllib.urlretrieve(url,path)
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

def createCommSet(comm_dict):
    return set(comm_dict.keys())


def createOthDict(filename):
    oth_dict = {}
    with open(filename) as f:
        for string in f:
            data = string.split("|")
            cont = data[0]
            comm = data[7]
            if oth_dict.get(cont) is None:
                oth_dict[cont] = {comm}
            else:
                oth_dict[cont] = oth_dict[cont].union({comm})
    return oth_dict


def reduceOthDict(oth_dict):
    red_dict = copy.copy(oth_dict)
    oth_keys = oth_dict.keys()
    for k in oth_keys:
        if len(oth_dict[k]) < 601:
            red_dict.pop(k,None)
    return red_dict


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


def computeJaccardP(oth_dict,comm_dict,pairs):
    J = {}
    pAB = {}
    pBA = {}
    for i in range(len(pairs)):
        idA = pairs[i][0]
        nameA = comm_dict[idA]
        A = oth_dict[idA]

        idB = pairs[i][1]
        nameB = comm_dict[idB]
        B = oth_dict[idB]

        intersect = float(len(A.intersection(B)))
        J[(nameA,nameB)] = intersect/len(A.union(B))
        pAB[(nameA,nameB)] = intersect/len(B)
        pBA[(nameB,nameA)] = intersect/len(A)
    return J,pAB,pBA
        

if __name__ == '__main__':
    DEBUG = True
    
    checkFiles()

    comm_dict = getDict(cm_name,'cm')
    oth_dict = getDict(oth_name,'oth')

    # SANITY CHECKING -- ENSURE GLOBALS ASSIGNED CORRECTLY
    print('Size of commDict:',len(comm_dict.keys()))
    print('Size of othDict:',len(oth_dict.keys()))

    if DEBUG:
        n = len(oth_dict)
        print('N pairs = ',n*(n-1)/2)

    oth_dict = reduceOthDict(oth_dict)

    if DEBUG:
        n = len(oth_dict)
        print('N pairs AFTER reduction = ',n*(n-1)/2)

    cont_list = list(oth_dict.keys())

    if DEBUG:
        for c in cont_list:
            print(len(oth_dict[c]))

    n = len(oth_dict)
    pairs = [(cont_list[i],cont_list[j]) for i in range(n-1) for j in range(i+1,n,1)]
    if DEBUG:
        print('Length of pairs: {l}'.format(l=len(pairs)))


    J,pAB,pBA = computeJaccardP(oth_dict,comm_dict,pairs)

    sortedJ = sorted(J.items(), key=operator.itemgetter(1))

    for i in range(len(sortedJ)):
        nameA = sortedJ[i][0][0]
        nameB = sortedJ[i][0][1]
        print(nameA,'|',nameB,round(sortedJ[i][1],3),round(pAB[(nameA,nameB)],3),round(pBA[(nameB,nameA)],3))

