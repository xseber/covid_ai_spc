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

data = pd.read_csv('meaningLibs.csv')
d = []
for i in range(len(data)):
    a = data['questionId'].iloc[i] + " " + data['answer'].iloc[i]
    d.append(pythainlp.word_tokenize(a))

tfigf = TfidfVectorizer(analyzer= lambda x: x.split(','))
tokens_list_j = [','.join(tkn) for tkn in d]
tfigf.fit(tokens_list_j)
corpus = tfigf.transform(tokens_list_j).toarray()
app = Flask(__name__)
print('successfully load model')
#model = urllib.request.urlretrieve ("https://storage.googleapis.com/covid-th/model.joblib", "static/model.joblib")
#m = jl.load("static/model.joblib")

@app.route('/', methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/awake', methods=['GET','POST'])
def awake():
    return render_template('home.html')

@app.route('/api', methods=["POST","GET"])
def send_response():
    if True:
        opt = interpret_request(request.get_json())
        output_prob = interpret_meaning(opt, tfigf, corpus)
        prob = np.argmax(output_prob)

        if output_prob[0][prob] > 0.3:    
            output = jsonify(questionId=opt['questionId'][0], answer = str(data['answer'].iloc[prob]),
                         meaning = int(data['meaning'].iloc[prob]), label = str(data['label'].iloc[prob]))
        else:
            output = jsonify(questionId=opt['questionId'][0], answer = None,
                         meaning = None, label = 'null')
    return output

def interpret_request(data_):
    output = pd.Series(data_).to_frame()
    output = output.T
    pred_ = output[['questionId','answer', 'dataType']]
    return pred_

def interpret_meaning(data_, model, corpus):
    tokenize = []
    temp_word = data_['questionId'][0] + " " + data_['answer'][0]
    tokenize.append(pythainlp.word_tokenize(temp_word))
    tokenize= [','.join(tkn) for tkn in tokenize]
    token_transform = model.transform(tokenize).toarray()
    q = pairwise.cosine_similarity(token_transform, corpus)

    return q




if __name__ == '__main__':
    app.run()