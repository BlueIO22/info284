
# coding: utf-8

# In[5]:


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
globalLearningGuess = int()


# In[19]:


def LearningStateReal(poNe):
    global globalLearningReal
    globalLearningReal = poNe


# In[20]:


def LearningStateGuess(poNe):
    global globalLearningGuess
    globalLearningGuess = poNe


# In[8]:


def nrCorrect(newCorrect):
    global globalNrCorrects
    globalNrCorrects = globalNrCorrects + newCorrect
    return globalNrCorrects


# In[9]:


def nrFiles(newFiles):
    global globalNrFiles 
    globalNrFiles = globalNrFiles + newFiles
    return globalNrFiles


# In[10]:


#Cell B [tags: #B, =>A]
def commonWordRemover(c):
    
    nonCommonWords = Counter()
    nonCommonWords.update(c)
        
    for key, count in dropwhile(lambda key_count: key_count[1] >= 600, c.most_common()): del c[key]
        
    nonCommonWords = nonCommonWords - c
    return nonCommonWords


# In[11]:


#Cell C [tags: #C, =>B]
def rareWordFinder(c):
        
    rareWords = Counter()
    rareWords = c
        
    for key, count in dropwhile(lambda key_count: key_count[1] <= 300, c.most_common()): del c[key]
        
    rareWords = rareWords - c
        
    return rareWords


# In[12]:


def singleFileWordCounter(Path):
    counter = Counter()
    #print(random.choice(os.listdir(Path)))
    file = random.choice(Path)
    #filepath = (Path + '/' + f1)
    #print('File = ' + f1)
    #for file in filepath:
#                print (b, end="\r"):
    #file = open(filepath)
    for x in range (0,1):
        for word in open(file).read().lower().split():
                    #words = re.findall(r'\w+', f.read().lower())
            counter[word] += 1
    file.close()
    Path.remove(file)
                
    return counter


# In[13]:


def test(posTest, negTest):
    test_counter = Counter()
    r = random.randint(1, 2)
    #r = 1
    if r == 2:
        test_counter = singleFileWordCounter(posTest) 
        print('Filen er positiv')
        LearningStateReal(True)
        
    else:
        test_counter = singleFileWordCounter(negTest)
        print('Filen er negativ')
        LearningStateReal(False)
    
    test_counter += Counter()
    #print(test_counter)
    #print(sum(test_counter.values()))
    return test_counter


# In[14]:


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


# In[41]:


def fileFinder(dirPath, nrFiles):
    i = 0
    files = []
    filepaths = glob(os.path.join(dirPath + '/*.txt'))
    for file in filepaths:
        if i <= nrFiles:
            files.extend([file])
        else:
            return files


# In[16]:


#Cell F [tags: #F, =>E]
def interpetFile(training, file):
    status = 1
    #te = Counter()
    testing = wordCounter(file)
    #te.subtract(te)
    #te.update(training)
    edu = Counter()
    x = 0
    #while x <= len(te):
    #    key = te.iter(x)
    #    edu[key] = edu[key] * training[key]
    #    x = x + 1
    for key in testing.keys():
        testing[key] = testing[key] * training[key]
        edu[key] = 1
         
        
    #Print(te)
    
    testSum = sum(testing.values())
    #print(testSum)
    

    if testSum > 0:
        #print('I guess that it is Positive')
        LearningStateGuess(True)
        
    elif testSum < 0:
        #print('I guess that it is Negative')
        LearningStateGuess(False)
        
    else:
        return training
     
    
            
    if globalLearningReal == globalLearningGuess:
        nrCorrect(1)
    else:
        nrCorrect(0)
        
    if globalLearningReal == True:
        training.update(edu)
        return training
    
    else:
        training.subtract(edu)
        return training
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


# In[17]:


#Cell E [tags: #E, =>D]
def train(directory):
    
    print('Training...', end='\r')

    train_counter = Counter()
    for file in directory:
        train_counter = interpetFile(train_counter)
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


# In[44]:


li = int()
learning = Counter()
nrCorrect(-globalNrCorrects)
nrFiles(-globalNrFiles)
li = 50 #int(input('Please type an integer between 1 and 10: '), 10)
if li <= 50 and li >= 1:
    #training = train()
    negTestFiles = fileFinder('/storage/emulated/0/INFO284/test/pos', 100)
    posTestFiles = fileFinder('/storage/emulated/0/INFO284/test/neg', 100)
    posFiles = fileFinder('/storage/emulated/0/INFO284/train/pos', 100)
    negFiles = fileFinder('/storage/emulated/0/INFO284/train/neg', 100)
    LearningStateReal(True)
    learning = train(posFiles)
    LearningStateReal(False)
    learning.update(train(negFiles))
    while li >= 1:
        nrFiles(1)
        print('Testing file nr: ' + str(nrFiles(0)))
        LearningStateReal(bool())
        LearningStateGuess(bool())
        testFile = test(posTestFiles, negTestFiles)
        learning = interpetFile(learning, testFile)
        if globalLearningReal == True:
            posTestFiles.remove(testFile)
        elif globalLearningReal == False:
            negTestFiles.remove(testFile)
        li = li - 1
        
        print('Learning...')
        print('  ' + str(nrCorrect(0)) + ' of ' + str(nrFiles(0)) + ' is correct')

else:
    print('Invalid input: ' + str(li))
    
print('done :)')

