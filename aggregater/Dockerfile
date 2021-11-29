FROM tensorflow/tensorflow
LABEL maintainer="kkp6249@gmail.com"
RUN apt-get update
WORKDIR /home
ADD aggregater.py /home
ENTRYPOINT ["python", "aggregater.py"]
