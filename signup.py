from flask import Flask, render_template
from flask_socketio import SocketIO
import speech_recognition as sr
import pyttsx3
import requests
import re
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to emit message to the front end
def emit_message(message):
    socketio.emit('message', message)

# Function to speak a message and emit to the front end
def speak(message):
    engine.say(message)
    engine.runAndWait()
    emit_message(message)

# Function to get audio input from the user
def get_audio_input(prompt):
    # Speak the prompt
    speak(prompt)

    # Use microphone for capturing speech
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        emit_message(prompt)
        audio = recognizer.listen(source)
    
    try:
        # Recognizing the speech using Google's API
        text = recognizer.recognize_google(audio)
        emit_message(f"You said: {text}")

        # Replace common words (like "at" with "@") and clean up text
        text = re.sub(r'\bat\b', '@', text)
        text = re.sub(r'\bdot\b', '.', text)
        text = re.sub(r'\s+', ' ', text).strip()

        return text
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please try again.")
        return get_audio_input(prompt)  # Retry if speech is not understood
    except sr.RequestError as e:
        speak("Sorry, there was an error with the speech recognition service.")
        return None

# Main function for the login/signup process
def main():
    speak("Welcome to the audio interactive login and signup system.")
    
    # Ask for email
    email = get_audio_input("Please say your email address.")
    speak(f"Your email is {email}.")
    
    # Ask for password
    password = get_audio_input("Please say your password.")
    speak("Your password has been captured.")
    
    # Send data to the Express server for login/signup
    express_url = 'http://localhost:5000/signup'  # Change to '/login' for login
    data = {
        'mail': email,
        'password': password
    }

    try:
        response = requests.post(express_url, json=data)

        if response.status_code == 200:
            speak("Your signup was successful.")
            emit_message(response.json())
        elif response.status_code == 409:  # Conflict, user already exists
            speak("This email is already registered. Please try another email.")
            emit_message("User already exists.")
        else:
            speak("There was an error with your signup. Please try again.")
            emit_message(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        speak("There was a problem connecting to the server. Please try again later.")
        emit_message(f"Error: {e}")

# Background task to start main function
def run_main_in_background():
    threading.Thread(target=main).start()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit_message("Connected to the server.")
    run_main_in_background()  # Start the main process in the background

if __name__ == '__main__':
    socketio.run(app, debug=True)
