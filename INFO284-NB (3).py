
# coding: utf-8

# In[152]:


#Cell A [tags: #A]
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


# In[153]:


def LearningStateReal(poNe):
    global globalLearningReal
    globalLearningReal = poNe
    return globalLearningReal


# In[154]:


def LearningStateGuess(poNe):
    global globalLearningGuess
    globalLearningGuess = poNe
    return globalLearningGuess


# In[155]:


def nrCorrect(newCorrect):
    global globalNrCorrects
    globalNrCorrects += newCorrect
    return globalNrCorrects


# In[156]:


def nrFiles(newFiles):
    global globalNrFiles 
    globalNrFiles = globalNrFiles + newFiles
    return globalNrFiles


# In[157]:


def globalMemoryPos(lc):
    global globLearningPos
    globLearning = lc
    return globLearningPos


# In[158]:


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
            counter[word] += 1
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
    return file

def wordCounter(filePath):
    
    #onlyfiles = next(os.walk(Path))[2]
    #totalFiles = len(onlyfiles)
    
    counter = Counter()
    f = open(filePath)
    for x in range (0,1):
        for word in f.read().lower().split():
            counter[word] += 1
    f.close()
    
    counter = commonWordRemover(counter)

    return(counter)


# In[164]:


def fileFinder(dirPath, nrFiles):
    i = 0
    files = []
    filepaths = os.listdir(dirPath)
    for file in filepaths:
        while i < nrFiles :
            if file.endswith(".txt"):
                files.append(os.path.join(dirPath + '/' + file))
            i += 1
    return files


# In[188]:

def interpetFile(nrFiles, trainingPos, trainingNeg, testing):
    testSum = 1
    for key in testing.keys():
        posOrNeg = trainingPos[key] - trainingNeg[key]
        posFile = (nrFiles / 2)
        if posOrNeg != 0:
            pPos = posOrNeg / (trainingPos[key] + trainingNeg[key] / nrFiles)
            if posOrNeg > 0:
                testing[key] = round(((posFile / pPos) * pPos) / posFile, 5)
                testSum = round(testSum * testing[key], 10)

    if testSum >= 0.5:
        print('I guess that it is Positive')
        LearningStateGuess(True)
        
    elif testSum < 0.5:
        print('I guess that it is Negative')
        LearningStateGuess(False)
        
    else:
        print('wrong')
        LearningStateGuess(bool)

def train(train_counter, directory):
    
    print('Training...', end='\r')
    
    for file in directory:
        train_counter = interpetFile(train_counter, wordCounter(file))
        directory.remove(file)
    return train_counter


# In[170]:


def learn(learningPos, learningNeg):
    li = int()
    trainFiles = []
    testFiles = []
    nrCorrect(-globalNrCorrects)
    nrFiles(-globalNrFiles)
    nrPos = 1
    nrNeg = 1
    nrTotal = 2
    li2 = int(input('How many files to use as training(max 20000): '), 10)
    li = int(input('How many files to test(max 10000): '), 10)
    if li2 > 0 and li >= 0:
        #training = train()
        posFiles = fileFinder('/storage/emulated/0/INFO284/test/pos', li2 / 2) #fileFinder(str(input(' Please write the path of the directory for positive training files: ')), li2 / 2)
        negFiles = fileFinder('/storage/emulated/0/INFO284/test/neg', li2 / 2) #fileFinder(str(input(' Please write the path of the directory for negative training files: ')), li2 / 2)
        if learningPos == Counter():
            learningPos = wordCounter(posFiles.pop())
        if learningNeg == Counter():
            learningNeg.update(wordCounter(negFiles.pop()))
        while len(negFiles) > 0 & len(posFiles) > 0:
            #LearningStateReal(True)
            learningPos.update(wordCounter(posFiles.pop()))
            #LearningStateReal(False)
            learningNeg.update(wordCounter(negFiles.pop()))
        #nrWords = len(learningPos) + len(learningNeg)
        #print(nrWords)
        
        if li == 0:
            text = textEvaluater(str(input('Please write a review for me to evaluate: ')))
            nrFiles(1)
            interpetFile(li2, learningPos, learningNeg, text)
            if globalLearningGuess == True:
                print('I belive that the text is positive')
            else:
                print('I belive that the text is negative')
            rw = str(input('Please type + if my guess was correct, or - if it was incorrect: '))
            if rw == '+':
                print('Yay! I was right :)')
                nrCorrect(1)
            elif rw == '-':
                print('So I was wrong this time? I guess I should do some more training then.')
            else:
                print('Incorrect input. Ending process')
        else:
            negTestFiles = fileFinder('/storage/emulated/0/INFO284/test/neg', li) #fileFinder(str(input('Please write the path of the directory for negative test files: ')), li)
            posTestFiles = fileFinder('/storage/emulated/0/INFO284/test/pos', li) #fileFinder(str(input('Please write the path of the directory for positive test files: ')), li)
            
            while li > nrFiles(0):
                nrFiles(1)
                testFile = test(posTestFiles.pop(), negTestFiles.pop())
            
                interpetFile(li2, learningPos, learningNeg, wordCounter(testFile))
        
                if globalLearningReal == globalLearningGuess:
                    nrCorrect(1)                    
                
                if globalLearningReal == True:
                    nrPos += 1
                else:
                    nrNeg+=1
                    
                nrTotal += 1
                print(str(nrCorrect(0)) + ' of ' + str(nrFiles(0)) + ' is correct', end='\r')

    else:
        print('Invalid input: ' + str(li2) + ' ' + str(li))
    
    print(str(nrCorrect(0)) + ' of ' + str(nrFiles(0)) + ' is correct')
    return learningPos & learningNeg


# In[168]:


def textEvaluater(text):
    words = Counter(text.lower().split())
    #words = Counter()
    #for word in text.read().lower().split():
    #    words[word] += 1
    return words


# In[189]:


learn(Counter(), Counter())
print('-Done-')


# In[ ]:



    

