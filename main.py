# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 12:06:59 2021

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
app = Flask(__name__)
print('successfully load model')
#model = urllib.request.urlretrieve ("https://storage.googleapis.com/covid-th/model.joblib", "static/model.joblib")
#m = jl.load("static/model.joblib")
versions = 1.0
@app.route('/', methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/check_version', methods=['GET','POST'])
def check_version():
    return jsonify(version=str(versions))

@app.route('/awake', methods=['GET','POST'])
def awake():
    return render_template('home.html')

@app.route('/api', methods=["POST","GET"])
def send_response():
    if True:
        opt = interpret_request(request.get_json())
        model = jl.load('static/model/vectorizer_'+str(opt['questionId'][0]+'.joblib'))
        data, corpus = query(source, opt['questionId'][0], model)
        output_prob = interpret_meaning(opt, model, corpus)
        prob = np.argmax(output_prob)

        if output_prob[0][prob] > 0.3:    
            output = jsonify(questionId=opt['questionId'][0], answer = str(data['answer'].iloc[prob]),
                         meaning = int(data['meaning'].iloc[prob]), label = str(data['label'].iloc[prob]))
        else:
            output = jsonify(questionId=opt['questionId'][0], answer = None,
                         meaning = None, label = 'null')
    return output

def query(data, questionId, model):
    data = data[data['questionId']==questionId].reset_index(drop=True)
    d = []
    for i in range(len(data)):
        a =  data['answer'].iloc[i]
        d.append(pythainlp.word_tokenize(a))
    tokens_list_j = [','.join(tkn) for tkn in d]
    corpus = model.transform(tokens_list_j).toarray()
    return data, corpus

def sp(x):
    return x.split(',')

def interpret_request(data_):
    output = pd.Series(data_).to_frame()
    output = output.T
    pred_ = output[['questionId','answer', 'dataType']]
    return pred_

def interpret_meaning(data_, model, corpus):
    tokenize = []
    temp_word =  data_['answer'][0]
    tokenize.append(pythainlp.word_tokenize(temp_word))
    tokenize= [','.join(tkn) for tkn in tokenize]
    token_transform = model.transform(tokenize).toarray()
    q = pairwise.cosine_similarity(token_transform, corpus)

    return q


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

