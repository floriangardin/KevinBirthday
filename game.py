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

## LOAD ASSETS

imgs_gilles = [pygame.image.load(image) for image in glob.glob("./assets/gilles/*gif")]
gilles_size_x, gilles_size_y = imgs_gilles[0].get_size()
music_gilles = pygame.mixer_music.load('./assets/music/main_music.ogg')
white_noise = pygame.mixer_music.load('./assets/music/white_noise.ogg')
clock = pygame.time.Clock()


def print_gilles_images(screen, x, y, time):
    screen.blit(imgs_gilles[int(time//100) % len(imgs_gilles)], (x, y))

def print_white_noise(screen):
    import random
    # Draw random RECT white or black
    sizex = 5
    sizey = 5
    for i in range(SIZEX//sizex):
        for j in range(SIZEY//sizey):
            if random.random() > 0.5:
                color = (0, 0, 0)
            else:
                color = (255, 255, 255)
            pygame.draw.rect(screen, color, (i*sizex, j*sizey, sizex, sizey))

# GAME LOOP

def main_loop():
    if state.state == STATE_WHITE_NOISE:
        if state.start_time_whitenoise is None:
            state.start_time_whitenoise = pygame.time.get_ticks()
            pygame.mixer_music.stop()
            pygame.mixer_music.load('./assets/music/white_noise.ogg')
            pygame.mixer_music.play(loops=1)

        print_white_noise(screen)

        if (time - state.start_time_whitenoise) > WHITE_NOISE_DURATION:
            state.set_state(STATE_MAIN)
            pygame.mixer_music.stop()
            pygame.mixer_music.load('./assets/music/main_music.ogg')
            pygame.mixer_music.play(loops=-1)
            voice.say("Bonjour Florian ... prêt à me défier ? hahaha ! ... Je suis invincible")

    elif state.state == STATE_MAIN:
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, SIZEX, SIZEY))
        print_gilles_images(screen, (SIZEX - gilles_size_x) / 2, (SIZEY - gilles_size_y) / 2, time)

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
