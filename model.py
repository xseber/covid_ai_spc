# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 18:58:38 2020

@author: xseber
"""


import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from pythainlp import word_tokenize
from sklearn import tree

data = pd.read_csv('meaningLib.csv')
d = []
for i in range(len(data)):
    a = data['questionId'].iloc[i] + " " + data['answer'].iloc[i]
    d.append(word_tokenize(a))

tfigf = TfidfVectorizer(analyzer= lambda x: x.split(','))
tokens_list_j = [','.join(tkn) for tkn in d]
tfigf.fit(tokens_list_j)

model = tree.DecisionTreeClassifier()



