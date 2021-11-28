FROM tensorflow/tensorflow:1.13.1 
LABEL email="syoon369@gmail.com"
RUN apt-get update
WORKDIR /home
ADD trainer.py /home
ENTRYPOINT ["python", "trainer.py"]