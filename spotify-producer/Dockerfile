FROM python:3.6

WORKDIR /usr/app

ADD ./requirements.txt ./
RUN pip3 install -r requirements.txt
ADD ./ ./

CMD ["python", "producer_app.py"]
