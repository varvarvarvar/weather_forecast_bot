# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /

ENV FLASK_APP=wsgi.py
ENV FLASK_RUN_HOST=0.0.0.0

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip3 install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

EXPOSE 5000

# command to run on container start
CMD [ "flask", "run" ]