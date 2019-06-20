import random
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
from flask import Flask, request, render_template, jsonify


with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('', 'rb') as e:
    extractor = pickle.load(e)
app = Flask(__name__, static_url_path="")

@app.route('/')
def index():
    """Return the main page."""
    return render_template('theme2.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Return a prediction of P(spam)."""
    answer = ['Hero','Villain']
    data = request.json
    
    prediction = model.predict_proba([data['user_input']])
    if prediction[0][1] > 0.5:
        i = 0
    else:
        i = 1
    prediction_name = answer[i]
    return prediction_name

