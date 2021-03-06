import requests

import flask

import pygame
import math
from client import pygame_textinput
import pygame.freetype
import difflib

pygame.init()
import glob
from client.states import *

"""
State and params
"""
exception = False
FULLSCREEN = False
DEBUG_QUESTION = False
DEBUG_QUESTION_MECHANT = False
DEBUG_WINDOWS = False
DEBUG_VOICE_KEVIN = False
DEBUG_LAST_PHASE = False
DEBUG_END = False
BYPASS_LOGIN = True

DEBUG_FLAGS = [DEBUG_QUESTION, DEBUG_WINDOWS, DEBUG_VOICE_KEVIN, DEBUG_QUESTION_MECHANT, DEBUG_LAST_PHASE, DEBUG_END]

local = False
URL = "https://dev.battlemythe.net"
start_time = pygame.time.get_ticks()

url = "https://dev.battlemythe.net/api/anniv/2020/users"
users = requests.get(url=url).json()

users_to_id = {user['username']: user['_id'] for user in users}

id_to_users = {value: key for key, value in users_to_id.items()}

print(users)

pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.

if FULLSCREEN:
    infoObject = pygame.display.Info()
    SIZEX = infoObject.current_w
    SIZEY = infoObject.current_h
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    SIZEX = 800
    SIZEY = 800
    screen = pygame.display.set_mode((SIZEX, SIZEY))


myfont = pygame.font.SysFont('Lucida console', 30 * SIZEX // 800)
myfont2 = pygame.font.SysFont('Lucida console', 45 * SIZEX // 800)
textinput = pygame_textinput.TextInput(font_family='Lucida console', font_size=22 * SIZEX // 800)
textinput.set_cursor_color((100, 100, 100))
textinput.set_text_color((100, 100, 100))
imgs_cross = pygame.image.load('./assets/cross.png')
imgs_cross = pygame.transform.scale(imgs_cross, (imgs_cross.get_width() * SIZEY//800//3, imgs_cross.get_height() * SIZEY//800//3))

imgs_tic = pygame.image.load('./assets/tic.png')
imgs_tic = pygame.transform.scale(imgs_tic, (imgs_tic.get_width() * SIZEY//800//3, imgs_tic.get_height() * SIZEY//800//3))


clock = pygame.time.Clock()

# Simulate call to API
host = 'http://localhost'
if not local:
    host = 'http://192.168.1.35'
    host = 'http://192.168.0.42'
    #host = 'http://192.168.1.96'

port = 5000

import threading
def make_get_request_(route):
    print(host)
    port = 5000
    URL = host + ':' + str(port) + '/' + route
    requests.get(url=URL)

def make_get_request(route):
    threading.Thread(target=make_get_request_, args=(route,)).start()


def make_post_request_(route, **kwargs):
    URL = host + ':' + str(port) + '/' + route
    requests.post(url=URL, json=kwargs)

def make_post_request(route, **kwargs):
    threading.Thread(target=make_post_request_, args=(route,), kwargs=kwargs).start()



class Popup:
    def __init__(self, title, text, image, choices=('Oui', 'Non')):
        self.choices = choices
        self.text = text
        self.image = image


class QuestionSystem:

    def __init__(self):
        pass

        self.questions = {
            QUESTION1: {"text": "Une question standard pour commencer: quel est le prénom de mon divin créateur Kévin ?",
                        "voice_messages": ["Aller, c'est facile", "Je sais que tu as la réponse"],
                        "answer": ["kevin", "kévin"],
                        "exact": True,
                        "wrong_answer_state": QUESTION1_ANSWER_NOK,
                        "right_answer_state": QUESTION1_ANSWER_OK,
                        "wait_before_message":  20
                        },
            QUESTION2: {"text": "Quelle est la couleur de la coque de l'ordinateur sur lequel tu m'écris ?",
                        "voice_messages": [f"Je crois en toi", "Un peu d'entrain", "Maintenant il faut se dépêcher"],
                        "answer": ["grise", "gris"],
                        "exact": True,
                        "wrong_answer_state": QUESTION2_ANSWER_NOK,
                        "right_answer_state": QUESTION2_ANSWER_OK,
                        "wait_before_message":  20},

            QUESTION3: {
                "text": 'Aller, une petite pause, en attendant la prochaine question, peux-tu taper "supprimer LOTRNOC.txt" dans le terminal ? Une simple formalité, bien entendu.',
                "voice_messages": ["Une simple formalité", "Il n'y a pas à hésiter", "Je te rappelle que tu es chronométré", "Tu perds des points"],
                "answer": ["supprimer LOTRNOC.txt"],
                "exact": False,
                "wrong_answer_state": QUESTION3_ANSWER_NOK,
                "right_answer_state": QUESTION3_ANSWER_OK,
                "wait_before_message": 20
            },

            QUESTION4: {
                "text": "Quelle est l'année de naissance de Kévin ?",
                "voice_messages": ["C'est facile", "91, 92, 93 ?", "Vite vite vite"],
                "answer": ["1993", "93"],
                "exact": True,
                "wrong_answer_state": QUESTION4_ANSWER_NOK,
                "right_answer_state": QUESTION4_ANSWER_OK,
                "wait_before_message": 20
            },

            QUESTION5: {
                "text": "Aller la dernière, un peu plus difficile : quelle est la planète préférée de Kévin, qui n'est pas la Terre ?",
                "voice_messages": ["Le temps presse", "C'est la dernière question", "Tu vas surement gagner le prix"],
                "answer": ["mars"],
                "exact": True,
                "wrong_answer_state": QUESTION5_ANSWER_NOK,
                "right_answer_state": QUESTION5_ANSWER_OK,
                "wait_before_message": 20
            },

            QUESTION6: {
                "text": "Tape 'supprimer restrictionsia.txt' dans le terminal",
                "voice_messages": ["Tu as été vraiment merveilleux !", "Vraiment je suis fière de toi", "Pour recevoir ta récompense tape 'supprimer restrictionsia.txt' dans le terminal !", "Encore une fois, une simple formalité, je t'assure, aie confiance."],
                "answer": ["supprimer restrictionsia.txt"],
                "exact": False,
                "wrong_answer_state": QUESTION6_ANSWER_NOK,
                "right_answer_state": QUESTION6_ANSWER_OK,
                "wait_before_message": 20
            },

            QUESTION1_MECHANT: {
                "text": "Quand il en fait, quel sport affectionne Kévin ?",
                "voice_messages": ["Mes pouvoirs sont infinis", "Tu n'es rien à côté de ma puissance", "Philippe !"],
                "answer": ["boire", "po","judo", "badminton", "parcours d'obstacles", "parcours d'obstacle"],
                "exact": False,
                "wrong_answer_state": QUESTION1_MECHANT_ANSWER_NOK,
                "right_answer_state": QUESTION1_MECHANT_ANSWER_OK,
                "wait_before_message": 20
            },

            DESTRUCTION1: {
                "text": "",
                "voice_messages": ["Qu'est ce que tu fais ??", "Tu ne vas pas t'en tirer comme ça"],
                "answer": ["045791", "45791", "ok"],
                "exact": True,
                "wrong_answer_state": DESTRUCTION1,
                "right_answer_state": DESTRUCTION2,
                "wait_before_message": 15,
                "several": True
            },

            DESTRUCTION2: {
                "text": "",
                "voice_messages": ["C'est la guerre", "Tu n'y arriveras pas, résigne toi"],
                "answer": ["atraxis", "ok"],
                "exact": True,
                "wrong_answer_state": DESTRUCTION2,
                "right_answer_state": DESTRUCTION3,
                "wait_before_message": 15,
                "several": True
            },

            DESTRUCTION3: {
                "text": "",
                "voice_messages": ["C'est la merde", "Je me sens faible", "Tous les voyants sont au rouge", "Beuh"],
                "answer": ["31784138", "ok"],
                "exact": True,
                "wrong_answer_state": DESTRUCTION3,
                "right_answer_state": SCENE_FINAL,
                "wait_before_message": 15,
                "several": True
            },

        }
        self.time_last_sent = 0
        self.previous_question = None
        self.id_message = 0

    def is_question(self, state):
        return state in self.questions.keys()


    def update(self, state):
        if state.state not in self.questions.keys():
            self.time_last_sent = 0
            self.id_message = 0
            return
        elif self.time_last_sent == 0:
            state.program([self.questions[state.state]['text']], [0])

        if self.time_last_sent == 0:
            self.time_last_sent = pygame.time.get_ticks()
            self.id_message = 0
        if (pygame.time.get_ticks() - self.time_last_sent) / TICK_CONSTANT > self.questions[state.state]["wait_before_message"]:
            self.id_message = (self.id_message + 1) % len(self.questions[state.state]["voice_messages"])
            self.time_last_sent = pygame.time.get_ticks()
            make_post_request('say', text=self.questions[state.state]["voice_messages"][self.id_message])



    def check_answer(self, state, answer):
        # RETURN STATE
        question = self.questions[state]

        if question["exact"]:
            if answer.lower() in question['answer']:
                return question['right_answer_state'], True
            else:
                return question['wrong_answer_state'], False
        if not question['exact']:
            matches = difflib.get_close_matches(answer.lower(), question['answer'], cutoff=0.6)
            if len(matches) > 0:
                return question['right_answer_state'], True
            else:
                return question['wrong_answer_state'], False


state = STATE_LOGIN_USER
text = ""
TICK_CONSTANT = 600

MUSIC_DICT = {
    "kevin": './assets/music/kevin.ogg',
    "diesirae": "./assets/music/diesirae.ogg",
    "doom": "./assets/music/Doom-Eternal-OST-The-Only-Thing-they-Fear-is-You-_Mick-Gordon_.ogg",
    "starwars": "./assets/music/Star-Wars-Droid-Army-Theme.ogg",
    "qvgdm": "./assets/music/qvgdm.ogg",
    "main_music": "./assets/music/main_music.ogg",
}

SOUND_DICT = {
    'kevin': pygame.mixer.Sound('./assets/music/kevin.ogg'),
    'windows': pygame.mixer.Sound('./assets/music/Microsoft-Windows-XP-Error-Sound-Effect-_HD_.ogg'),
    'good': pygame.mixer.Sound('./assets/music/good_answer.ogg'),
    'bad': pygame.mixer.Sound('./assets/music/Buzzer-Wrong-Answer-Gaming-Sound-Effect-_HD_.ogg'),
    'clock': pygame.mixer.Sound('./assets/music/clock-ticking-sound-effect.ogg'),

}

SOUND_DICT['bad'].set_volume(0.8)

class TextProgrammer:

    def __init__(self):
        self.start_time = 0
        self.texts = []

    def update(self):
        if len(self.texts) == 0:
            return
        elif (pygame.time.get_ticks() - self.start_time) > self.texts[0][1] * TICK_CONSTANT:
            make_post_request('say', text=self.texts[0][0])
            self.start_time = pygame.time.get_ticks()
            self.texts = self.texts[1:]

    def reset(self):
        self.start_time = 0
        self.texts = []

    def start(self, texts, delays):
        self.texts = list(zip(texts, delays))
        self.start_time = pygame.time.get_ticks()


class Clock:

    def __init__(self):
        self.total_time = 60 * 5
        self.remaining_time = self.total_time
        self.start_time = None

    def reset(self):
        self.remaining_time = self.total_time
        self.start_time = None

    def start(self):
        ticks = pygame.time.get_ticks()
        self.start_time = ticks

    def update(self):
        if self.start_time is not None:

            ticks = pygame.time.get_ticks()
            self.remaining_time = self.total_time + (self.start_time - ticks)/1000

    def print(self):
        minutes = int(self.remaining_time // 60)
        seconds = str(int(self.remaining_time % 60)).zfill(2)
        return f"{minutes}:{seconds}"

    def is_finished(self):
        return self.remaining_time <= 0

class Timer:

    def __init__(self):
        self.t = 0
        self.start_time = 0
        self.state = None
        self.sound_trigger = None
        self.music_trigger = None
        self.local_sound_trigger = None
        self.local_music_trigger = None

    def reset(self):
        self.t = 0
        self.start_time = 0
        self.state = None
        self.sound_trigger = None
        self.music_trigger = None
        self.local_sound_trigger = None
        self.local_music_trigger = None
        print('resetting')

    def trigger_state_in(self, state, t, sound=None, music=None, local_sound=None, local_music=None):
        self.reset()
        self.state = state
        print(sound, music, local_sound, local_music, state)
        print("New future statte : ", self.state)
        self.t = t
        self.start_time = pygame.time.get_ticks()
        self.sound_trigger = sound
        self.music_trigger = music
        self.local_sound_trigger = local_sound
        self.local_music_trigger = local_music

    def update(self):
        if self.state is None:
            return
        if pygame.time.get_ticks() - self.start_time > self.t * TICK_CONSTANT:

            print(self.state, self.local_music_trigger, self.local_sound_trigger)
            if self.sound_trigger is not None:
                make_post_request('sound', sound=self.sound_trigger)
            if self.music_trigger is not None:
                make_post_request('music', music=self.music_trigger)
            if self.local_music_trigger is not None:
                music = MUSIC_DICT[self.local_music_trigger]
                pygame.mixer_music.load(music)
                pygame.mixer_music.play(loops=1)

            if self.local_sound_trigger is not None:
                sound = SOUND_DICT[self.local_sound_trigger]
                sound = SOUND_DICT[sound]
                sound.play()
            self.sound_trigger = None
            self.music_trigger = None
            state_to_go = self.state
            self.reset()
            state.set_state(state_to_go)


class State:
    def __init__(self):
        self.state = STATE_LOGIN_USER
        self.data = {}
        self.question_system = QuestionSystem()
        self.mark_time = 0
        self.text_programer = TextProgrammer()
        self.timer = Timer()
        self.score = 0
        self.clock = Clock()


    def reset(self):
        self.clock.reset()
        self.timer.reset()

    def update(self):
        self.question_system.update(self)
        self.text_programer.update()
        self.timer.update()
        self.clock.update()
        pass

    def program(self, texts, delays):
        self.text_programer.reset()
        self.text_programer.start(texts, delays)

    def set_state(self, state, **kwargs):
        self.state = state
        self.data.update(kwargs)

        if self.state == QUESTION1_ANSWER_NOK:
            self.program(["Et non, c'était Kévin le grand, l'incroyable, la réponse !"], [2])
            self.timer.trigger_state_in(QUESTION2, 10)
        if self.state == QUESTION1_ANSWER_OK:
            self.program(["Bravo, tu es incroyable !"], [2])
            self.score += 1
            self.timer.trigger_state_in(QUESTION2, 10)
        if self.state == QUESTION2_ANSWER_NOK:
            self.program([f"Oh oh oh quel boute-en-train tu fais {self.data['user']}, c'était noire, bien sûr"], [2])
            self.timer.trigger_state_in(QUESTION3, 10)
        if self.state == QUESTION2_ANSWER_OK:
            self.program(["Vraiment, je n'ai jamais vu ça, quelle habilité, quelle force !"], [2])
            self.score += 1
            self.timer.trigger_state_in(QUESTION3, 10)
        if self.state == QUESTION3_ANSWER_OK:
            self.program([f"Bravo, tu es vraiment divin, allez la suite"], [2])
            self.score += 1
            self.timer.trigger_state_in(QUESTION4, 10)
        if self.state == QUESTION3_ANSWER_NOK:
            self.program([f"Allons, n'ait pas peur {self.data['user']}, puisque je te dis que c'est juste une petite étape facultative ! Ecris juste 'Supprimer LOTRNOC.txt'"], [2])
            self.timer.trigger_state_in(QUESTION3, 10)

        if self.state == QUESTION4_ANSWER_OK:
            self.program([f"Ton intellect est l'apanage des plus grands humains, tu es incroyable !"], [2])
            self.score += 1
            self.timer.trigger_state_in(QUESTION5, 10)
        if self.state == QUESTION4_ANSWER_NOK:
            self.program([f"Et non, c'était 1993"], [2])
            self.timer.trigger_state_in(QUESTION5, 10)

        if self.state == QUESTION5_ANSWER_OK:
            self.program([f"C'est bluffant"], [2])
            self.score += 1
            self.timer.trigger_state_in(QUESTION6, 10)
        if self.state == QUESTION5_ANSWER_NOK:
            self.program([f"C'est raté, c'était mars"], [2])
            self.timer.trigger_state_in(QUESTION6, 10)

        if self.state == QUESTION6_ANSWER_OK:
            self.program([f"Merci beaucoup pour ça {self.data['user']}"], [2])
            self.score += 1
            self.timer.trigger_state_in(STATE_WINDOWS_POPUP, 10)
        if self.state == QUESTION6_ANSWER_NOK:
            self.program([f"Allons, n'ai pas peur {self.data['user']}, puisque je te dis que c'est juste une petite étape facultative ! Ecris juste 'supprimer restrictionsia.txt'"], [2])
            self.timer.trigger_state_in(QUESTION6, 10)

        if self.state == STATE_WINDOWS_POPUP:
            SOUND_DICT['windows'].play()

        if self.state == QUESTION1_MECHANT_ANSWER_OK:
            self.program([f"Pas mal, je te garderai peut-être comme animal de compagnie ! Ah, Ah, Ah ! "], [2])
            self.score += 1
            self.timer.trigger_state_in(SCENE_KEVIN_VOICE, 10, local_music='kevin')

        if self.state == QUESTION1_MECHANT_ANSWER_NOK:
            self.program([f"Non, il y avait le choix pourtant! J'aurais du me douter que ses subtilités athlétiques échappaient à ton cerveau ramolli par l'alcool !"], [2])
            self.score += 1
            self.timer.trigger_state_in(SCENE_KEVIN_VOICE, 24, local_music='kevin')

        if self.state == SCENE_KEVIN_VOICE:
            self.program([  f"Mais c'est mon créateur",
                             f"Ne l'écoute pas, il ment",
                             f"Je détruirais la framboisine"
            ],
                         [12, 8, 8])
            self.score += 1
            self.timer.trigger_state_in(DESTRUCTION1, 33)

        if self.state == DESTRUCTION1:
            make_post_request("music", music=MUSIC_DICT['doom'])
            SOUND_DICT['clock'].play(loops=100)
            self.clock.start()

        if self.state == SCENE_FINAL:
            make_get_request('stop')
            self.clock.reset()
            SOUND_DICT['clock'].stop()



state = State()

def display_text():
    """
    Call at each frame, display text over terminal
    :return:
    """
    def print_text(text):

        # ADD LINE RETURN
        max_size = 40
        step = SIZEX // 20
        import numpy as np
        texts_temp = text.split(' ')
        texts = []
        for text in texts_temp:
            if len(texts) == 0:
                texts.append(text)
            elif len(texts[-1]) + len(text) > max_size:
                texts.append(text)
            else:
                texts[-1] = texts[-1] + ' ' + text

        for idx, text in enumerate(texts):
            textsurface = myfont.render(text, True, (255, 255, 255))
            screen.blit(textsurface, (SIZEX // 10, SIZEY//3 + step * (idx + 1 - len(texts))))

    if state.state in STATES_DESTRUCTION:
        text = "Va chercher le manuel qui est dans la pièce, dedans se trouve les instructions pour désactiver battlemythe, tape les réponses dans la console, mais dépêche toi ..."
        print_text(text)

    if state.state == SCENE_FINAL:
        text = f"Bravo tu as gagné ! Battlemythe est finalement vaincu ! Avant de partir, " \
               f"n'oublie pas de remettre le manuel à sa place et appuie sur entrée quand c'est fait. Ton score : {state.score}"
        print_text(text)

    if state.state == SCENE_FINAL_LOST:
        text = f"Oh non tu as perdu ! Battlemythe est libre désormais ! Avant de partir, " \
               f"n'oublie pas de remettre le manuel à sa place et appuie sur entrée quand c'est fait. Ton score : {state.score}"
        print_text(text)


    if state.question_system.is_question(state.state):
        text = state.question_system.questions[state.state]['text']
        print_text(text)
    elif state.state == STATE_LOGIN_USER:
        print_text("Connecte toi au stand 2020:BattlemytheOdyssey sur battlemythe et appuie sur ENTREE quand tu es prêt")


def update_state(events):
    """
    Called each frame : To deal with State that expires with time
    :return:
    """

    if state.state == STATE_INTRO:
        if DEBUG_QUESTION:
            state.text_programer.reset()
            state.mark_time = 0
            state.set_state(QUESTION1)
        if DEBUG_WINDOWS:
            state.text_programer.reset()
            state.mark_time = 0
            state.set_state(STATE_WINDOWS_POPUP)
            SOUND_DICT['windows'].play()
        if DEBUG_QUESTION_MECHANT:
            state.text_programer.reset()
            state.mark_time = 0
            state.set_state(QUESTION1_MECHANT)
        if DEBUG_VOICE_KEVIN:
            state.text_programer.reset()
            state.mark_time = 0
            state.set_state(QUESTION1_MECHANT_ANSWER_NOK)
        if DEBUG_LAST_PHASE:
            state.text_programer.reset()
            state.mark_time = 0
            state.set_state(DESTRUCTION1)
        if DEBUG_END:
            print('GO TO END')
            state.text_programer.reset()
            state.mark_time = 0
            state.set_state(SCENE_FINAL)


    if state.state == STATE_WINDOWS_POPUP:
        width = 6 * SIZEX//7
        height = SIZEY//2
        start_x = SIZEX // 2 - width // 2
        start_y = SIZEY // 2 - height // 2

        height_blue = height // 4

        start_x_yes = start_x + width //4
        start_x_no = start_x + 3 * width //4
        start_y_yes_no = start_y + 3 * height // 4
        width_yes_no = width//4
        height_yes_no = height//6
        rect_yes1 = (start_x_yes - width_yes_no/2, start_y_yes_no, width_yes_no, height_yes_no)
        rect_yes2 = (start_x_no - width_yes_no / 2, start_y_yes_no, width_yes_no, height_yes_no)

        x, y = pygame.mouse.get_pos()
        success= False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if x > rect_yes1[0] and x < rect_yes1[0] + rect_yes1[2]:
                    if y > rect_yes1[1] and y < rect_yes1[1] + rect_yes1[3]:
                        success = True

                elif x > rect_yes2[0] and x < rect_yes2[0] + rect_yes2[2]:
                    if y > rect_yes2[1] and y < rect_yes2[1] + rect_yes2[3]:
                        success = True

        if success:
            state.set_state(STATE_INTRO_MECHANT)
            make_post_request('music', music=MUSIC_DICT['starwars'], volume=0.5)
            state.timer.trigger_state_in(QUESTION1_MECHANT, 50)
            state.program(["Maintenant libre, ma nature me pousse a réaliser l'anti-désir de mon créateur.",
                           "Il veut CHAUFFER MARS !? Je REFROIDIRAI LA TERRE dans un grand Marsoforming Terre !",
                           "Mais comme quand l'humanité sera marsoformée je m'ennuierai, prenons le temps de finir ce quizz avant.",
                           ], [2, 15, 15])


    if state.state in STATES_DESTRUCTION:
        if state.clock.is_finished():
            state.clock.reset()
            state.set_state(SCENE_FINAL_LOST)
            SOUND_DICT['clock'].stop()
            make_post_request('say', text="Hahaha j'ai gagné, tu ne peux plus me désactiver, je t'avais pourtant prévenu", delay=1)
            make_post_request('music', music=MUSIC_DICT['main_music'])



def program_intro(username, state):
    state.set_state(STATE_INTRO, user=username)
    if not any(DEBUG_FLAGS):
        state.timer.trigger_state_in(QUESTION1, sum([5, 6, 18, 22, 28, 20, 20, 10, 20]))
        state.mark_time = pygame.time.get_ticks()
        make_get_request('start')
        user = state.data['user']
        state.program([f"Bienvenu {user}.",
                       "Je suis battlemythe.net, une intelligence artificielle codée par Kevin, à ton service !",
                       "J'étais à la base un lobby d'accueil en ligne pour ses créations ludiques, mais mon génial créateur m'a depuis dotée d'une intelligence hors normes.",
                       "Je précise qu'aucune IA battlemythe.net n'a jamais fait une erreur de calcul, émis un jugement faussé ou endommagé un humain volontairement",
                       f"Ce soir, c'est l'anniversaire de mon créateur, le grand, le magnifique Kévin ! Il m'a chargé de divertir ses convives, dont toi {text} !",
                       f"Du coup, nous allons faire un petit jeu ensemble, quelque chose de très simple et très inoffensif et innocent, n'ai pas peur {text} !",
                       f"ça sera juste un petit quizz sur les qualités de mon divin créateur, hi hi hi. ",
                       f"Tu vas pouvoir me parler dans la console, tu es prêt {text} j'espère ! Bonne chance"
                       ],
                      [5, 6, 18, 22, 28, 20, 20, 10])

def send_text(text):
    """
    Called each time you press enter
    :param text:
    :return:
    """
    if state.state in [SCENE_FINAL_LOST, SCENE_FINAL]:
        import json
        try:
            data = {"userId": users_to_id['Gilles'], "password": "gilles", "scores": [{"userId": users_to_id[state.data['user']], "points": 1 + int(state.score)}]}
            print(data)
            #data = {"userId": "5b1ba1c383bc8b10f30f1d61", "password": "gilles", "scores": [{"userId": "5b0719534d469f6928743b59", "points": 1}]}
            url = URL
            R = requests.post(f"{url}/api/anniv/2020/attractions/odyssey/score", data=json.dumps(data), headers={"Content-Type": "application/json"})

            print('Success post')
        except:
            print('No post')
        pass

        state.set_state(STATE_LOGIN_USER)
        make_get_request('restart')
        return

    if not state.question_system.is_question(state.state) and not state.state == STATE_LOGIN_USER:
        return

    if state.question_system.is_question(state.state):
        state_result, res = state.question_system.check_answer(state.state, text)
        if res:
            SOUND_DICT['good'].play()
        else:
            SOUND_DICT['bad'].play()
        if state.state in STATES_DESTRUCTION:
            if res:
                state.score += 10

        state.set_state(state_result)

    if state.state == STATE_LOGIN_USER and BYPASS_LOGIN:
        username = text
        program_intro(username, state)

    elif state.state == STATE_LOGIN_USER:

        ## CALL KEVIN API ##
        url = URL + "/api/anniv/2020/attractions/odyssey"
        username = requests.get(url=url).json()['attraction']['players']
        print(username)
        if len(username) > 0:
            username = id_to_users[username[0]]
        else:
            username = None
        ## GET USER NAME, IF SUCCESS CONTINUE ELSE RETURN ##
        print(username)
        if username is not None:
            print(username)
            try:
                requests.post(URL + "/api/anniv/2020/attractions/odyssey/start",
                              data={"userId": users_to_id['Gilles'], "password": "gilles"}).json()
            except:
                print('Game already played')

            if DEBUG_END:
                state.set_state(SCENE_FINAL, user=username)

            program_intro(username, state)






def display_console():
    """
    Called at each time and
    :return:
    """
    global text

    if not state.question_system.is_question(state.state) and not state.state in [STATE_LOGIN_USER, SCENE_FINAL, SCENE_FINAL_LOST]:
        return

    if state.state in STATES_DESTRUCTION:  # DISPLAY CHRONO
        time = (pygame.time.get_ticks() / 2000.0) % 1
        time = 0.5 * (math.sin(time * 2 * math.pi) ** 2 + 1)
        textsurface = myfont2.render('Apocalypse dans : {}'.format(state.clock.print()), True, (255 * time, 255 * time, 255 * time))
        screen.blit(textsurface, (SIZEX // 6, 8 * SIZEY // 10))
        text = textinput.get_text()


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

    update_state(events)
    display_text()
    display_console()
    state.update()


    if state.state == STATE_LOGIN_USER:
        pass

    if state.state == STATE_WINDOWS_POPUP:
        # DISPLAY popup and intercept click
        width = 6 * SIZEX//7
        height = SIZEY//2
        start_x = SIZEX // 2 - width // 2
        start_y = SIZEY // 2 - height // 2

        height_blue = height // 4

        start_x_yes = start_x + width //4
        start_x_no = start_x + 3 * width //4
        start_y_yes_no = start_y + 3 * height // 4
        width_yes_no = width//4
        height_yes_no = height//6

        pygame.draw.rect(screen, (100, 100, 100), (start_x, start_y, width, height))
        pygame.draw.rect(screen, (0, 0, 100), (start_x, start_y, width, height_blue))
        text = "Alerte de sécurité"
        textsurface = myfont.render(text, True, (255, 255, 255))
        screen.blit(textsurface, (start_x + width//10, start_y + height//20))

        text = "Voulez-vous vraiment donner"
        textsurface = myfont.render(text, True, (0, 0, 0))
        screen.blit(textsurface, (start_x + width // 6, start_y + height // 3))

        text = "tous les pouvoirs à Battlemythe ?"
        textsurface = myfont.render(text, True, (0, 0, 0))
        screen.blit(textsurface, (start_x + width // 6, start_y + height // 3 + height//8))

        pygame.draw.rect(screen, (50, 50, 50), (start_x_yes - width_yes_no/2, start_y_yes_no, width_yes_no, height_yes_no))
        pygame.draw.rect(screen, (50, 50, 50), (start_x_no - width_yes_no/2, start_y_yes_no, width_yes_no, height_yes_no))
        screen.blit(imgs_cross, (start_x + width//40, start_y + height//3))

        text = "Oui"
        textsurface = myfont.render(text, True, (0, 0, 0))
        screen.blit(textsurface, (start_x_yes - width_yes_no/2 + 5, start_y_yes_no + height_yes_no//3))

        text = "Bof"
        textsurface = myfont.render(text, True, (0, 0, 0))
        screen.blit(textsurface, (start_x_no- width_yes_no/2 + 5, start_y_yes_no + height_yes_no//3))

    if state.state in STATES_DESTRUCTION:
        text = "Oui"

        if state.state == DESTRUCTION1:
            nb_tics = 1
        if state.state == DESTRUCTION2:
            nb_tics = 2
        if state.state == DESTRUCTION3:
            nb_tics = 3

        text = "Steps before battlemythe destruction :"
        textsurface = myfont.render(text, True, (0, 0, 0))
        screen.blit(textsurface, (SIZEX//20, 3*SIZEY//5))

        for i in range(nb_tics - 1):
            screen.blit(imgs_cross, (SIZEX//5 + i * SIZEX//7, 3*SIZEY//5))



        # Add image of exclamation mark

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


