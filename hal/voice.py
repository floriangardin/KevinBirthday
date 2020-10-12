import pyttsx3
import threading






class Voice:

    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        print(self.engine.getProperty('voices'))
        voice = self.engine.getProperty('voices')[2]  # the french voice
        newVoiceRate = 150
        self.engine.setProperty('rate', newVoiceRate)
        self.engine.setProperty('voice', voice.id)
        self.should_stop = False
        self._running = False

    def say(self, text):

        threading.Thread(
            target=self.say_, args=(text,), daemon=True
        ).start()

    def stop(self):
        threading.Thread(
            target=self.stop_, daemon=True
        ).start()


    def stop_(self):
        self.engine.stop()

    def say_(self, text):
        self._running = False

        while True:
            if not self.engine._inLoop:
                break
            try:
                self.engine.endLoop()
                break
            except Exception as e:
                print(e)
        voice = self.engine.getProperty('voices')[2]  # the french voice
        newVoiceRate = 150
        self.engine.setProperty('rate', newVoiceRate)
        self.engine.setProperty('voice', voice.id)
        self.engine.say(text)
        self.engine.startLoop(False)
        self._running = True
        self.engine.iterate()