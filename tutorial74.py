import numpy as np


# Create paperDict
path = 'owners.txt'
paperDict = {}
with open(path, "rU") as f:
    for string in f:
        string = string.replace('\n',' ')
        #print(string)
        lst = string.split(",")
        paperDict[int(lst[0])] = lst[1]
print(paperDict)


sentenceDict = {}
nSentences = 0
sentence = ''
path = "1404-8.txt"
with open(path,"rU") as f:
    for string in f:
        string = string.replace("\n"," ")
        for char in string:
            if char == '.':
                sentenceDict[nSentences] = sentence
                sentence = ''
                nSentences += 1
            else:
                if char not in ',?!/;:-"()':
                    sentence += char

            
# OH MY GOD DON'T PRINT THE ENTIRE DICTIONARY -- IT WILL CRASH YOUR PYTHON INSTANCE
print(list(sentenceDict.values())[0])

paperCount = 0
FedPaperDict = {}
paper = []
save = False
for index in sentenceDict:
    if 'PUBLIUS' in sentenceDict[index]:
        FedPaperDict[(paperCount,author)] = paper
        paper = []
        save = False
    if 'To the People of the State of New York' in sentenceDict[index]:
        paperCount += 1
        author = paperDict[paperCount]
        print(sentenceDict[index])
        save = True
    if save is True:
        paper.extend([sentenceDict[index]])

# Sanity checking
for k,v in iter(FedPaperDict.items()):
    print(k,len(v))

# Create Stop Word List (set)
path = "stop.txt"
stopWordList = []
with open(path,"rU") as f:
    for word in f:
        stopWordList.append(word.strip("\n"))
stopWordSet = stopWordList
print(stopWordList)

# Create wordDict
wordDict = dict.fromkeys(FedPaperDict.keys())
for pair in FedPaperDict:
    paper = FedPaperDict[pair]
    countDict = {}
    for sentence in paper:
        words = sentence.split(" ")
        for word in words:
            lowerWord = word.lower()
            if lowerWord not in stopWordSet:
                value = countDict.get(lowerWord)
                if value is None:
                    countDict[lowerWord] = 1
                else:
                    countDict[lowerWord] += 1
    wordDict[pair] = countDict
    print("WordDict:",pair,len(wordDict[pair]))
        
# Disputed and Joints
disputed = []
joint = []
for pair in FedPaperDict:
    if pair[0] in [49,50,51,52,53,54,55,56,57,58,62,63]:
        disputed.append(pair)
    elif pair[0] in [19,20,18]:
        joint.append(pair)
print(disputed)
print(joint)
merge = disputed #+ joint
skip = [x[0] for x in merge]
print(skip)

# Used Words Dict
usedWordsDict = {}
for pair in wordDict:
    if pair[0] not in skip:
        D = wordDict[pair]
        author = pair[1]
        for word in D.keys():
            value = usedWordsDict.get(word)
            if value is None:
                value = [author]
            else:
                if author not in value:
                    value.append(pair[1])
            usedWordsDict[word] = value
print(len(usedWordsDict))

# create test word list
testWords = []
for key,val in iter(usedWordsDict.items()):
    if 'HAMILTON ' in val and 'JAY ' in val and 'MADISON ' in val and 'H and M ' in val:
        testWords.append(key)
print(len(testWords))

# Remove non-test words from wordDict
for pair in wordDict:
    if pair[0] not in skip:
        D = wordDict[pair]
        newDict = {}
        for word in D:
            if word in testWords:
                newDict[word] = D[word]
        wordDict[pair] = newDict

nR = 0.
authors = ['HAMILTON ', 'JAY ', 'MADISON ', 'H and M ']
nGroups = len(authors)
logPriors = dict.fromkeys(authors,0)
freqDistnDict = dict.fromkeys(authors)
for pair in wordDict:
    if pair[0] not in skip:
        author = pair[1]
        D = wordDict[pair]
        distn = freqDistnDict.get(author)
        if distn is None:
            distn = D
        else:
            for word in D:
                if word in distn.keys():
                    distn[word] += D[word]
                else:
                    distn[word] = D[word]
        freqDistnDict[author] = distn
        logPriors[author] += 1.
        nR += 1.
        
logProbDict = dict.fromkeys(authors,{})
distnDict = dict.fromkeys(authors)
for author in authors:
    authorDict = {}
    nWords= 0.
    for word in testWords:
        nWords += freqDistnDict[author][word]
    for word in testWords:
        relFreq = freqDistnDict[author][word]/nWords
        authorDict[word] = np.log(relFreq)
    logProbDict[author] = authorDict
    logPriors[author] = np.log(logPriors[author]/nR)
    distnDict[author] = [logPriors[author], logProbDict[author]]

confusionMatrix = np.zeros(shape=(nGroups,nGroups))
for pair in wordDict:
    testAuthor = pair[1]
    if pair[0] not in skip:
        xj = wordDict[pair]
        postProb = dict.fromkeys(authors,0)
        for author in list(authors):
            distn = distnDict[author]
            postProb[author] = distn[0]
            for word in xj:
                logProb = distn[1][word]
                postProb[author] += xj[word]*logProb
        postProbAuthors = list(postProb.keys())
        postProbList = list(postProb.values())
        maxIndex = np.argmax(postProbList)
        prediction = postProbAuthors[maxIndex]
        i = list(authors).index(testAuthor)
        j = list(authors).index(prediction)
        confusionMatrix[i,j] += 1

print('acc =',sum(np.diag(confusionMatrix))/sum(sum(confusionMatrix)))

###################### HOMEWORK 7.6 # 1 #################################


# Remove non-test words from wordDict
for pair in wordDict:
    if pair[0] in skip:
        D = wordDict[pair]
        newDict = {}
        for word in D:
            if word in testWords:
                newDict[word] = D[word]
        wordDict[pair] = newDict

nR = 0.
authors = ['HAMILTON ', 'JAY ', 'MADISON ', 'H and M ']
nGroups = len(authors)
logPriors = dict.fromkeys(authors,0)
freqDistnDict = dict.fromkeys(authors)
for pair in wordDict:
    author = pair[1]
    D = wordDict[pair]
    distn = freqDistnDict.get(author)
    if distn is None:
        distn = D
    else:
        for word in D:
            if word in distn.keys():
                distn[word] += D[word]
            else:
                distn[word] = D[word]
    freqDistnDict[author] = distn
    logPriors[author] += 1.
    nR += 1.
        
logProbDict = dict.fromkeys(authors,{})
distnDict = dict.fromkeys(authors)
for author in authors:
    authorDict = {}
    nWords= 0.
    for word in testWords:
        nWords += freqDistnDict[author][word]
    for word in testWords:
        relFreq = freqDistnDict[author][word]/nWords
        authorDict[word] = np.log(relFreq)
    logProbDict[author] = authorDict
    logPriors[author] = np.log(logPriors[author]/nR)
    distnDict[author] = [logPriors[author], logProbDict[author]]

for pair in wordDict:
    testAuthor = pair[1]
    if pair[0] in skip:
        xj = wordDict[pair]
        postProb = dict.fromkeys(authors,0)
        for author in list(authors):
            distn = distnDict[author]
            postProb[author] = distn[0]
            for word in xj:
                logProb = distn[1][word]
                postProb[author] += xj[word]*logProb
        postProbAuthors = list(postProb.keys())
        postProbList = list(postProb.values())
        maxIndex = np.argmax(postProbList)
        prediction = postProbAuthors[maxIndex]
        i = list(authors).index(testAuthor)
        j = list(authors).index(prediction)
        print("Prediction:",pair[0],authors[j],"Accepted:",paperDict[pair[0]])

