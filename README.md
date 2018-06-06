## web_terminal
Clone your local terminal on the browser.

### Introduction
With this **web_terminal** you can clone your local terminal of the machine to any browser using a single script. The commands which can be run on the local terminal are also able to run on the _web_terminal_, no extra permissions are required. Further it can be used for any web application project or for creating online labs. 

### Dependencies
You must have following dependencies installed on your system, if not install the following dependencies.  
```
apt-get install -y python-pip python-dev build-essential  
apt-get install -y python3-pip
```
### Quickstart Guide
```
git clone https://github.com/sourabhdeshmukh/web_terminal  
cd web_terminal/server-python3
pip3 install -r requirements.txt
service ssh start
python3 websocket_terminal.py
```
### Navigate to Browser  
Search the following in your browser search field.  
```
http://localhost:5002
```
You will be presented your local terminal in your browser window.

### Credits
Thanks to Tamás Hegedűs for the websocket_terminal project. Which helped me to build this project.  
Greenlet and wsgi implementation: eventlet  
Python ssh client: paramiko  
Browser side terminal: xterm.js
