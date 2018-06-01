
from collections import Counter
import os

globalNrCorrects = 0
globalNrFiles = 0
globalLearningReal = bool()
globalLearningGuess = bool()

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

'''
Counts occourances of unique words in a file
@param filePath: Path to file
'''
def wordCounter(filePath):
    counter = Counter()
    f = open(filePath)
    c = 0
    for word in f.read().lower().split():
        counter[word] += 1
    f.close()

    return (counter)

'''
iterates through a directory and finds the path of all files with .txt extension.
@param dirPath: Path of directory to files
'''
def fileFinder(dirPath):
    i = 0
    files = []
    filepaths = os.listdir(dirPath)
    for file in filepaths:
        if file.endswith(".txt"):
            files.append(os.path.join(dirPath + '/' + file))

    return files

'''
Interprets file, and using naive bayes predicts weather the file is positive or negative
@param nrFiles: Number of files
@param trainingPos: Counter of positive words
@param trainingNeg: Counter of negative words
@param testing: Counter of occouranses of each unique word in file
@param trainingFull: Counter of total accourances of all words
@param posFileCount: Count of positive files
@param negFileCount: Count of negative files
'''
def interpetFile(nrFiles, trainingPos, trainingNeg, testing, trainingFull, posFileCount, negFileCount):
    pos = 1.0
    neg = 1.0
    c = 1.0

    nrFiles = float(nrFiles)

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

'''
Learning and testing the algorithm with data from a dataset
'''
def learn():
    learningPos = Counter()
    learningNeg = Counter()
    nrCorrect(-globalNrCorrects)
    nrFiles(-globalNrFiles)
    posFiles = fileFinder(str(input('Please write the path of the directory for positive training files: ')))
    negFiles = fileFinder(str(input('Please write the path of the directory for negative training files: ')))
    posTestFiles = fileFinder(str(input('Please write the path of the directory for positive test files: ')))
    negTestFiles = fileFinder(str(input('Please write the path of the directory for negative test files: ')))
    allTrainingFiles = list(set().union(posFiles, negFiles))
    allTestFiles = list(set().union(posTestFiles, negTestFiles))

    trainingFull = Counter()

    print('Training algorithm..')
    i = 0

    while i < len(allTrainingFiles):

        if i < len(posFiles):
            learningPos.update(wordCounter(posFiles[i]))

        if i < len(negFiles):
            learningNeg.update(wordCounter(negFiles[i]))

        i = i + 1


    i = 0
    trainingFull.update(learningNeg)
    trainingFull.update(learningPos)

    pos_ct = float(len(posFiles)) / len(allTrainingFiles)
    neg_ct = float(len(negFiles)) / len(allTrainingFiles)

    print('Testing algorithm..')
    for file in allTestFiles:
        testFile = file

        nrFiles(1)

        interpetFile(len(allTrainingFiles), learningPos, learningNeg, wordCounter(testFile), trainingFull, pos_ct, neg_ct)

        if globalLearningReal == globalLearningGuess:
            nrCorrect(1)

    print(str(nrCorrect(0)) + ' of ' + str(nrFiles(0)) + ' is correct')

# starting the training and testing
learn()
print('-Done-')