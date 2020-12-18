from flask import Flask
from flask import make_response
import threading
from .state import *
from flask import request
import pygame

data = 'foo'
app = Flask(__name__)

@app.route("/start")
def main_start():
    state.set_state(STATE_WHITE_NOISE)
    state.writer.clear()
    return make_response()


@app.route("/restart")
def main_restart():
    state.set_state(STATE_WAIT_TO_START)
    state.writer.clear()
    return make_response()

@app.route("/stop")
def main_stop():
    state.set_state(STATE_WHITE_NOISE)
    state.writer.clear()
    return make_response()

@app.route("/say", methods = ['POST'])
def main_say():
    state.state = STATE_MAIN
    if request.method == 'POST':
        text = request.json['text']
        delay = request.json['delay'] if 'delay' in request.json else 0
        only_write = request.json['only_write'] if 'only_write' in request.json else False
        if not only_write:
            voice.say(text, delay=delay, only_write=only_write)
        state.writer.start(text, pygame.time.get_ticks(), delay=delay * 1000)
        return make_response()


@app.route("/music", methods = ['POST'])
def main_music():
    if request.method == 'POST':
        music = request.json['music']
        volume = request.json['volume'] if 'volume' in request.json else 1.0
        pygame.mixer_music.stop()
        pygame.mixer_music.load(music)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer_music.play(loops=1)
        return make_response()


@app.route("/sound", methods=['POST'])
def main_sound():
    if request.method == 'POST':
        sound = request.json['sound']
        if sound in sounds.keys():
            sound = sounds[sound]
            sound.play()
        return make_response()

threading.Thread(target=app.run, kwargs=dict(host='0.0.0.0', port=5000)).start()