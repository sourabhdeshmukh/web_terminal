FROM ubuntu:latest
MAINTAINER Sourabh Deshmukh "sourabh.deshmukh.988@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y python3-pip
RUN apt-get -q -y install sudo openssh-server
RUN service ssh start
EXPOSE 22
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["websocket_terminal.py"]
