import os

basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask 
from mongodb import Connection 

mongodb_host = 'localhost'
mongodb_port = 27017 

connection = Connection(app.config['mongodb_host'],app.config['mongodb_port']) 