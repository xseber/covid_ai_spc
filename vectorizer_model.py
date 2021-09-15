# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 18:56:21 2021

@author: xseber
"""

import pandas as pd
import joblib as jl
import urllib
import json
import numpy as np
import pythainlp
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, jsonify, request, render_template
from sklearn import tree
from sklearn.pipeline import Pipeline
from sklearn.metrics import pairwise
import joblib as jl
source = pd.read_csv('meaningLibs.csv')
def sp(x):
    return x.split(',')
for ids in source['questionId'].drop_duplicates():
    data = source[source['questionId']==str(ids)].reset_index(drop=True)
    d = []
    for i in range(len(source)):
        a =  source['answer'].iloc[i]
        d.append(pythainlp.word_tokenize(a))
    
    tfigf = TfidfVectorizer(analyzer= sp)
    tokens_list_j = [','.join(tkn) for tkn in d]
    tfigf.fit(tokens_list_j)
    #corpus = tfigf.transform(tokens_list_j).toarray()
    jl.dump(tfigf, 'static/model/vectorizer_'+str(ids)+'.joblib')

