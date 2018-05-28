
# coding: utf-8

# In[95]:


#Cell A [tags: #A]
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
globLearning = Counter()


# In[96]:


def LearningStateReal(poNe):
    global globalLearningReal
    globalLearningReal = poNe
    return globalLearningReal


# In[97]:


def LearningStateGuess(poNe):
    global globalLearningGuess
    globalLearningGuess = poNe
    return globalLearningGuess


# In[98]:


def nrCorrect(newCorrect):
    global globalNrCorrects
    globalNrCorrects += newCorrect
    return globalNrCorrects


# In[99]:


def nrFiles(newFiles):
    global globalNrFiles 
    globalNrFiles = globalNrFiles + newFiles
    return globalNrFiles


# In[100]:


def globalMemory(lc):
    global globLearning
    globLearning = lc
    return globLearning


# In[101]:


#Cell B [tags: #B, =>A]
def commonWordRemover(c):
    
    nonCommonWords = Counter()
    nonCommonWords.update(c)
        
    for key, count in dropwhile(lambda key_count: key_count[1] >= 600, c.most_common()): del c[key]
        
    nonCommonWords = nonCommonWords - c
    return nonCommonWords


# In[102]:


#Cell C [tags: #C, =>B]
def rareWordFinder(c):
        
    rareWords = Counter()
    rareWords = c
        
    for key, count in dropwhile(lambda key_count: key_count[1] <= 300, c.most_common()): del c[key]
        
    rareWords = rareWords - c
        
    return rareWords


# In[103]:


def singleFileWordCounter(Path):
    counter = Counter()
    #print(random.choice(os.listdir(Path)))
    file = open(random.choice(Path))
    #filepath = (Path + '/' + f1)
    #print('File = ' + f1)
    #for file in filepath:
#                print (b, end="\r"):
    #file = open(filepath)
    for x in range (0,1):
        for word in file.read().lower().split():
                    #words = re.findall(r'\w+', f.read().lower())
            counter[word] += 1
    file.close()
                
    return counter


# In[104]:


def test(posTest, negTest):
    
    r = random.randint(1, 2)
    #r = 1
    if r == 2:
        file = posTest
        #print('Filen er positiv')
        LearningStateReal(True)
        
    else:
        file = negTest               
        #print('Filen er negativ')
        LearningStateReal(False)

    #print(test_counter)
    #print(sum(test_counter.values()))
    return file


# In[105]:


#Cell D [tags: #D, =>C]
def wordCounter(filePath):
    
    #onlyfiles = next(os.walk(Path))[2]
    #totalFiles = len(onlyfiles)
    
    counter = Counter()
    f = open(filePath)
    #        i = i + 1
#            b = 'File: ' + str(i) + ' of: ' + '100' #str(totalFiles)
    for x in range (0,1):
        for word in f.read().lower().split():
                    #words = re.findall(r'\w+', f.read().lower())
            counter[word] += 1
    f.close()
                
    #for key in counter.keys():
    #    if counter[key] > 10 * i:
    #        counter[key] = 0
    return(counter)


# In[106]:


def fileFinder(dirPath, nrFiles):
    i = 0
    files = []
    filepaths = os.listdir(dirPath) #glob(os.path.join(dirPath + '*.txt'))
    for file in filepaths:
        while i <= nrFiles :
            if file.endswith(".txt"):
                files.append(os.path.join(dirPath + '/' + file))
            i += 1
    return files


# In[107]:


#Cell F [tags: #F, =>E]
def interpetFile(training, testing, pNeg, pPos):
    #status = 1
    #te = Counter()
    #te.subtract(te)
    #te.update(training)
    edu = Counter()
   # x = 0
    #while x <= len(te):
    #    key = te.iter(x)
    #    edu[key] = edu[key] * training[key]
    #    x = x + 1
    for key in testing.keys():
        edu[key] = testing[key]
        if training[key] == None:
            training[key] = 0
        if training[key] > 0:
            testing[key] = round((testing[key] * training[key]) / pPos, 3)
        elif training[key] < 0:
            testing[key] = round((testing[key] * training[key]) / pNeg, 3)
        else:
            testing[key] = 0
         
        
    #Print(te)
    
    testSum = sum(testing.values())
    

    if testSum > 0:
        #print('I guess that it is Positive')
        LearningStateGuess(True)
        
    elif testSum < 0:
        #print('I guess that it is Negative')
        LearningStateGuess(False)
        
    else:
        return training
    
     
    if globalLearningReal == True:
        training.update(edu)
        return training
    
    else:
        training.subtract(edu)
        return training
    
    #print(str(globalLearningReal))
    #print(str(globalLearningGuess))
        
    #x = 0
    #while status != 1:
    #    learning_input = input(' Please tell me whether I am right or wrong by typing  - for wrong or + for right ')
    #    if learning_input == '+' or '-':
    #        print('You typed ' + learning_input)
    #        status = 1
    #    elif learning_input != '+' or '-' and x <= 7:
    #        status = 0
    #        print('Invalid input!: ' + learning_input)
    #        x = x + 1
    #    else:
    #        print('You gave to many invalid inputs! I quit!!!')
    #        return None
            
    #print(te)
    return training


# In[108]:


#Cell E [tags: #E, =>D]
def train(train_counter, directory):
    
    print('Training...', end='\r')
    
    for file in directory:
        train_counter = interpetFile(train_counter, wordCounter(file))
        directory.remove(file)

    #pos = Counter()
    #neg = Counter()
    
    #pos += wordCounter(posDir)
    #neg += wordCounter(negDir)
        
    #train_counter += pos
    #train_counter.subtract(neg)
    
    #print(train_counter)        
    #print(sum(train_counter.values()))
    return train_counter


# In[120]:


def learn(learning):
    li = int()
    trainFiles = []
    testFiles = []
    nrCorrect(-globalNrCorrects)
    nrFiles(-globalNrFiles)
    nrPos = 1
    nrNeg = 1
    nrTotal = 2
    li2 = int(input('How many files to use as training(max10000): '), 10)
    li = int(input('How many files to test(max10000): '), 10)
    if li2 > 0 and li > 0:
        #training = train()
        negTestFiles = fileFinder('/storage/emulated/0/INFO284/test/pos', li) #str(input(' Please write directory path: ')))
        posTestFiles = fileFinder('/storage/emulated/0/INFO284/test/neg', li)
        posFiles = fileFinder('/storage/emulated/0/INFO284/train/pos', li2 / 2)
        negFiles = fileFinder('/storage/emulated/0/INFO284/train/neg', li2 / 2)
        if learning == Counter():
            learning.update(wordCounter(posFiles.pop()))
            learning.subtract(wordCounter(negFiles.pop()))
        while len(negFiles) > 0:
            LearningStateReal(True)
            learning = interpetFile(learning, wordCounter(posFiles.pop()), nrNeg / nrTotal, nrPos / nrTotal)
            nrTotal += 1            
            nrPos += 1
            LearningStateReal(False)
            learning = interpetFile(learning, wordCounter(negFiles.pop()), nrNeg / nrTotal, nrPos / nrTotal )
            nrTotal += 1
            nrNeg += 1

    #learning.update(train(learning, posFiles))
    #LearningStateReal(False)
    #pos.update(neg)
    #learning = pos
    #learning.update(train(learning, negFiles))
        while li > nrFiles(0):
            nrFiles(1)
            #print('Testing file nr: ' + str(nrFiles(1)))
        #LearningStateReal(bool())
        #LearningStateGuess(bool())
            testFile = test(posTestFiles.pop(), negTestFiles.pop())
            
            #if globalLearningReal == True:
            #    print('Positive File')
            #else:
             #   print('Negative File')
            learning = interpetFile(learning, wordCounter(testFile), nrNeg / nrTotal, nrPos / nrTotal)
            #if globalLearningGuess == True:
              #  print('Is it positive?')
            #else:
               # print('Is it negativ?')
        
            if globalLearningReal == globalLearningGuess:
                nrCorrect(1)
            else:
                nrCorrect(0)
                
            if globalLearningReal == True:
                nrPos += 1
            else:
                nrNeg+=1
            nrTotal += 1
        #if globalLearningReal == True:
        #    posTestFiles.remove(testFile)
        #elif globalLearningReal == False:
        #    negTestFiles.remove(testFile)
        
            #print('Learning...')
            print(str(globalNrCorrects) + ' of ' + str(nrFiles(0)) + ' is correct', end='\r')

    else:
        print('Invalid input: ' + str(li2) + ' ' + str(li))
    
    print(str(globalNrCorrects) + ' of ' + str(nrFiles(0)) + ' is correct')
    return learning


# In[123]:


globalMemory(Counter())
globalMemory(learn(globLearning))
print('-Done-')

