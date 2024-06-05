import os
import threading
import speech_recognition as sr

# Suppress ALSA error messages
os.environ['PYTHONWARNINGS'] = 'ignore:Warning'

recognizer_lock = threading.Lock()

def speak(text):
    print(text)

def recognize_speech():
    with recognizer_lock:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Écoute...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
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

def continuous_recognition():
    while True:
        try:
            recognize_speech()
        except KeyboardInterrupt:
            print("Exiting program.")
            break

if __name__ == "__main__":
    continuous_recognition()

