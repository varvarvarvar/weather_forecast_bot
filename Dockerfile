FROM python:3.8

WORKDIR /code

ADD src /code/src
COPY requirements.txt /code
COPY main.py /code
COPY .env /code

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["main.py"]
