from .voice import Voice
import math
import glob
import pygame
pygame.init()
pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.

start_time = pygame.time.get_ticks()

sounds = {
    'white_noise': pygame.mixer.Sound('./assets/music/white_noise.ogg')
}
musics = {
    'noise': './assets/music/white_noise',
    'main': './assets/music/main_music.ogg'
}

FULLSCREEN = False
if FULLSCREEN:
    infoObject = pygame.display.Info()
    SIZEX = infoObject.current_w
    SIZEY = infoObject.current_h
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    SIZEX = 800
    SIZEY = 800
    screen = pygame.display.set_mode((SIZEX, SIZEY))

WHITE_NOISE_DURATION = 1000
STATE_WAIT_TO_START = 'WAIT_TO_START'
STATE_WHITE_NOISE = 'WHITE_NOISE'
STATE_MAIN = 'MAIN'
imgs_gilles = [pygame.image.load(image) for image in glob.glob("./assets/hal/*gif")]
imgs_gilles = [pygame.transform.scale(picture, (picture.get_width() * SIZEY//800, picture.get_height() * SIZEY//800)) for picture in imgs_gilles]

gilles_size_x, gilles_size_y = imgs_gilles[0].get_size()
music_gilles = pygame.mixer_music.load('./assets/music/main_music.ogg')
white_noise = pygame.mixer_music.load('./assets/music/white_noise.ogg')
clock = pygame.time.Clock()

myfont = pygame.font.SysFont('Lucida console', 25 * SIZEX // 800)
white = (255, 255, 255)




class WriterTemp:

    def __init__(self, x, y, font, color,  delay=0, frequency=1500):
        self.text = ''
        self.delay = delay
        self.current_text = ''
        self.start_time = 0
        self.font = font
        self.x = x
        self.y = y
        self.active = False
        self.frequency = frequency
        self.color = color


    def update(self, screen, ticks):
        if self.active:
            nb_char = max(0, (ticks - self.start_time - self.delay) // self.frequency)
            # if (ticks - self.start_time - self.delay) // self.frequency > len(self.text) + 10:
            #     self.clear()
            self.current_text = self.text[0: nb_char]

            # ADD LINE RETURN
            max_size = 45
            step = SIZEX // 30
            import numpy as np
            texts_temp = self.current_text.split(' ')
            texts = []
            for text in texts_temp:
                if len(texts) == 0:
                    texts.append(text)
                elif len(texts[-1]) + len(text) > max_size:
                    texts.append(text)
                else:
                    texts[-1] = texts[-1] + ' ' + text

            for idx, text in enumerate(texts):
                textsurface = self.font.render(text, True, self.color)
                text_width = textsurface.get_width()
                screen.blit(textsurface, (SIZEX//2 - text_width//2, self.y + step * idx))

    def clear(self):
        self.active = False
        self.text = ''

    def start(self, text, start_time, delay):
        self.clear()
        self.text = text
        self.current_text = ''
        self.start_time = start_time + delay
        self.active = True


def print_gilles_images(screen, x, y, time):
    screen.blit(imgs_gilles[int(time//100) % len(imgs_gilles)], (x, y))

class State:

    def __init__(self, screen):
        self.state = STATE_WAIT_TO_START
        self.start_time_whitenoise = None
        self.writer = WriterTemp(SIZEX // 6, 3 * SIZEY // 4, myfont, white, delay=0, frequency=75)
        self.screen = screen


    def set_state(self, state):
        print('Change state from', self.state, 'to', state)
        self.state = state
        if state == STATE_WHITE_NOISE:
            self.state = STATE_WHITE_NOISE
            self.start_time_whitenoise = None

        if state == STATE_MAIN:
            self.state = STATE_MAIN

    def update(self):
        self.writer.update(self.screen, pygame.time.get_ticks())

voice = Voice()
state = State(screen)