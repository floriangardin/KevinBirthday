from .voice import Voice

FULLSCREEN = False
WHITE_NOISE_DURATION = 1000
STATE_WHITE_NOISE = 'WHITE_NOISE'
STATE_MAIN = 'MAIN'

class State:

    def __init__(self):
        self.state = STATE_WHITE_NOISE
        self.start_time_whitenoise = None

    def set_state(self, state):
        print('Change state from', self.state, 'to', state)
        if state == STATE_WHITE_NOISE:
            self.state = STATE_WHITE_NOISE
            self.start_time_whitenoise = None

        if state == STATE_MAIN:
            self.state = STATE_MAIN


voice = Voice()
state = State()