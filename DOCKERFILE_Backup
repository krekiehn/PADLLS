FROM sharedcloud/tensorflow-gpu-python36
#FROM python:3.6
RUN cd /
COPY src/ /root/

WORKDIR /root/

RUN pip3 install pydicom==2.0.0
RUN pip3 install numpy
RUN pip3 install matplotlib
RUN pip3 install scikit-image
RUN pip3 install SimpleITK
RUN pip3 install nibabel==3.1.1
RUN pip3 install NiftyNet==0.6.0
#RUN pip3 install tensorflow==1.9.0
RUN pip3 install natsort

RUN apt-get update
RUN apt-get install wget
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python2.7 get-pip.py

RUN pip2.7 install virtualenv
RUN virtualenv venv
RUN . ./venv/bin/activate && pip2.7 install -r requirements.txt && pip2.7 install tensorflow-gpu==1.10.0
