from flask import Flask, render_template, request, jsonify
import spacy
import pyttsx3
import speech_recognition as sr

# Initialize the Flask app
app = Flask(__name__)

# Load the language model
nlp = spacy.load("en_core_web_sm")

# Initialize pyttsx3 for Text-to-Speech
engine = pyttsx3.init()

# Define intents and responses
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
    "product_inquiry": "We offer a variety of products. Which category interests you?",
    "price_inquiry": "Our products range from $10 to $500 depending on the item. What product are you interested in?",
    "thank_you": "You're welcome! I'm here to help.",
    "goodbye": "Goodbye! Have a great day!",
    "default": "I'm sorry, I didn't quite catch that. Could you please repeat?"
}

# Function to match intent
def preprocess_input(text):
    return text.strip().lower()

def match_intent(text):
    text_doc = nlp(preprocess_input(text))
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in text:  # Simple substring match
                return intent
            keyword_doc = nlp(keyword.lower())
            if text_doc.similarity(keyword_doc) > 0.7:  # Semantic similarity
                return intent
    return "default"

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')  # Correctly serving the index.html from templates folder

# Route to handle conversation
@app.route('/conversation', methods=['POST'])
def conversation():
    user_input = request.json.get("text", "")
    intent = match_intent(user_input)
    response = responses.get(intent, responses["default"])
    text_to_speech(response)
    return jsonify({"response": response})

# Function to handle text-to-speech
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

# Function to convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand that."
        except sr.RequestError:
            return "Sorry, the speech service is down."

# Main entry point
if __name__ == "__main__":
    app.run(debug=True)
