import numpy as np
import codecs
import pandas as pd

import urllib

import sklearn
from sklearn.naive_bayes import GaussianNB

from sklearn import metrics
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score

doc = codecs.open('dataset.txt', 'rU', 'UTF-8')

dataset = pd.read_csv(doc, sep='\t', lineterminator='\r', header=None)

x = dataset.iloc[:, 0:23]
y = dataset.iloc[:, 0]


x_train, y_train, x_test, y_test = train_test_split(x, y, test_size=.33, random_state=17)


GausNB = GaussianNB()

GausNB.fit(x_train, y_train)
