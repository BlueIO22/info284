
# coding: utf-8

# In[12]:


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
globalLearningGuess = int()


# In[13]:


def LearningStateReal(poNe):
    global globalLearningReal
    globalLearningReal = poNe
    return globalLearningReal


# In[14]:


def LearningStateGuess(poNeNu):
    global globalLearningGuess
    globalLearningGuess = 0
    globalLearningGuess += poNeNu
    return globalLearningGuess


# In[15]:


def nrCorrect(newCorrect):
    global globalNrCorrects 
    globalNrCorrects = globalNrCorrects + newCorrect
    return globalNrCorrects


# In[16]:


def nrFiles(newFiles):
    global globalNrFiles 
    globalNrFiles = globalNrFiles + newFiles
    return globalNrFiles


# In[17]:


#Cell B [tags: #B, =>A]
def commonWordRemover(c):
    
    nonCommonWords = Counter()
    nonCommonWords.update(c)
        
    for key, count in dropwhile(lambda key_count: key_count[1] >= 600, c.most_common()): del c[key]
        
    nonCommonWords = nonCommonWords - c
    return nonCommonWords


# In[18]:


#Cell C [tags: #C, =>B]
def rareWordFinder(c):
        
    rareWords = Counter()
    rareWords = c
        
    for key, count in dropwhile(lambda key_count: key_count[1] <= 300, c.most_common()): del c[key]
        
    rareWords = rareWords - c
        
    return rareWords


# In[19]:


def singleFileWordCounter(Path):
    counter = Counter()
    f1 = random.choice(os.listdir(Path))
    file = glob(os.path.join(Path + '/' + f1))
    print('File = ' + f1)
    for x in range (0,1):
        with open(Path + '/' + f1) as f:
            words = re.findall(r'\w+', f.read().lower())
            #print(words)
            counter = counter + Counter(words)
                
    return counter


# In[20]:


#Cell D [tags: #D, =>C]
def wordCounter(Path):
    
    onlyfiles = next(os.walk(Path))[2]
    totalFiles = len(onlyfiles)
    
    counter = Counter()
    fileCounter = Counter()
    i = 0
    a = 0
        
    filepaths = glob(os.path.join(Path + '/*.txt'))
    for file in filepaths:
        if i >= 200:    
            break
        else:
            i = i + 1
#            b = 'File: ' + str(i) + ' of: ' + '100' #str(totalFiles)
            for x in range (0,1):
#                print (b, end="\r")
                with open(file) as f:
                    words = re.findall(r'\w+', f.read().lower())
                    counter = counter + Counter(words)
                
    for key in counter.keys():
        if counter[key] > 10 * i:
            counter[key] = 0
    return(counter)


# In[21]:


#Cell E [tags: #E, =>D]
def train():
    
    print('Training...', end='\r')

    train_counter = Counter()
    pos = Counter()
    neg = Counter()
    
    pos += wordCounter('/storage/emulated/0/INFO284/train/pos')
    neg += wordCounter('/storage/emulated/0/INFO284/train/neg')
        
    train_counter += pos
    train_counter.subtract(neg)
    
    #print(train_counter)        
    #print(sum(train_counter.values()))
    return train_counter


# In[22]:


def test():
    test_counter = Counter()
    r = random.randint(1, 2)
    #r = 1
    if r == 2:
        test_counter = singleFileWordCounter('/storage/emulated/0/INFO284/test/pos') 
        print('Filen er positiv')
        LearningStateReal(True)
        
    else:
        test_counter = singleFileWordCounter('/storage/emulated/0/INFO284/test/neg')
        print('Filen er negativ')
        LearningStateReal(False)
    
    test_counter += Counter()
    #print(test_counter)
    #print(sum(test_counter.values()))
    return test_counter


# In[23]:


#Cell F [tags: #F, =>E]
def interpetRandomFile(training):
    status = 1
    #te = Counter()
    te = test()
    #te.subtract(te)
    #te.update(training)
    edu = te
    x = 0
    #while x <= len(te):
    #    key = te.iter(x)
    #    edu[key] = edu[key] * training[key]
    #    x = x + 1
    for key in te.keys():
        te[key] = te[key] * training[key]
        
    #Print(te)
    
    testSum = sum(te.values())
    #print(testSum)

    if testSum > 0:
        print('I guess that it is Positive')
        LearningStateGuess(1)
    elif testSum == 0:
        print('I guess that it is Neutral')
        LearningStateGuess(0)
    elif testSum < 0:
        print('I guess that it is Negative')
        LearningStateGuess(-1)
        
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

    if status == 1:
        if globalLearningReal == True and globalLearningGuess == 1:
            nrCorrect(1)
            for key in te.keys():
                if te[key] == 0:
                    te[key] = 2
                else:
                    te[key] = 1
                    
        elif globalLearningReal == False and globalLearningGuess == -1:
            nrCorrect(1)
            i = 0
            for key in te.keys():
                if te[key] == 0:
                    te[key] = -2
                else:
                    te[key] = -1
                
        elif globalLearningReal == False and globalLearningGuess == 1:
            for key in te.keys():
                if te[key] == 0:
                    te[key] = -2
                else:
                    te[key] = -1
                
        elif globalLearningReal == True and globalLearningGuess == -1:
            i = 0
            for key in te.keys():
                if te[key] == 0:
                    te[key] = 2
                else:
                    te[key] = 1
                
        elif globalLearningGuess == 0:
            i = 0
            for key in te.keys():
                te[key] = 0
            
        else:
            print('error!!!')
        
    else:
        print('Unknown error??! status: ' + status + 'input: ' + learning_input)
            
    #print(te)
    return te


# In[24]:


li = int()
learning = Counter()
#training = Counter()
nrCorrect(-globalNrCorrects)
nrFiles(-globalNrFiles)
li = 50 #int(input('Please type an integer between 1 and 10: '), 10)
if li <= 50 and li >= 1:
    #training = train()
    learning = train()
    while li >= 1:
        nrFiles(1)
        print('  Testing file nr: ' + str(nrFiles(0)))
        LearningStateReal(bool())
        LearningStateGuess(int())
        learning.update(interpetRandomFile(learning))
        li = li - 1
        
        print('Learning...')
        print(str(nrCorrect(0)) + ' of ' + str(nrFiles(0)) + ' is correct')

else:
    print('Invalid input: ' + str(li))
    
print('done :)')

