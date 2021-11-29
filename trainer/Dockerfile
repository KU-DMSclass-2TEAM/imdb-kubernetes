FROM tensorflow/tensorflow
LABEL email="syoon369@gmail.com"
RUN apt-get update
WORKDIR /home
ADD trainer.py /home
ENTRYPOINT ["python", "trainer.py"]