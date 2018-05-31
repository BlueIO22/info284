
from glob import glob
from collections import Counter
import re
import os
import time
from itertools import dropwhile
import random

globalNrCorrects = 0
globalNrFiles = 0
globalLearningReal = bool()
globalLearningGuess = bool()
globLearningPos = Counter()
globLearningNeg = Counter()

def LearningStateReal(poNe):
    global globalLearningReal
    globalLearningReal = poNe
    return globalLearningReal

def LearningStateGuess(poNe):
    global globalLearningGuess
    globalLearningGuess = poNe
    return globalLearningGuess

def nrCorrect(newCorrect):
    global globalNrCorrects
    globalNrCorrects += newCorrect
    return globalNrCorrects

def nrFiles(newFiles):
    global globalNrFiles 
    globalNrFiles = globalNrFiles + newFiles
    return globalNrFiles

def globalMemoryPos(lc):
    global globLearningPos
    globLearning = lc
    return globLearningPos

def globalMemoryNeg(lc):
    global globLearningNeg
    globLearning = lc
    return globLearningNeg

def commonWordRemover(c):
    
    for key in c.keys():
        if c[key] >= len(c) * 0.05:
            c[key] = 0
    return c

def rareWordFinder(c):
        
    rareWords = Counter()
    rareWords = c
        
    for key, count in dropwhile(lambda key_count: key_count[1] <= 300, c.most_common()): del c[key]
        
    rareWords = rareWords - c
        
    return rareWords

def singleFileWordCounter(Path):
    counter = Counter()
    file = open(random.choice(Path))
    for x in range (0,1):
        for word in file.read().lower().split():
            counter[word] = 1
    file.close()
    counter = commonWordRemover(counter)
    return counter

def test(posTest, negTest):
    
    r = random.randint(1, 2)
    if r == 2:
        file = posTest
        print('Filen er positiv')
        LearningStateReal(True)
        
    else:
        file = negTest               
        print('Filen er negativ')
        LearningStateReal(False)
    print(file)
    return file

def wordCounterTrain(filePath):

    counter = Counter()
    f = open(filePath)
    c = 0
    for word in f.read().lower().split():
        counter[word] = 1
    f.close()

    return(counter)

def wordCounterTest(filePath):
    counter = Counter()
    f = open(filePath)
    c = 0
    for word in f.read().lower().split():
        counter[word] += 1
    f.close()

    return (counter)

def fileFinder(dirPath):
    i = 0
    files = []
    filepaths = os.listdir(dirPath)
    for file in filepaths:
        if file.endswith(".txt"):
            files.append(os.path.join(dirPath + '/' + file))

    return files

def interpetFileCopy(nrFiles, posFiles, negFiles, trainingPos, trainingNeg, testing, trainingFull, posFileCount, negFileCount):
    pos = 1.0
    neg = 1.0
    c = 1.0

    nrFiles = float(nrFiles)
    negFiles = float(negFiles)
    posFiles = float(posFiles)

    for key in testing.keys():
        wordProbPos = ((trainingPos[key] + 1) / posFileCount) / 1000
        pos = pos * wordProbPos
        wordProbNeg = ((trainingNeg[key] + 1) / negFileCount) / 1000
        neg = neg * wordProbNeg
        c = ((trainingFull[key] + 1) / nrFiles)

    pos = (pos * posFileCount) / c
    neg = (neg * negFileCount) / c

    if (pos - neg) > 0.5 :
        LearningStateGuess(True)

    elif (pos - neg) < 0.5:
        LearningStateGuess(False)

def interpetFile(nrFiles, trainingPos, trainingNeg, testing):
    pos = 1
    neg = 1
    for key in testing.keys():
        wordProbPos = float(trainingPos[key] + 1) / len(trainingPos.values())
        pos = pos * wordProbPos
        wordProbNeg = float(trainingNeg[key] + 1) / len(trainingNeg.values())
        neg = pos * wordProbNeg

    file = (nrFiles / 2) / nrFiles

    pos = (pos * file) / (pos / nrFiles)

    neg = (neg * file) / (neg / nrFiles)


    if pos >= neg:
        LearningStateGuess(True)
            
    elif pos < neg:
        LearningStateGuess(False)


def train(train_counter, directory):
    for file in directory:
        train_counter = interpetFileCopy(train_counter, wordCounterTrain(file))
        directory.remove(file)
    return train_counter

def learn(learningPos, learningNeg):
    li = float()
    trainFiles = []
    testFiles = []
    nrCorrect(-globalNrCorrects)
    nrFiles(-globalNrFiles)
    nrPos = 1
    nrNeg = 1
    nrTotal = 2
    posFiles = fileFinder("/Users/mariussorenes/PycharmProjects/train/pos")
    negFiles = fileFinder("/Users/mariussorenes/PycharmProjects/train/neg")
    negTestFiles = fileFinder('/Users/mariussorenes/PycharmProjects/test/neg')  # fileFinder(str(input('Please write the path of the directory for negative test files: ')), li)
    posTestFiles = fileFinder('/Users/mariussorenes/PycharmProjects/test/pos')  # fileFinder(str(input('Please write the path of the directory for positive test files: ')), li)
    allTrainingFiles = list(set().union(posFiles, negFiles))
    allTestFiles = list(set().union(posTestFiles, negTestFiles))

    trainingFull = Counter()


    i = 0

    while i < len(allTrainingFiles):

        if i < len(posFiles):
            learningPos.update(wordCounterTest(posFiles[i]))

        if i < len(negFiles):
            learningNeg.update(wordCounterTest(negFiles[i]))

        i = i + 1


    i = 0
    trainingFull.update(learningNeg)
    trainingFull.update(learningPos)

    pos_ct = float(len(posFiles)) / len(allTrainingFiles)
    neg_ct = float(len(negFiles)) / len(allTrainingFiles)

    for file in allTestFiles:
        testFile = file

        nrFiles(1)

        interpetFileCopy(len(allTrainingFiles), len(posFiles), len(negFiles), learningPos, learningNeg, wordCounterTest(testFile), trainingFull, pos_ct, neg_ct)

        if globalLearningReal == globalLearningGuess:
            nrCorrect(1)

        print(str(nrCorrect(0)) + ' of ' + str(nrFiles(0)) + ' is correct')

def textEvaluater(text):
    words = Counter(text.lower().split())
    return words

learn(Counter(), Counter())
print('-Done-')



    

