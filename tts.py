import pyttsx3, threading

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.lock = threading.Lock()
        self.is_speaking = False

    def speak(self, text):
        with self.lock:
            self.is_speaking = True
            self.engine.say(text)
            self.engine.runAndWait()
            self.is_speaking = False

    def stop(self):
        with self.lock:
            if self.is_speaking:
                self.engine.stop()
                self.is_speaking = False
