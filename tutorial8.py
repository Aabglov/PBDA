import numpy as np
import os
import collections

path = '/Users/keganrabil/Desktop/PBDA/week 11/Data/'

def getColumns(data):
    try:
        u = [int(data[2]),int(data[3])]
    except IndexError:
        u = [int(data[2])]
    return u

codeBook = {}
with open(path + 'codeBook.txt',encoding='utf-8') as f:
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
with open(path + 'statecounty.csv',encoding='utf-8') as f:
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
    with open(file, encoding="utf-8",errors='ignore') as f:
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
    print(v[0],v[1])
    print("Weighted Mean:",k,100 * v[0]/v[1])
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

with open(path + 'plottingData.csv','w') as f:
    for k,data in iter(statePrevalenceDict.items()):
        X = np.array([[1,year-2007] for year,_ in data])
        Y = np.array([[prevalence] for _,prevalence in data])
        b = np.linalg.solve(X.T.dot(X),X.T.dot(Y))
        print(stateCodes[k],b[0],b[1])
        string = str(stateCodes[k]) + ',' + str(b[0][0]) + ',' + str(b[1][0]) + '\n'
        f.write(string)
f.close()
