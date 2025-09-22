import pyttsx3

# Initialize the pyttsx3 engine
engine = pyttsx3.init('espeak' )

# Set the voice to the desired mbrola voice
# Replace 'mb-fr4' with the exact voice name you identified

engine.setProperty('voice', 'english')
# for v in engine.getProperty('voices'): 
    # print (v) 
engine.setProperty('rate', 100)  # Set the speech rate

engine.setProperty('pitch',50)
# Text to be spoken
text = "Hello everyone i am happy to see you all  "# je suis trés content. je suis un étudiant en premiere année ingenieur a l'ISI aaa"

# Use the engine to say the text
engine.say(text)
engine.runAndWait()
