FROM tensorflow/tensorflow
LABEL email="syoon369@gmail.com"
RUN apt-get update
WORKDIR /home
ADD copier.py /home
ENTRYPOINT ["python", "copier.py"]