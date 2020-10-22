from hal.state import *
import math
from hal.server import app

"""
State and params
"""
exception = False

## LOAD ASSETS

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

    elif state.state == STATE_MAIN:
        color = 0.0 * math.sin(time / 2000) ** 2
        pygame.draw.rect(screen, (10 * color, 0, 0), (0, 0, SIZEX, SIZEY))
        a = 30 * math.sin(time/3000)
        b = 30 * math.cos(time/3000)
        print_gilles_images(screen, (SIZEX - gilles_size_x + a) / 2, (SIZEY - gilles_size_y + b) / 4, time)

    state.update()
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
