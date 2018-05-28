
# coding: utf-8

# In[2]:


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


# In[3]:


def LearningStateReal(poNe):
    global globalLearningReal
    globalLearningReal = poNe
    return globalLearningReal


# In[4]:


def LearningStateGuess(poNe):
    global globalLearningGuess
    globalLearningGuess = poNe
    return globalLearningGuess


# In[5]:


def nrCorrect(newCorrect):
    global globalNrCorrects
    globalNrCorrects += newCorrect
    return globalNrCorrects


# In[6]:


def nrFiles(newFiles):
    global globalNrFiles 
    globalNrFiles = globalNrFiles + newFiles
    return globalNrFiles


# In[7]:


def globalMemoryPos(lc):
    global globLearningPos
    globLearning = lc
    return globLearningPos


# In[8]:


def globalMemoryNeg(lc):
    global globLearningNeg
    globLearning = lc
    return globLearningNeg


# In[9]:


def commonWordRemover(c):
    
    for key in c.keys():
        if c[key] >= len(c) * 0.05:
            c[key] = 0
    return c


# In[10]:


def rareWordFinder(c):
        
    rareWords = Counter()
    rareWords = c
        
    for key, count in dropwhile(lambda key_count: key_count[1] <= 300, c.most_common()): del c[key]
        
    rareWords = rareWords - c
        
    return rareWords


# In[11]:


def singleFileWordCounter(Path):
    counter = Counter()
    file = open(random.choice(Path))
    for x in range (0,1):
        for word in file.read().lower().split():
            counter[word] = 1
    file.close()
    counter = commonWordRemover(counter)
    return counter


# In[12]:


def test(posTest, negTest):
    
    r = random.randint(1, 2)
    #r = 1
    if r == 2:
        file = posTest
        print('Filen er positiv')
        LearningStateReal(True)
        
    else:
        file = negTest               
        print('Filen er negativ')
        LearningStateReal(False)
    print(file)
    #print(test_counter)
    #print(sum(test_counter.values()))
    return file


# In[13]:


def wordCounterTrain(filePath):

    counter = Counter()
    f = open(filePath)
    c = 0
    for word in f.read().lower().split():
        counter[word] = 1
    f.close()

    #counter = commonWordRemover(counter)
    return(counter)

def wordCounterTest(filePath):
    counter = Counter()
    f = open(filePath)
    c = 0
    for word in f.read().lower().split():
        counter[word] += 1
    f.close()

    #counter = commonWordRemover(counter)
    return (counter)

# In[14]:


def fileFinder(dirPath):
    i = 0
    files = []
    filepaths = os.listdir(dirPath)
    for file in filepaths:
        if file.endswith(".txt"):
            files.append(os.path.join(dirPath + '/' + file))

    return files


# In[34]:

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

    print(posFileCount)
    pos = (pos * posFileCount) / c
    neg = (neg * negFileCount) / c
    print("POS: " + str(pos) + " NEG: " + str(neg))

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
        #print("Pos: " + str(trainingPos[key] + 1) + "\/" + str(len(trainingPos.values())))
        wordProbNeg = float(trainingNeg[key] + 1) / len(trainingNeg.values())
        neg = pos * wordProbNeg
        #print("Neg: " + str(trainingNeg[key] + 1) + "\/" + str(len(trainingNeg.values())))

        
    #posAndNeg = sum(trainingPos.values()) + sum(trainingNeg.values())
    file = (nrFiles / 2) / nrFiles
    #print(pos)
    #print(str((pos*file) / neg))
    #print(str((neg * pos) / pos))
    #print("pos: " +  str(pos) + "Slash, times" + str(file) + "slash" + str(pos) +  "slash" + str(nrFiles))

    pos = (pos * file) / (pos / nrFiles)
    #print("neg: " + str(neg) + "Slash, times" + str(file) + "slash" + str(neg) +  "slash" + str(nrFiles))

    neg = (neg * file) / (neg / nrFiles)


    if pos >= neg:
        LearningStateGuess(True)
            
    elif pos < neg:
        LearningStateGuess(False)
        
        #if testSum != 0:
        #prob = round(testSum / len(testing.values()), 5)
        #if prob != 0:
        #    if prob >= 0.5:
                #print('I guess that it is Positive')
                
        
        #    elif prob < 0.5:
                #print('I guess that it is Negative')
        #        LearningStateGuess(False)
            
        #    else:
                #print('I guess that it is Negative')
        #        LearningStateGuess(False)
        
    #else:
    #    print('I guess that it is Negative')
    #    LearningStateGuess(False)


# In[16]:


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
        #training = train()

        #LearningStateReal(True)
        if i < len(posFiles):
            learningPos.update(wordCounterTest(posFiles[i]))

        #LearningStateReal(False)
        if i < len(negFiles):
            learningNeg.update(wordCounterTest(negFiles[i]))

        i = i + 1

        #nrWords = len(learningPos) + len(learningNeg)
        #print(nrWords)

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

            # if globalLearningReal == True:
        #    nrPos += 1
        # else:
        #    nrNeg+=1

        # nrTotal += 1
        print(str(nrCorrect(0)) + ' of ' + str(nrFiles(0)) + ' is correct')

    #print(str(nrCorrect(0)) + ' of ' + str(nrFiles(0)) + ' is correct')
    #return learningPos & learningNeg


# In[18]:


def textEvaluater(text):
    words = Counter(text.lower().split())
    return words


# In[36]:


learn(Counter(), Counter())
print('-Done-')


# In[ ]:



    

