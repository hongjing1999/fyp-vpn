FROM ubuntu:20.04

MAINTAINER Hong Jing "hongjing1999@gmail.com"

RUN apt-get -y update && \
    apt-get -y install python3-pip python3.8-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "server.py" ]