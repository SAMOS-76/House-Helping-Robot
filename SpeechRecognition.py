import spacy
import speech_recognition as sr
import sys


class Speech:
    def __init__(self):
        self.object = None  #
        self._nlp = spacy.load('en_core_web_sm')

    def get_object_phrase(self, text):
        # Gets the object of an input sentence
        doc = self._nlp(text)
        for token in doc:
            if "dobj" in token.dep_:
                subtree = list(token.subtree)
                start = subtree[0].i
                end = subtree[-1].i + 1
                self._object = doc[start:end]

    def speech_recognition(self):
        # Converts speech to text
        r = sr.Recognizer()
        mic = sr.Microphone(device_index=1)

        with mic as source:
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
        except:
            print("No sentence spoken")
            sys.exit()

        print(text)
        self.get_object_phrase(text)
