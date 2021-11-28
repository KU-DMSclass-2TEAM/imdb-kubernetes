FROM tensorflow/tensorflow:1.13.1 
LABEL email="kkp6249@gmail.com"
LABEL version = "1.0.0"
LABEL description = "A first docker image (server)"
RUN pip install flask flask_dropzone && \
  mkdir /home/uploads
ADD server.py /home/
ADD templates /home/templates 
WORKDIR /home/uploads 
ENTRYPOINT ["python", "/home/server.py"]