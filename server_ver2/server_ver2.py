import numpy as np
import re
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask import Flask , render_template , request
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--dir", type=str, required=True)
args = parser.parse_args(args.dir)

dirname = os.listdir()
load_models = list()

for file in dirname:
    filename = os.path.join(args.dir, file)
    ext = os.path.splitext(filename)[-1].strip()
    if ext == '.h5':
        load_models.append(tf.keras.models.load_model(filename, compile=False))
        print('>loaded %s' % filename)

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
        predicts = list()
        for i in range(len(load_models)):
            predicts.extend(load_models[i].predict(pad_sequence))
        good_pro = list()
        for i in range(len(predicts)):
            if predicts[i][0] > 0.5:
                pro = "{:.2f}".format(predicts[i][0]*100)
                good_pro.append(float(pro))
            else:
                pro = "{:.2f}".format((1-predicts[i][0])*100)
                good_pro.append(100-float(pro))
        aver_good = "{:.2f}".format(sum(good_pro) / len(good_pro))
        result = "good review : " + aver_good +" / " + " bad review : " + str(100-float(aver_good))

        return render_template('predict.html', predict=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)