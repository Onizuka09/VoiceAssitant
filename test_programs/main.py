import cv2
import pyttsx3
import speech_recognition as sr
import threading
import queue
import time
import os

os.environ['PYTHONWARNINGS'] = 'ignore:Warning'
user_interacted = False
is_speaking =False

# calcback function for pyttsx3 

def onStart(name):
    is_speaking= True
    print("Speech started")

def onEnd(name, completed):
    is_speaking = False
    if completed:
        print("Speech completed")
    else:
        print("Speech interrupted")


# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.connect('started-utterance', onStart)
engine.connect('finished-utterance', onEnd)
# Queue to handle TTS requests
tts_queue = queue.Queue()

# Lock for speech recognition to prevent concurrent access
recognizer_lock = threading.Lock()

# Set properties for the TTS engine
def setup_tts_engine():
    voices = engine.getProperty('voices')
    french_voice = None
    
    for voice in voices:
        if "french" ==  voice.name.lower(): # or "fr" in voice.id.lower():
            french_voice = voice
            print("French voice set", voice)
            #break

   
  #  french_voice= 
    if french_voice:
        engine.setProperty('voice', french_voice.id)
    else:
        print("French voice not found. Using default voice.")
    engine.setProperty('rate', 150)  # Speed can be adjusted (default is usually around 200)
    engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)



# Function to process the TTS queue
def tts_worker():
    while True:
        text = tts_queue.get()
        if text is None:
            break
        engine.say(text)
        engine.runAndWait()
        tts_queue.task_done()

# Start the TTS worker thread

# Function to add text to the TTS queue
def speak(text):
    print(text)
    tts_queue.put(text)

# Function to recognize speech and return the text
def recognize_speech():
    global user_interacted
    with recognizer_lock:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Écoute...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            #audio = recognizer.listen(source)
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                result = recognizer.recognize_google(audio, language='fr-FR', show_all=True)
                print(f"result: {result}")
                if result and 'alternative' in result:
                    text = result['alternative'][0]['transcript']
                    print(f"L'utilisateur a dit: {text}")
                    return text.lower()
                else:
                    speak("Désolé, je n'ai pas compris.")
                    user_interacted=False
                    return ""
            except sr.WaitTimeoutError:
                speak("Temps Ecouler sans entre un vocale" )
            except sr.UnknownValueError:
                speak("Désolé, Errure undefinie.")
                user_interacted=False
                return ""
            except sr.RequestError:
                speak("Désolé, le service de reconnaissance vocale est en panne.")
                user_interacted=False
                return ""
            except Exception as e:
                print(f"Exception: {e}")
                speak("Une erreur est survenue lors de la reconnaissance vocale.")
                user_interacted=False
                return ""

# Function to provide detailed information about Tunisia
def provide_information(topic):
    details = {
        "histoire": "La Tunisie a une histoire riche qui remonte à l'antiquité. Elle a été un point central pour de nombreuses civilisations, y compris les Carthaginois, les Romains, et les Ottomans.",
        "culture": "La culture tunisienne est un mélange de différentes influences, incluant les traditions arabes, berbères, européennes et africaines. La musique, l'artisanat, et la cuisine sont des aspects importants de cette culture.",
        "géographie": "La Tunisie est située en Afrique du Nord, bordée par l'Algérie à l'ouest, la Libye au sud-est et la mer Méditerranée au nord et à l'est. Sa capitale est Tunis.",
        "gastronomie": "La cuisine tunisienne est connue pour ses saveurs épicées et ses ingrédients frais. Les plats populaires incluent le couscous, la brik, et la harissa."
    }
    return details.get(topic, "Désolé, je n'ai pas d'informations sur ce sujet.")

# Function to handle the voice assistant interaction
def voice_assistant_interaction():
    speak("voulez vous connaitre la tunisie  ?")
    time.sleep(1)  # Wait for 1 second to ensure speech synthesis is complete
    user_response = recognize_speech()
    print(f"User response: {user_response}")

    if "oui" in user_response or "yes" in user_response:
        speak("La Tunisie est un pays d'Afrique du Nord bordant la mer Méditerranée et le désert du Sahara. Sa capitale est Tunis, et elle a une riche histoire avec de nombreux sites anciens.")
        speak("Voulez-vous en savoir plus sur l'histoire, la géographie, ou la gastronomie de la Tunisie?")
        time.sleep(12)  # Wait for 1 second before listening for user response
        user_interest = recognize_speech()
        print(f"User interest: {user_interest}")

        if any(topic in user_interest for topic in ["histoire", "géographie", "gastronomie"]):
            for topic in ["histoire", "géographie", "gastronomie"]:
                if topic in user_interest:
                    speak(f"D'accord, je vais vous parler de la {topic} de la Tunisie.")
                    speak(provide_information(topic))
                
                    break
        else:
            speak("Désolé, je n'ai pas compris votre demande.")
    elif "non" in user_response:
        speak("D'accord, peut-être une autre fois.")
    else:
        speak("Désolé, je n'ai pas compris.")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 200)

side_border_color = (0, 0, 255)
side_borders_distance = 100
top_border = 50

# Flag to track if a face has been detected for the first time
first_face_detected = False


def main_loop():
    setup_tts_engine()

    tts_thread = threading.Thread(target=tts_worker, daemon=True)
    tts_thread.start()


    global first_face_detected, user_interacted
    
    while True:
        _, img = cap.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.1, 3)

        if len(faces) > 0 and not first_face_detected:
            speak("Bonjour, comment puis-je vous aider ?")
            first_face_detected = True

        if first_face_detected and not user_interacted and not is_speaking:
            voice_thread = threading.Thread(target=voice_assistant_interaction)
            voice_thread.start()
            user_interacted = True

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.line(img, (side_borders_distance, 0), (side_borders_distance, img.shape[0]), side_border_color, 5)
        cv2.line(img, (img.shape[1] - side_borders_distance, 0),
                 (img.shape[1] - side_borders_distance, img.shape[0]), side_border_color, 5)

        cv2.line(img, (0, 66), (320, 66), (0, 100, 255), 5)
        cv2.line(img, (0, 170), (320, 170), (0, 100, 255), 5)
        cv2.imshow('img', img)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
   
    tts_queue.put(None)
    tts_thread.join()
      
    cap.release()
    cv2.destroyAllWindows()
 
if __name__ == "__main__":
    main_loop()
    
    #speak("Bonjours comment vas tu ? ") 
    print("hello world")
