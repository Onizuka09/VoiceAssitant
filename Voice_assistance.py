import sys
import threading 
import speech_recognition as sr 
import pyttsx3 as tts 
import os
from face_layout import Face
import time 
from face_layout import pygame
from neuralintents.assistants import BasicAssistant
from Custom_assistant import CustomAssistant

import queue 


os.environ['PYTHONWARNINGS'] = 'ignore:Warning'

class Assistant:
   def __init__(self) -> None:
      #self.sr = speech_recognition.Recognizer()
      self.speaker  = tts.init()#driverName= 'espeak')
      #self.fc = Face()
      #self.set_voice()
      self.speaker.setProperty('voice', 'mb/mb-fr1')
      self.speaker.setProperty('rate', 100)  # Set the speech rate


      #self.speaker.setProperty("rate",150) 
      self.is_speaking = False 
      self.mouth_open = False

      self.tts_queue = queue.Queue()
      #self.engine = tts.init(driverName='espeak')
      self.init_spkr()
      self.assistant = CustomAssistant('./intents.json')

      if os.path.exists('basic_model.keras'):
          self.assistant.load_model()
          print("model loaded...") 
      else:
          self.assistant.fit_model(epochs=50)
          self.assistant.save_model()
      #self.assistant.fit_model(epochs = 50)
      #self.assistant.save_model()
      self.recognizer_lock = threading.Lock()
      #self.main_loop()
   def on_start(self,name):
        print("started speaking") 
        self.is_speaking = True

   def on_end(self,name, completed):
        print("finished speaking")
        self.is_speaking = False
   def onWord(self, name, location, length):
        print(f"Current word: {name}, Location: {location}, Length: {length}")

   def set_voice(self): 
        voices = self.speaker.getProperty('voices')
        for voice in voices: 
            if "french" in voice.name.lower():
                print(voice)

   def face_anim(self): 
       pass
       """ 
       if is_speaking:
            print("mth dir: ", self.mouth_open) 
            self.fc.draw_face(act="talk", expression="neutral", eyes_open=True, look_direction="center", mouth_open=self.mouth_open)
            time.sleep(0.3)
            self.mouth_open = not self.mouth_open
       else:
            self.fc.draw_face(act="neutral", expression="neutral", eyes_open=True, look_direction="center", mouth_open=True , )
        """
 
   def init_spkr(self):
        self.speaker.connect('started-utterance', self.on_start)
        self.speaker.connect('finished-utterance',self.on_end)
        #self.engine.connect('word',self.onWord)
   """
   def main_loop(self):
       try:
            while True:
                self.run()
       except KeyboardInterrupt:
           print("exiting .." )
           exit(0)
   """
   def create_file(self):
      print("file createte") 

   def speak_worker(self):
       while True:

           text = self.tts_queue.get() 
        
           if text is None:
               break 
           self.speaker.say(text)
           print("i am speaking ", text )
           self.speaker.runAndWait()
           self.tts_queue.task_done()
   def speak(self,text):
       print("Speaking this: ",text) 
       self.tts_queue.put(text)

   def run(self):
        while True:
            if not self.is_speaking : 
              resp = ""
              with self.recognizer_lock:
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Écoute...")
                    recognizer.adjust_for_ambient_noise(source)
                    try:
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        result = recognizer.recognize_google(audio, language='fr-FR')
                        print(f"result: {result}")
                        text = result.lower()
                        if text is not None:
                            resp = self.assistant.process_input(text)
                            self.speak(resp)
                    except sr.WaitTimeoutError:
                        self.speak("Temps Ecouler sans entre un vocale")
                    except sr.UnknownValueError:
                        self.speak("Désolé, Errure undefinie.")
                    except sr.RequestError:
                        self.speak("Désolé, le service de reconnaissance vocale est en panne.")
                    except Exception as e:
                        print(f"Exception: {e}")
                        self.speak("Une erreur est survenue lors de la reconnaissance vocale.")

   def main(self):
        pygame.init()
        #screen = pygame.display.set_mode((0,0) , pygame.FULLSCREEN)  
        screen = pygame.display.set_mode((400,400))  
        tts_thread = threading.Thread(target=self.speak_worker, daemon=True )
        assistant_thread = threading.Thread(target=self.run)
 
        fc_lay = Face(screen )
        run = True
        is_talking = False
        assistant_thread.start()
        tts_thread.start() 
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            if self.is_speaking:
                fc_lay.talk2() 
               #self.clock.tick(0.3)
            else :
                fc_lay.draw_face(act="neutral",expression="talk", eyes_open=True, look_direction="center",mouth_open=True)
            pygame.display.flip()    
        self.tts_queue.put(None)
        tts_thread.join()
        assistant_thread.join()
        pygame.quit()

    

#if __name__ == '__main__':
assisst = Assistant()
assisst.main()

