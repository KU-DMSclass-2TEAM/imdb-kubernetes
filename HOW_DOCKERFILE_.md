# Dockerfile

base 는 tensorflow/tensorflow 로 작성

|명령|설명|
|-----|-------------|
|FROM|베이스 이미지 지정 명령|
|LABEL|버전 정보, 작성자와 같은 이미지 설명을 작성하기 위한 명령|
|WORKDIR|docker 컨테이너에서의 작업 디렉토리 설정|
|ADD|파일, 디렉토리, 또는 특정 URL의 데이터를 docker 이미지에 추가|
|ENTRYPOINT|docker 컨테이너가 시작할 때, 실행하는 쉘 명령을 지정하는 명령|

## splitter
```c
FROM tensorflow/tensorflow
LABEL email="syoon369@gmail.com"
RUN apt-get update
WORKDIR /home
ADD splitter.py /home
ENTRYPOINT ["python", "splitter.py"]
```

## copier
```c
FROM tensorflow/tensorflow
LABEL email="syoon369@gmail.com"
RUN apt-get update
WORKDIR /home
ADD copier.py /home
ENTRYPOINT ["python", "copier.py"]
```

## trainer
```c
FROM tensorflow/tensorflow
LABEL email="syoon369@gmail.com"
RUN apt-get update
WORKDIR /home
ADD trainer.py /home
ENTRYPOINT ["python", "trainer.py"]
```

## aggregator
```c
FROM tensorflow/tensorflow
LABEL maintainer="kkp6249@gmail.com"
RUN apt-get update
WORKDIR /home
ADD aggregater.py /home
ENTRYPOINT ["python", "aggregater.py"]
```

## server
```c
FROM tensorflow/tensorflow
LABEL email="kkp6249@gmail.com"
RUN pip install flask flask_dropzone && \
  mkdir /home/uploads
ADD server.py /home/
ADD templates /home/templates
WORKDIR /home/uploads
ENTRYPOINT ["python", "/home/server.py"]
```

## server_ver2
```c
FROM tensorflow/tensorflow
LABEL email="kkp6249@gmail.com"
RUN pip install flask flask_dropzone && \
  mkdir /home/uploads
ADD server_ver2.py /home/
ADD templates /home/templates
WORKDIR /home/uploads
ENTRYPOINT ["python", "/home/server_ver2.py"]
```
