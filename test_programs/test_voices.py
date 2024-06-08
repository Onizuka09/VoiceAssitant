import pyttsx3

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Set the voice to the desired mbrola voice
# Replace 'mb-fr4' with the exact voice name you identified
engine.setProperty('voice', 'mb-fr4')
engine.setProperty('rate', 155)  # Set the speech rate

# Text to be spoken
text = "Bonjours je suis trés content. je suis un étudiant en premiere année ingenieur a l'ISI aaa"

# Use the engine to say the text
engine.say(text)
engine.runAndWait()
