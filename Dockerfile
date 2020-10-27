FROM python:3.8

WORKDIR /code

ADD src /code/src
COPY requirements.txt /code
COPY wsgi.py /code
COPY .env /code

RUN pip3 install -r requirements.txt

ENV FLASK_APP=wsgi.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD [ "flask", "run" ]
