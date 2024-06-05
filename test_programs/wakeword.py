import os
import threading
import speech_recognition as sr

# Suppress ALSA error messages
os.environ['PYTHONWARNINGS'] = 'ignore:Warning'

recognizer_lock = threading.Lock()

def speak(text):
    print(text)

def recognize_speech(timeout=None, phrase_time_limit=None):
    with recognizer_lock:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Écoute...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            try:
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                result = recognizer.recognize_google(audio, language='fr-FR', show_all=True)
                print(f"result: {result}")
                if result and 'alternative' in result:
                    text = result['alternative'][0]['transcript']
                    print(f"L'utilisateur a dit: {text}")
                    return text.lower()
                else:
                    speak("Désolé, je n'ai pas compris.")
                    return ""
            except sr.WaitTimeoutError:
                speak("Temps écoulé sans entrée vocale.")
                return ""
            except sr.UnknownValueError:
                speak("Désolé, je n'ai pas compris.")
                return ""
            except sr.RequestError:
                speak("Désolé, le service de reconnaissance vocale est en panne.")
                return ""
            except Exception as e:
                print(f"Exception: {e}")
                speak("Une erreur est survenue lors de la reconnaissance vocale.")
                return ""

def listen_for_wake_word(wake_word):
    while True:
        print("Listening for wake word...")
        text = recognize_speech(timeout=10, phrase_time_limit=5)
        if wake_word in text:
            print("Wake word detected!")
            return True 

def process_commands():
    while True:
        print("Listening for commands...")
        text = recognize_speech(timeout=5, phrase_time_limit=10)
        if text:
            if "arrête" in text:
                print("Stopping the assistant.")
                break
            else:
                print(f"Processing command: {text}")

def assistant_loop():
    wake_word = "jarvis"
    while True:
        st = listen_for_wake_word(wake_word)
        
        if (st):
            print("Enter COmmand" ) 
            process_commands()

if __name__ == "__main__":
    try:
        assistant_loop()
    except KeyboardInterrupt:
        print("Exiting program.")

