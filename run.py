#!venv/bin/python
from app import app, socketio
#app.run(port=1337, host="0.0.0.0", debug = True)
socketio.run(app, host='0.0.0.0', port=1337)
