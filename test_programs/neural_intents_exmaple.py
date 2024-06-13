import random
import numpy as np
import nltk
from neuralintents.assistants import BasicAssistant
class CustomAssistant(BasicAssistant):
    def __init__(self, intents_file, confidence_threshold=0.6):
        super().__init__(intents_file)
        self.confidence_threshold = confidence_threshold
        self.context = None  # Initialize context



    def _predict_intent(self, input_text):
        input_words = nltk.word_tokenize(input_text)
        input_words = [self.lemmatizer.lemmatize(w.lower()) for w in input_words]

        input_bag_of_words = [0] * len(self.words)

        for input_word in input_words:
            for i, word in enumerate(self.words):
                if input_word == word:
                    input_bag_of_words[i] = 1

        input_bag_of_words = np.array([input_bag_of_words])

        predictions = self.model.predict(input_bag_of_words, verbose=0)[0]
        #predicted_intent = self.intents[np.argmax(predictions)]

        max_prob = np.max(predictions)
        print(max_prob)
        if max_prob < self.confidence_threshold:
             return None
        predicted_intent = self.intents[np.argmax(predictions)]

        return predicted_intent
    def process_input(self, input_text: str):
        predicted_intent = self._predict_intent(input_text)

        if predicted_intent is None :
            # Handle out-of-context or unknown input
            #self.context = "out_of_context"
            return "I don't understand. Can you please rephrase?"
        
        try:
            # Check if the predicted intent is relevant to the current context
            for intent in self.intents_data["intents"]:
                if intent["tag"] == predicted_intent:
                    print(intent)
                    if "context_filter" in intent:
                        if intent["context_filter"] == self.context:
                            if "context_set" in intent and intent["context_set"]:
                                self.context = intent["context_set"] 
                            # Handle follow-up questions
                            if self.is_follow_up(intent):
                                out= str( self.handle_follow_up(intent))+" "+str(random.choice(intent["responses"] )) 
                                return out
                            else:
                                return random.choice(intent["responses"])
                        else:
                            print("the context filter and the context no doesn't much up" ) 
                            continue
                    else:
                        # Handle transitions
                        if "context_set" in intent and intent["context_set"]:
                            self.context = intent["context_set"]
                        if self.is_transition(intent):
                            return self.handle_transition()
                        else:
                            return random.choice(intent["responses"])

            # If no matching intent is found
            print("The context is: ", self.context)
            return "I don't understand. Please rephrase."
        except IndexError:
            return "I don't understand. Please try again."
        """
        try:
        # Check if the predicted intent is relevant to the current context
            for intent in self.intents_data["intents"]:
                if intent["tag"] == predicted_intent:
                    print(intent)
                    if "context_filter" in intent:
                        if intent["context_filter"] == self.context:
                        # Update context if context_set is present
                            if "context_set" in intent and intent["context_set"]:
                                self.context = intent["context_set"]
                            return random.choice(intent["responses"])
                        else:
                            continue
                    else:
                    # Update context if context_set is present
                        if "context_set" in intent and intent["context_set"]:
                            self.context = intent["context_set"]
                            return random.choice(intent["responses"])
            print("The context is: ", self.context)
            return "I don't understand. Please try again."
        except IndexError:
            return "I don't understand. Please try again."
        """
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
    assistant = CustomAssistant('test_intents.json')
    assistant.fit_model(epochs=50)
    assistant.save_model()
    done = False
    while not done:
        message = input("You: ")
        if message.lower() == "stop":
            done = True
        else:
            print("Assistant:", assistant.process_input(message))

