import requests

import flask

import pygame
import math
from client import  pygame_textinput
import pygame.freetype

pygame.init()
import glob
from client.states import *
from hal.server import app

"""
State and params
"""
exception = False
FULLSCREEN = False

start_time = pygame.time.get_ticks()

pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
myfont = pygame.font.SysFont('Lucida console', 35)
textinput = pygame_textinput.TextInput(font_family='Lucida console', font_size=35)
textinput.set_cursor_color((100, 100, 100))
textinput.set_text_color((100, 100, 100))
if FULLSCREEN:
    infoObject = pygame.display.Info()
    SIZEX = infoObject.current_w
    SIZEY = infoObject.current_h
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    SIZEX = 800
    SIZEY = 800
    screen = pygame.display.set_mode((SIZEX, SIZEY))
clock = pygame.time.Clock()

# Simulate call to API
host = 'http://localhost'
port = 5000

import threading
def make_get_request_(route):
    host = 'http://localhost'
    port = 5000
    URL = host + ':' + str(port) + '/' + route
    requests.get(url=URL)

def make_get_request(route):
    threading.Thread(target=make_get_request_, args=(route,)).start()


def make_post_request_(route, **kwargs):
    URL = host + ':' + str(port) + '/' + route
    requests.post(url=URL, data=kwargs)

def make_post_request(route, **kwargs):
    threading.Thread(target=make_post_request_, args=(route,), kwargs=kwargs).start()




state = STATE_LOGIN_USER
text = ""

class State:
    def __init__(self):
        self.state = STATE_LOGIN_USER
        self.data = {}


    def set_state(self, state, **kwargs):
        self.state = state
        self.data.update(kwargs)

state = State()

def display_text():
    if state.state == STATE_LOGIN_USER:
        textsurface = myfont.render('Username :', True, (255, 255, 255))
        screen.blit(textsurface, (SIZEX//10, SIZEY//3))
    if state.state == STATE_LOGIN_PASSWORD:
        textsurface = myfont.render('Password :', True, (255, 255, 255))
        screen.blit(textsurface, (SIZEX//10, SIZEY//3))
    pass

def send_text(text):

    if state.state == STATE_LOGIN_USER:
        state.set_state(STATE_LOGIN_PASSWORD, user=text)
    elif state.state == STATE_LOGIN_PASSWORD:
        # SEND LOGIN PASSWORD TO API
        success = True
        if not success:
            state.set_state(STATE_LOGIN_USER)
        else:
            make_get_request('start')
            state.set_state(STATE_INTRO)

def display_console():
    global text

    time = (pygame.time.get_ticks() / 3000.0) % 1
    time = math.sin(time * 2 * math.pi) ** 2
    textsurface = myfont.render('>', True, (255 * time, 255 * time, 255 * time))
    screen.blit(textsurface, (SIZEX//10, SIZEY // 2))


    text = textinput.get_text()

    if textinput.update(events):
        send_text(text)
        textinput.clear_text()
        text = ""

    # Blit its surface onto the screen
    remind_text = textinput.get_text()
    text_to_print = remind_text
    if state.state == STATE_LOGIN_PASSWORD:
        textinput.password = True
    if state.state != STATE_LOGIN_PASSWORD:
        textinput.password = False

    screen.blit(textinput.get_surface(), (SIZEX // 7, SIZEY // 2))


def main_loop(events):
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, SIZEX, SIZEY))

    display_text()
    display_console()

    if state == STATE_LOGIN_USER:
        pass



    pygame.display.flip()
    clock.tick(60)


while True:
    time = pygame.time.get_ticks() - start_time
    events = pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    if exception:
        try:  # Catch logic errors (because asynchronous is weird)
            main_loop(events)
        except Exception as e:
            print(e)
    else:
        main_loop(events)


