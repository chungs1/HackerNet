from flask import Flask
from config import basedir
import time
import threading
import os

SCAN_WAIT_TIME=300

SCANNER_ACTIVE = True

app = Flask(__name__)
app.config.from_object('config')

from app import views, scanner


def scanner_thread():
    while SCANNER_ACTIVE:
        scanner.rescan()
        time.sleep(SCAN_WAIT_TIME)

thread = threading.Thread(target = scanner_thread)
thread.start()

