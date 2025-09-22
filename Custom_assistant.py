import random
import numpy as np
import nltk
import os
import json
import pickle
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, InputLayer
from tensorflow.keras.optimizers import Adam, Optimizer
from tensorflow.keras.optimizers import Adam, Optimizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from neuralintents.assistants import BasicAssistant

class CustomAssistant(BasicAssistant):
    def __init__(self, intents_file, confidence_threshold=0.6):
        super().__init__(intents_file)
        self.confidence_threshold = confidence_threshold
        self.context = None  # Initialize context

    def _predict_intent(self, input_text: str):
        input_words = nltk.word_tokenize(input_text)
        input_words = [self.lemmatizer.lemmatize(w.lower()) for w in input_words]

        input_bag_of_words = [0] * len(self.words)

        for input_word in input_words:
            for i, word in enumerate(self.words):
                if input_word == word:
                    input_bag_of_words[i] = 1

        input_bag_of_words = np.array([input_bag_of_words])

        predictions = self.model.predict(input_bag_of_words, verbose=0)[0]
        max_prob = np.max(predictions)

        if max_prob < self.confidence_threshold:
            return None
        predicted_intent = self.intents[np.argmax(predictions)]
        return predicted_intent
    

    def fit_model(self, optimizer: Optimizer = None, epochs=200):

        X, y = self._prepare_intents_data()
        if self.hidden_layers is None:
            self.model = Sequential()
            self.model.add(InputLayer(input_shape=(X.shape[1],)))
            self.model.add(Dense(128, activation='relu'))
            self.model.add(Dropout(0.5))
            self.model.add(Dense(64, activation='relu'))
            self.model.add(Dropout(0.5))
            self.model.add(Dense(y.shape[1], activation='softmax'))
        else:
            self.model = Sequential()
            self.model.add(InputLayer(input_shape=(X.shape[1],)))
            for layer in self.hidden_layers:
                self.model.add(layer)
            self.model.add(Dense(y.shape[1], activation='softmax'))

        if optimizer is None:
            optimizer = Adam(learning_rate=0.01)

        self.model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])

        self.history = self.model.fit(X, y, epochs=epochs, batch_size=5, verbose=1)

    def save_model(self):
        self.model.save(f"{self.model_name}.keras")
        pickle.dump(self.words, open(f'{self.model_name}_words.pkl', 'wb'))
        pickle.dump(self.intents, open(f'{self.model_name}_intents.pkl', 'wb'))
    
    def load_model(self):
        self.model = load_model(f'{self.model_name}.keras')
        self.words = pickle.load(open(f'{self.model_name}_words.pkl', 'rb'))
        self.intents = pickle.load(open(f'{self.model_name}_intents.pkl', 'rb'))

    def process_input(self, input_text: str):
        predicted_intent = self._predict_intent(input_text)

        if predicted_intent is None:
            return "I don't understand. Can you please rephrase?"

        try:
            for intent in self.intents_data["intents"]:
                if intent["tag"] == predicted_intent:
                    if "context_filter" in intent:
                        if intent["context_filter"] == self.context:
                            if "context_set" in intent and intent["context_set"]:
                                self.context = intent["context_set"]
                            if self.is_follow_up(intent):
                                return str(self.handle_follow_up(intent)) + " " + str(random.choice(intent["responses"]))
                            else:
                                return random.choice(intent["responses"])
                        else:
                            continue
                    else:
                        if "context_set" in intent and intent["context_set"]:
                            self.context = intent["context_set"]
                        if self.is_transition(intent):
                            return self.handle_transition()
                        else:
                            return random.choice(intent["responses"])

            return "I don't understand. Please rephrase."
        except IndexError:
            return "I don't understand. Please try again."
    def is_follow_up(self, intent):
        return "follow_up" in intent["tag"]

    def handle_follow_up(self, intent):
        # Implement logic to handle follow-up questions
        return "Sure, here's more information about Tunisian food..."

    def is_transition(self, intent):
        return intent["tag"] == "switch_topic"

    def handle_transition(self):
        # Implement logic to handle topic transitions
        return "Sure! What topic would you like to explore next?"

        

if __name__ == '__main__':
# Usage example
    assistant = CustomAssistant('intents_en.json')
    assistant.fit_model(epochs=50)
    assistant.save_model()
    done = False
    while not done:
        message = input("You: ")
        if message.lower() == "stop":
            done = True
        else:
            print("Assistant:", assistant.process_input(message))


