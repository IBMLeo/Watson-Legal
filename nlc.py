from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble
from sklearn.naive_bayes import GaussianNB
import pandas, xgboost, numpy, textblob, string
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template

app = Flask(__name__)

# load the dataset
data = open('NLC_NEW2.csv').read()
labels, texts = [], []

for i, line in enumerate(data.split("\n")):
    content = line.split(',')
    labels.append(content[1])
    texts.append(content[0])

trainDF = pandas.DataFrame()
trainDF['text'] = texts
trainDF['label'] = labels

v = TfidfVectorizer(use_idf = True)  
texts = v.fit_transform(texts).toarray()  

mnb = naive_bayes.MultinomialNB()
mnb = mnb.fit(texts, labels)  

cache = {}

@app.route('/processa', methods=['POST'])
def processa():
    txt = request.form['valor']
    test = v.transform([txt]).toarray()
    if txt in cache:
        return cache[txt]
    else:
        prediction = mnb.predict(test)
        cache[txt] = str(prediction[0])
        return str(prediction[0])

app.run(port=3001)