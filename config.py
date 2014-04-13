import os

CSRF_ENABLED = True
SECRET_KEY = 'some-random-secret-key'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

basedir = os.path.abspath(os.path.dirname(__file__))

