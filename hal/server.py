from flask import Flask
from flask import make_response
import threading
from .state import *
from flask import request
import pygame

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
        delay = request.json['delay'] if 'delay' in request.json else 0
        only_write = request.json['only_write'] if 'only_write' in request.json else False
        if not only_write:
            voice.say(text, delay=delay, only_write=only_write)
        state.writer.start(text, pygame.time.get_ticks(), delay=delay * 1000)
        return make_response()


threading.Thread(target=app.run, kwargs=dict(host='0.0.0.0', port=5000)).start()