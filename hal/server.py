from flask import Flask
from flask import make_response
import threading
from .state import *

data = 'foo'
app = Flask(__name__)

@app.route("/start")
def main():
    state.set_state(STATE_WHITE_NOISE)
    return make_response()



threading.Thread(target=app.run, kwargs=dict(host='0.0.0.0', port=5000)).start()