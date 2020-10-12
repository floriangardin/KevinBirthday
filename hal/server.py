from flask import Flask
from flask import make_response
import threading
from .state import *
from flask import request

data = 'foo'
app = Flask(__name__)

@app.route("/start")
def main():
    state.set_state(STATE_WHITE_NOISE)
    return make_response()

@app.route("/say", methods = ['POST'])
def main_say():
    if request.method == 'POST':
        text = request.json['text']
        voice.say(text)
        return make_response()



threading.Thread(target=app.run, kwargs=dict(host='0.0.0.0', port=5000)).start()