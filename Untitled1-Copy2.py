
# coding: utf-8

# In[132]:


from glob import glob
from collections import Counter
import re
import os
import time
from itertools import dropwhile
import random
import tempfile
globalNrCorrects = 0
globalNrFiles = 0
globalLearningReal = bool()
globalLearningGuess = bool()
globLearning = None


# In[133]:


def LearningStateReal(poNe):
    global globalLearningReal
    globalLearningReal = poNe
    return globalLearningReal


# In[134]:


def LearningStateGuess(poNe):
    global globalLearningGuess
    globalLearningGuess = poNe
    return globalLearningGuess


# In[135]:


def nrCorrect(newCorrect):
    global globalNrCorrects
    globalNrCorrects += newCorrect
    return globalNrCorrects


# In[136]:


def nrFiles(newFiles):
    global globalNrFiles 
    globalNrFiles = globalNrFiles + newFiles
    return globalNrFiles


# In[137]:


def globalMemory(lc):
    global globLearning
    globLearning = lc
    return globLearning


# In[140]:


def singleFileWordCounter(Path):
    counter = Counter()
    file = open(random.choice(Path))
    for x in range (0,1):
        for word in file.read().lower().split():
            counter[word] += 1
    file.close()
                
    return counter


# In[178]:


def test(posTest, negTest):
    test_counter = Counter()
    r = random.randint(1, 2)
    #r = 1
    if r == 2:
        file = posTest.pop()
        LearningStateReal(True)
        
    else:
        file = posTest.pop()               
        LearningStateReal(False)
    
    test_counter += Counter()
    return file


# In[142]:


def wordCounter(filePath):
    
    counter = Counter()
    f = open(filePath)
    for x in range (0,1):
        for word in f.read().lower().split():
            counter[word] += 1
    f.close()
    return(counter)


# In[171]:


def fileFinder(dirPath, nrFiles):
    i = 0
    files = []
    filepaths = os.listdir(dirPath)
    for file in filepaths:
        while i <= nrFiles :
            if file.endswith(".txt"):
                files.append(os.path.join(dirPath + '/' + file))
            i += 1
    return files


# In[153]:


def interpetFile(training, testing):
    edu = Counter()
    for key in testing.keys():
        testing[key] = testing[key] * training[key]
        edu[key] = 1
         
    testSum = sum(testing.values())

    if testSum > 0:
        LearningStateGuess(True)
        
    elif testSum < 0:
        LearningStateGuess(False)
        
    else:
        return training
    
     
    if globalLearningReal == True:
        training.update(edu)
        return training
    
    else:
        training.subtract(edu)
        return training
    
    return training


# In[3]:


def train(train_counter, directory):
    
    print('Training...', end='\r')
    
    for file in directory:
        train_counter = interpetFile(train_counter, wordCounter(file))
        directory.remove(file)
    return train_counter


# In[ ]:


def learn(learning):
    li = int()
    trainFiles = []
    testFiles = []
    nrCorrect(-globalNrCorrects)
    nrFiles(-globalNrFiles)
    li2 = int(input('How many files to use as training(max500): '), 10)
    li = int(input('How many files to test(max500): '), 10)
    if li >= nrFiles(0):
        negTestFiles = fileFinder('/storage/emulated/0/INFO284/test/pos', li)
        posTestFiles = fileFinder('/storage/emulated/0/INFO284/test/neg', li)
        testFiles.extend(posTestFiles)
        testFiles.extend(negTestFiles)
        posFiles = fileFinder('/storage/emulated/0/INFO284/train/pos', li2 / 2 + 1)
        negFiles = fileFinder('/storage/emulated/0/INFO284/train/neg', li2 / 2)
        if learning == None:
            learning = wordCounter(posFiles.pop())
        while len(negFiles) > 0:
            LearningStateReal(True)
            learning = interpetFile(learning, wordCounter(posFiles.pop()))
            LearningStateReal(False)
            learning = interpetFile(learning, wordCounter(negFiles.pop()))
            
        while li - 1 >= nrFiles(0):
            testFile = test(posTestFiles, negTestFiles)
            learning = interpetFile(learning, wordCounter(testFile))
            if globalLearningReal == globalLearningGuess:
                nrCorrect(1)
            else:
                nrCorrect(0)
            print('  ' + str(globalNrCorrects) + ' of ' + str(nrFiles(1)) + ' is correct', end='\r')

    else:
        print('Invalid input: ' + str(li))
    
    
    return learning


# In[ ]:


globalMemory(learn(globLearning))
print('done :)')

