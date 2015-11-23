import numpy as np
import os
import collections

#path = '/Users/keganrabil/Desktop/PBDA/week 11/Data/'
path = '/Users/keganrabil/Desktop/PBDA/Data/'

def getColumns(data):
    try:
        u = [int(data[2]),int(data[3])]
    except IndexError:
        u = [int(data[2])]
    return u

codeBook = {}
with open(path + 'codeBook.txt','rU') as f:
    for line in f:
        data = line.replace('\n','').replace(' ','').split(',')
        key = data[0]
        variableDict = codeBook.get(key)
        if variableDict is None:
            year = int(data[1])
            u = getColumns(data)
            variableDict = {year:u}
        else:
            variableDict[int(data[1])] = getColumns(data)
        # WHAT THE ACTUAL FUCK IS VALUE?!?!?
        # codeBook[key] = value
        codeBook[key] = variableDict


stateCodes = {}
with open(path + 'statecounty.csv','rU') as f:
    print(f.readline())
    for string in f:
        data = string.split(',')
        stateCodes[int(data[1])] = data[0]
print(stateCodes)

dataTuple = collections.namedtuple('dataTuple','year stateName weight diabetes')

def mapper(file,dataDict,counter,year):
    startWt = int(codeBook['Weight'][year][0])-1
    endWt = int(codeBook['Weight'][year][1])
    print(startWt,endWt)
    columnDiabetes = codeBook['Diabetes'][year][0]-1
    with open(file,'rU') as f:
        for string in f:
            stateCode = int(string[:2])
            #print('stateCode',stateCode)
            try:
                stateName = stateCodes[stateCode]
                weight = float(string[startWt:endWt])
                diabetesString = string[columnDiabetes]
                boolean = diabetesString in set(['1','3','4','7'])
                if boolean:
                    diabetes = int(diabetesString == '1')
                    dataDict[counter] = dataTuple(year,stateCode,weight,diabetes)
                    counter += 1
            except KeyError:
                pass
    return dataDict, counter

counter = 0
dataDict = {}
for filename in os.listdir(path):
    try:
        year = 2000 + int(filename[6:8])
        file = path + filename
        print(file)
        dataDict,counter = mapper(file, dataDict, counter, year)
    except ValueError:
        pass
print(len(dataDict))

stateDataDict = {}
for k,v in iter(dataDict.items()):
    stateKey = (v.stateName,v.year)
    value = stateDataDict.get(stateKey)
    if value is None:
        totalWeight = v.weight
        totalPrevWeighted = v.weight * v.diabetes
    else:
        prevalence, totalWeight = value
        totalWeight += v.weight 
        totalPrevWeighted += v.weight * v.diabetes
    stateDataDict[stateKey] = [totalPrevWeighted, totalWeight]
print(len(stateDataDict))

for k,v in iter(stateDataDict.items()):
    #print(v[0],v[1])
    #print("Weighted Mean:",k,100 * v[0]/v[1])
    stateDataDict[k] = 100 * v[0]/v[1]

statePrevalenceDict = dict.fromkeys(stateCodes)
for stateKey in stateDataDict:
    prevalence = stateDataDict[stateKey]
    stateCode, year = stateKey
    data = statePrevalenceDict.get(stateCode)
    if data is None:
        statePrevalenceDict[stateCode] = [(year,prevalence)]
    else:
        data.append((year,prevalence))
        statePrevalenceDict[stateCode] = data


R_sq_ad_list = []
with open(path + 'plottingData.csv','w') as f:
    for k,data in iter(statePrevalenceDict.items()):
        X = np.array([[1,year-2007] for year,_ in data])
        Y = np.array([[prevalence] for _,prevalence in data])
        b = np.linalg.solve(X.T.dot(X),X.T.dot(Y))
        ##### R^2 adjusted calculations
        y = np.mean(Y)
        y_dot = np.dot(Y.T,Y)[0][0]
        n = float(len(Y))
        s2 = (y_dot - (n * (y **2)))/(n-1.)
        l = np.dot(Y.T,np.dot(X,b))[0][0]
        sig2 = (y_dot - l)/(n-2.)
        R2 = (s2-sig2)/s2
        R_sq_ad_list.append([stateCodes[k],R2])
        print(stateCodes[k],R2)
        string = str(stateCodes[k]) + ',' + str(b[0][0]) + ',' + str(b[1][0]) + '\n'
        f.write(string)
f.close()

# Write R2 values for homework 8 #4
with open(path+'rSquared.csv','w') as f:
    f.write("State,R2\n")
    for l in R_sq_ad_list:
            f.write(str(l[0])+","+str(l[1])+"\n")
f.close()
