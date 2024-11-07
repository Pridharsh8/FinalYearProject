import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    """Speak out the given text."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to a command from the user."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
        
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
        except sr.UnknownValueError:
            print("Sorry, I did not understand.")
            speak("Sorry, I did not understand.")
            return None
        except sr.RequestError:
            print("Request failed; check your internet connection.")
            speak("Request failed; please check your internet connection.")
            return None

    return query.lower()

def respond_to_command(command):
    """Process and respond to user command."""
    if 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The time is {current_time}")
    
    elif 'open google' in command:
        webbrowser.open('https://www.google.com')
        speak("Opening Google")
    
    elif 'open youtube' in command:
        webbrowser.open('https://www.youtube.com')
        speak("Opening YouTube")
    
    elif 'how are you' in command:
        speak("I'm here to assist you!")
    
    elif 'search for' in command:
        # Extract the search query
        search_query = command.replace('search for', '').strip()
        speak(f"Searching for {search_query}")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
    
    elif 'exit' in command or 'stop' in command:
        speak("Goodbye!")
        return 'exit'  # Indicate to exit the loop
    
    else:
        speak("Sorry, I didn't understand that command.")

def virtual_assistant():
    """Main function for the virtual assistant."""
    speak("Hello, I am your virtual assistant. How can I help you?")
    
    while True:
        command = listen()
        if command:
            if respond_to_command(command) == 'exit':
                break

# Run the virtual assistant
virtual_assistant()
