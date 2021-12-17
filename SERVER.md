# server
Python, flask framework 사용
* 함수
    - prepro_sentence({문자열})
    - index()
    - upload()

### prepro_sentence
입력된 문장에 대해서 전처리, 정수 인코딩을 수행하는 함수이다.
1. 알파벳과 숫자를 제외하고 모두 제거 하며, 소문자화 한다.
2. 정수로 인코딩 하는 과정이다. 단어 집합의 크기를 10,000으로 제한하고 10,000이상의 숫자와 단어 집합에 없는 단어는 <unk> 토큰으로 변환한다.

```c
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
```

### index
초기 화면

    @app.route('/') 
        def index():
            return render_template('index.html') 

### upload / 예측 api
client로 부터 받은 문자열 (영화 리뷰) 이 긍정 리뷰인지 부정 리뷰인지 예측 한다.
1. 문자열을 prepro_sentence를 통해 인코딩을 하고 패딩을 수행한다.
2. model.predict(패딩한 값)을 통해 예측값을 얻는다.
* method는 POST
* model file은 volume에 저장되어 있다.

```c
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
```

# server_ver2
Python, flask framework 사용

* 함수 
    - prepro_sentence({문자열})
    - predict(pad_sequence)
    - index()
    - upload()

### prepro_sentence
위 내용과 같다.

### predict(pad_sequence)
분산으로 수행된 모델을 통해 예측 하는 함수
1. load된 모델 여러개로 predict을 수행한다.
2. 예측값들을 총합하여 평균을 계산한다.

```c
def predict(pad_sequence):
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
    return aver_good
```

### index
위 내용과 같다.

### upload / 예측 api
1. 위 내용과 같다.
2. predict(pad_sequence) 함수를 수행하여 얻은 결과물을 출력.

```c
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        data = request.form['review']
        pad_sequence = pad_sequences([prepro_sentence(str(data))], maxlen = 500)
        aver_good = predict(pad_sequence)
        result = "good review : " + aver_good +" / " + " bad review : " + str(100-float(aver_good))

        return render_template('predict.html', predict=result)
```
