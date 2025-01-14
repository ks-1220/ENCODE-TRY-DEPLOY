const chatBox = document.getElementById('chat-box');
let recognition;
let isListening = false;

function appendMessage(message, sender) {
    const div = document.createElement('div');
    div.textContent = `${sender}: ${message}`;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function startListening() {
    if (window.SpeechRecognition || window.webkitSpeechRecognition) {
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = "en-US";
        recognition.onstart = () => {
            isListening = true;
            appendMessage("Listening...", "System");
        };
        recognition.onresult = (event) => {
            const userText = event.results[0][0].transcript;
            appendMessage(userText, "User");
            sendTextToServer(userText);
        };
        recognition.onend = () => {
            isListening = false;
        };
        recognition.start();
    } else {
        appendMessage("Speech Recognition not supported", "System");
    }
}

function stopListening() {
    if (isListening && recognition) {
        recognition.stop();
        isListening = false;
        appendMessage("Stopped listening.", "System");
    }
}

function sendTextToServer(userInput) {
    fetch('/conversation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: userInput })
    })
    .then(response => response.json())
    .then(data => {
        const botResponse = data.response;
        appendMessage(botResponse, "Bot");
        textToSpeech(botResponse);
    })
    .catch(err => {
        appendMessage("Error: " + err, "System");
    });
}

function textToSpeech(text) {
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = 'en-US';
    window.speechSynthesis.speak(speech);
}
