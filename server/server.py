# -*- coding: utf-8 -*-
import numpy as np
import re
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask import Flask, render_template, request
from werkzeug import secure_filename
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True)
args = parser.parse_args()

model = tf.keras.models.load_model(args.model, compile=False)
model._make_predict_function()
session = tf.keras.backend.get_session()

app = Flask(__name__)

def prepro_sentence(new_sentence):
    new_sentence = re.sub('[^0-9a-zA-Z]', '', new_sentence).lower()
    
    word_to_index = imdb.get_word_index()
    
    encoded = []
    for word in new_sentence.split():
        try:
            if word_to_index[word] <= 10000:
                encoded.append(word_to_index[word]+3)
            else:
                encoded.append(2)
        except KeyError:
            encoded.append(2)
    return encoded
            
@app.route('/') 
def index():
   return render_template('index.html') 

@app.route('/upload', methods=['POST']) 
def upload():
    if request.method == 'POST': 
        data = request.form['review'] 
        pad_sequence = pad_sequences([prepro_sentence(str(data))], maxlen = 500)
        
        with session.as_default():
            predict = float(model.predict(pad_sequence))
            if predict > 0.5:
                result = "{:.2f}% _good".format(predict*100)
            else:
                result = "{:.2f}% _bad".format((1-predict)*100)
    

    
        return render_template('predict.html', predict=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)