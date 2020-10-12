import requests

import flask

import pygame

pygame.init()
import glob
from hal.state import *
from hal.server import app

"""
State and params
"""
exception = False

start_time = pygame.time.get_ticks()
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
host = '0.0.0.0'
port = 5000


def make_get_request(route):
    URL = host + ':' + str(port) + '/' + route
    requests.get(url=URL)


def make_post_request(route, **kwargs):
    URL = host + ':' + str(port) + '/' + route
    requests.post(url=URL, data=kwargs)


def main_loop():

    pygame.display.flip()
    clock.tick(60)


while True:
    time = pygame.time.get_ticks() - start_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    if exception:
        try:  # Catch logic errors (because asynchronous is weird)
            main_loop()
        except Exception as e:
            print(e)
    else:
        main_loop()
