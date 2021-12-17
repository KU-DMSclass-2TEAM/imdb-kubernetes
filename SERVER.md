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

### upload / 예측 api
client로 부터 받은 문자열 (영화 리뷰) 이 긍정 리뷰인지 부정 리뷰인지 예측 한다.
<method는 POST>

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

# server_ver2
Python, flask framework 사용

* 함수 
    - prepro_sentence({문자열})
    - predict()
    - index()
    - upload()