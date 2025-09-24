# main.py
import os
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from transformers import pipeline
import pyttsx3

from RAG.config import Config
from RAG.vectorstore import VectorDB
from RAG.rag import RAG
from gtts import gTTS

import speech_recognition as sr
import threading



from piper.voice import PiperVoice
import sounddevice as sd
import requests



def record_audio(filename="user_voice.wav", duration=5, samplerate=16000):
    """Record audio from microphone and save it to a file."""
    print("\n🎤 Speak now...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    wav.write(filename, samplerate, audio)
    print("✅ Recording finished.")
    return filename


def transcribe_audio(filename):
    """Convert speech to text using facebook/wav2vec2-base-960h."""
    print("📝 Transcribing...")
    asr = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-base-960h")
    result = asr(filename)
    text = result["text"]
    print(f"🗣️ You said: {text}")
    return text


#---------------------------------------------------------------------------------


def speak_text(text):
    tts = gTTS(text, lang="en")  # 'en' for English
    tts.save("response.mp3")     # gTTS only saves mp3
    os.system("mpg123 response.mp3")  # Or use 'aplay' if you have mp3 support
#---------------------------------------------------------------------------------

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
                result = recognizer.recognize_google(audio, language='en-USA', show_all=True)
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



if __name__ == "__main__":
    config = Config()

    # Build FAISS index if not exists
    if not os.path.exists(config.faiss_index_file):
        print("Building FAISS index...")
        vectordb = VectorDB(config)
        vectordb.preprocess_file()
        vectordb.build_index()

    rag = RAG(config)

    while True:
        print("\n--- Freeways Voice Chatbot ---")
        print("1) Voice query 🎤")
        print("2) Text query ⌨️")
        print("3) Exit ❌")
        choice = input("Choose an option: ")

        if choice == "3":
            break

        if choice == "1":
            
            query = recognize_speech()

        elif choice == "2":
            query = input("\nAsk Freeways chatbot: ")

        else:
            print("Invalid choice.")
            continue

        if query.lower() in ["exit", "quit"]:
            break

        print("🤖 Thinking...")
        answer = rag.pipeline(query)
        print("\n🤖 Chatbot:", answer)

        # Speak the answer
        speak_text(answer)
