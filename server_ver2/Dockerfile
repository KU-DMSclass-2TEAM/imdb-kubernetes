FROM tensorflow/tensorflow
LABEL email="kkp6249@gmail.com"
RUN pip install flask flask_dropzone && \
  mkdir /home/uploads
ADD server_ver2.py /home/
ADD templates /home/templates
WORKDIR /home/uploads
ENTRYPOINT ["python", "/home/server_ver2.py"]