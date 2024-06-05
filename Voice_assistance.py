import sys
import threading 
import speech_recognition as sr 
import pyttsx3 as tts 
import os
from face_layout import Face
import time 
from face_layout import pygame
from neuralintents.assistants import BasicAssistant
from neural_intents_exmaple import CustomAssistant
os.environ['PYTHONWARNINGS'] = 'ignore:Warning'

class Assistant:
   def __init__(self) -> None:
      #self.sr = speech_recognition.Recognizer()
      self.speaker  = tts.init()
      self.fc = Face()
      #Self.speaker.setProperty("rate",150) 
      self.is_speaking = False 
      self.mouth_open = False
      self.engine = tts.init(driverName='espeak')
      self.init_spkr()
      self.assistant = CustomAssistant('./intents.json')

      if os.path.exists('./model/basic_model.keras'):
          self.assistant.load_model()
      else:

          self.assistant.fit_model(epochs=50)
          self.assistant.save_model()
      #self.assistant.fit_model(epochs = 50)
      #self.assistant.save_model()
      self.recognizer_lock = threading.Lock()
      self.main_loop()
   def on_start(self,name):
        global is_speaking
        is_speaking = True

   def on_end(self,name, completed):
        global is_speaking
        is_speaking = False
   def onWord(self, name, location, length):
        print(f"Current word: {name}, Location: {location}, Length: {length}")


   def face_anim(self): 
       if is_speaking:
            print("mth dir: ", self.mouth_open) 
            self.fc.draw_face(act="talk", expression="neutral", eyes_open=True, look_direction="center", mouth_open=self.mouth_open)
            time.sleep(0.3)
            self.mouth_open = not self.mouth_open
       else:
            self.fc.draw_face(act="neutral", expression="neutral", eyes_open=True, look_direction="center", mouth_open=True , )

   def speak_text(self,text):
        self.engine.say(text)
        self.engine.runAndWait()

   def init_spkr(self):
        self.engine.connect('started-utterance', self.on_start)
        self.engine.connect('finished-utterance',self. on_end)
        #self.engine.connect('word',self.onWord)
   def main_loop(self):
       try:
            while True:
                self.run()
       except KeyboardInterrupt:
           print("exiting .." )
           exit(0)
   def create_file(self):
      print("file createte") 

   def speak(self,text):
       self.speaker.say(text)
       self.speaker.runAndWait()

   def run(self):
       resp=""
       thread_e  = threading.Thread(target= self.speak, args =(resp,))
       with self.recognizer_lock:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Écoute...")
                recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    result = recognizer.recognize_google(audio)#, language='fr-FR', show_all=True)
                    print(f"result: {result}")
                    text = result.lower()
                    if text is not None:
                        resp = self.assistant.process_input(text)
                        #self.speak(resp)    
                        thread_e.start()
                except sr.WaitTimeoutError:
                    self.speak("Temps Ecouler sans entre un vocale" )
                    
                except sr.UnknownValueError:
                    self.speak("Désolé, Errure undefinie.")
                    
                except sr.RequestError:
                    self.speak("Désolé, le service de reconnaissance vocale est en panne.")
                    
                except Exception as e:
                    print(f"Exception: {e}")
                    self.speak("Une erreur est survenue lors de la reconnaissance vocale.")
                    



#if __name__ == '__main__':
Assistant()


