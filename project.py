# TRY 1 TO COMPLETE POORA CONVERSATION
from flask import Flask, request, jsonify
import speech_recognition as sr
import pyttsx3
import spacy
import datetime

app = Flask(__name__)
# Initialize speech recognition, TTS, and NLU
r = sr.Recognizer()
nlp = spacy.load("en_core_web_sm")
engine = pyttsx3.init()
print("i have codedddd")
# Define some simple intents and responses
intents = {
    "greeting": ["hello", "hi", "hey", "good morning", "good evening", "hey there"],
    "product_inquiry": ["tell me about your product", "what do you sell", "give me more info about your products"],
    "price_inquiry": ["how much does it cost", "what is the price", "pricing details", "how much is it"],
    "thank_you": ["thank you", "thanks", "appreciate it"],
    "goodbye": ["bye", "goodbye", "see you", "later", "talk to you soon"],
    "default": ["sorry", "what", "huh", "can you repeat that"]
}

responses = {
    "greeting": "Hello! How can I assist you with your purchase today?",
    "product_inquiry": "We offer a variety of products, including electronics, home appliances, and accessories. Which category interests you?",
    "price_inquiry": "Our products range from $10 to $500 depending on the item. What product are you interested in?",
    "thank_you": "You're welcome! I'm here to help.",
    "goodbye": "Goodbye! Have a great day, and thank you for your interest in our products!",
    "default": "I'm sorry, I didn't quite catch that. Could you please repeat?"
}


# Function to recognize speech and return text

def record_text():
    while True:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.3)
                audio2 = r.listen(source2, timeout=5, phrase_time_limit=10)
                MyText = r.recognize_google(audio2)
                return MyText
        except sr.RequestError as e:
            print(f"Request error: {e}")
        except sr.UnknownValueError:
            print("Unknown error occurred")


# Function to process natural language understanding (NLU) and extract useful information
def process_nlu(text):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]
    verbs = [token.text for token in doc if token.pos_ == "VERB"]
    return entities, verbs


# Function to match intents based on keywords in the text
def match_intent(text):
    text = text.lower()
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in text:
                return intent
    return "default"


# Function to generate response based on intent
def respond(intent):
    response = responses.get(intent, responses["default"])
    if callable(response):
        return response()
    return response


# Function to speak the response using TTS
def speak_response(response):
    engine.say(response)
    engine.runAndWait()


# Function to handle the entire conversation flow
def conversation():
    print("Agent is ready to speak.")
    while True:
        # Step 1: Record customer's speech
        text = record_text()
        print(f"Customer said: {text}")

        # Step 2: Process the text (NLU)
        entities, verbs = process_nlu(text)
        print(f"Entities: {entities}, Verbs: {verbs}")

        # Step 3: Match intent based on the text
        intent = match_intent(text)
        print(f"Matched intent: {intent}")

        # Step 4: Generate a response based on the intent
        response = respond(intent)
        print(f"Agent responds: {response}")

        # Step 5: Speak the response
        speak_response(response)

        # Step 6: End conversation if intent is goodbye
        if intent == "goodbye":
            break
@app.route("/conversation", methods=["POST"])
def handle_conversation():
    input_text = record_text()  # Simulating speech input for this example

    if input_text:
        print(f"Customer said: {input_text}")

        # Match intent
        intent = match_intent(input_text)
        print(f"Matched intent: {intent}")

        # Generate response
        response = respond(intent)
        print(f"Agent responds: {response}")

        # Speak the response
        speak_response(response)

        # Return Exotel XML response
        return f"""
        <Response>
            <Say>{response}</Say>
            <Gather action="/conversation" method="POST" numDigits="1" timeout="10"/>
        </Response>
        """
    else:
        # If no input, repeat request
        return f"""
        <Response>
            <Say>Sorry, I didn't quite catch that. Could you please repeat?</Say>
            <Gather action="/conversation" method="POST" numDigits="1" timeout="10"/>
        </Response>
        """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# Start the conversation
#conversation()
