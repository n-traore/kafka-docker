FROM python:3.6

WORKDIR /usr/app

ADD ./requirements.txt ./
ARG CASS_DRIVER_NO_CYTHON=1
RUN pip3 install -r requirements.txt
ADD ./ ./

CMD ["python", "consumer_app.py"]
