# Dockerfile

base 는 tensorflow/tensorflow 로 작성

|제목|설명|
|테스트2|테스트3|
|테스트2|테스트3|
|테스트2|테스트3|

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