from flask import Flask
from config import basedir
import time
import threading
import os
from werkzeug.contrib.cache import MemcachedCache
from flask.ext.socketio import SocketIO

SCAN_WAIT_TIME=300

SCANNER_ACTIVE = True

app = Flask(__name__)
app.config.from_object('config')
app.config['SECRET_KEY'] = 'idkwhyweneedthisbutitseemsimportant'
socketio = SocketIO(app)
cache = MemcachedCache()

#connection = Connection(app.config['mongodb_host'],app.config['mongodb_port'])

from app import views, scanner


def scanner_thread():
    while SCANNER_ACTIVE:
        scanner.rescan()
        time.sleep(SCAN_WAIT_TIME)

#thread = threading.Thread(target = scanner_thread)
#thread.start()


