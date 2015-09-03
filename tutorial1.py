import sys
import os
import numpy
import pickle
import operator
import urllib
import zipfile

# ALL FILES IN THE SAME DIRECTORY AS SCRIPT
ind_path = 'itcont.txt'
cm_path = 'cm.txt'
cn_path = 'cn.txt'

cm_name = 'cm_dict.pckl'
cn_name = 'cn_dict.pckl'
ind_name = 'ind_dict.pckl'
employ_name = 'employ_dict.pckl'
reduced_name = 'reduced_dict.pckl'
summ_name = 'summ_dict.pckl'

    
# GLOBALS
comm_dict = {}
cand_dict = {}
employ_dict = {}
reduced_dict = {}



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
        f = open(cn_path,'rb')
        f.close()
    except:
        print('{c} not found, downloading local version...'.format(c=cn_path))
        download('cn')
        
    try:
        f = open(ind_path,'rb')
        f.close()
    except:
        print('{i} not found, downloading local version...'.format(i=ind_path))
        download('ind')



def download(dict_id):
    
    if dict_id == 'cm':
        url = 'ftp://ftp.fec.gov/FEC/2014/cm14.zip'
        path = 'cm.zip'
        extract = cm_path
        
    elif dict_id == 'cn':
        url = 'ftp://ftp.fec.gov/FEC/2014/cn14.zip'
        path = 'cn.zip'
        extract = cn_path
        
    elif dict_id == 'ind':
        url = 'ftp://ftp.fec.gov/FEC/2014/indiv14.zip'
        path = 'ind.zip'
        extract = ind_path
        
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

##def createContribDict(filename,key_ind,val_ind):
##    D = {}
##    n = 0
##    with open(filename) as f:
##        for string in f:
##            data = string.split("|")
##            key = data[key_ind]
##            value = data[val_ind]
##            if key in D:
##                D[key] += int(value)
##            else:
##                D[key] = int(value)
##            if not n%5000:
##                print n
##            n += 1
##    return D

def createEmployDict(filename):
    # explicit globals
    global cand_dict
    global comm_dict
    D = {}
    with open(filename) as f:
        for string in f:
            data = string.split("|")
            employ = data[11]
            # this could be more efficient using globals
            party = getParty(data[0])
            contrib = int(data[14])
            if employ in D:
                D[employ] += [[party,contrib]]
            else:
                D[employ] = [[party,contrib]]
    return D


def createReducedDict():
    global employ_dict
    reduced_dict = {}
    for employ in employ_dict:
        totals = {'REP':0,'DEM':0,'Other':0}
        for val in employ_dict[employ]:
            try:
                totals[val[0]] += val[1]
            except:
                totals['Other'] += val[1]
        reduced_dict[employ] = totals
    return reduced_dict


def createSummDict():
    global reduced_dict
    summ_dict = {}
    for employ in reduced_dict:
        totals = reduced_dict[employ]
        summ_dict[employ] = sum(totals.values())
        if summ_dict[employ] > 100000:
            print('{k}: {c}'.format(k=employ,c=summ_dict[employ]))
    return summ_dict



def getDict(filename,dict_id):
    try:
        print('attempting to load {d} dictionary'.format(d=dict_id))
        var = load(filename)
        print('load successful')
    except:
        print('\nload failed,')
        if dict_id == 'employ':
            print('creating employ_dict ....')
            var = createEmployDict(ind_path)
        elif dict_id == 'reduced':
            print('creating reduced_dict ....')
            var = createReducedDict()
        elif dict_id == 'summ':
            print('creating summ_dict ....')
            var = createSummDict()
        elif dict_id == 'cm':
            print('creating commDict ....')
            var = createDict(cm_path,0,10)
        elif dict_id == 'cn':
            print('creating candDict ....')
            var = createDict(cn_path,9,2)
        save(var,filename)
        print('saved {d} dictionary'.format(d=dict_id))
    return var

def getParty(key):
    
    global comm_dict
    global cand_dict
    
    if key in comm_dict:
        return comm_dict[key]
    elif key in cand_dict:
        return cand_dict[key]
    else:
        return None

##########################################


if __name__ == '__main__':
    checkFiles()

    comm_dict = getDict(cm_name,'cm')
    cand_dict = getDict(cn_name,'cn')
    employ_dict = getDict(employ_name,'employ')
    reduced_dict = getDict(reduced_name,'reduced')

    # SANITY CHECKING -- ENSURE GLOBALS ASSIGNED CORRECTLY
    print('Size of commDict:',len(comm_dict.keys()))
    print('Size of candDict:',len(cand_dict.keys()))
    print('Size of employDict:',len(employ_dict.keys()))
    print('Size of reducedDict:',len(reduced_dict.keys()))
          
    summ_dict = getDict(summ_name,'summ')


    # Not sure why we're seeing negative entries, but this is definitely an issue
    # with the data, not the processing
    sorted_summ = sorted(summ_dict.items(),key=operator.itemgetter(1))
    n = len(sorted_summ)
    for e in sorted_summ[n-100:]:
        print('{k}: ${c}.00'.format(k=e[0],c=e[1]))

    print('Saving to file....')
    f = open('employerMoney.txt','wb')
    for i in range(n-200,n):
        key = sorted_summ[i][0].replace("'","")
        totals = reduced_dict[key]
        rep = str(totals['REP'])
        dem = str(totals['DEM'])
        oth = str(totals['Other'])
        tot = str(sorted_summ[i][1])
        f.write("'{k}',{r},{d},{o},{t}\n".format(k=key,r=rep,d=dem,o=oth,t=tot))
    f.close()
    print('....complete')
