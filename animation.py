
from face_layout import Face
import time
from face_layout import pygame
#pygame.quit()
import threading
import pyttsx3
is_speaking = False
running = True
engine = pyttsx3.init(driverName='espeak')
f = Face((400,400)) 
mouth_open = False
def on_start(name):
    global is_speaking
    is_speaking = True

def on_end(name, completed):
    global is_speaking
    is_speaking = False
def onWord(name, location, length):
    print(f"Current word: {name}, Location: {location}, Length: {length}")


def talk(): 
    global mouth_open
    print("mth dir: ", mouth_open) 
    f.draw_face(act="talk", expression="neutral", eyes_open=True, look_direction="center", mouth_open=mouth_open)
    time.sleep(0.3)
    mouth_open = not mouth_open

def speak_text(text):
    engine.say(text)
    engine.runAndWait()



def init():
    engine.connect('started-utterance', on_start)
    engine.connect('finished-utterance', on_end)
    engine.connect('word',onWord)





text = "Hello, how can I help you today?  , I am fine Thank you !"
# Speak the initial text
thread_e = threading.Thread(target=speak_text, args=(text,))
thread_a = threading.Thread(target=talk)
def main():
    global running
    global is_speaking
    init()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                thread_e.start()
        if is_speaking: 
            #talk()
            thread_a.start()
        else:    
        #thread_a.stops()
            f.draw_face(act="neutral", expression="neutral", eyes_open=True, look_direction="center", mouth_open=True , )
    pygame.quit() 
main()
#f.test()


