import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import webbrowser
import requests

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set speaking rate (speed)
engine.setProperty('volume', 0.9)  # Set volume (0.0 to 1.0)

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listens to user voice and converts it to text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that. Could you please repeat?")
        return None
    except sr.RequestError:
        speak("Sorry, my speech service is down.")
        return None

def search_google(query):
    """Performs a Google search using SerpAPI and returns the first result URL."""
    api_key = "db123e5b39a6ae97fc277fc153875a8e1913f215862c154138f0240390fcfebd"  # Replace with your actual SerpAPI key
    search_url = f"https://serpapi.com/search.json?api_key={api_key}&q={query}&hl=en"
    
    try:
        response = requests.get(search_url)
        response.raise_for_status()  # Raise an error for bad responses
        
        data = response.json()
        
        if 'organic_results' in data and len(data['organic_results']) > 0:
            first_result = data['organic_results'][0]  # Get the first organic result
            return first_result['link']  # Return the link of the first result
    except Exception as e:
        print(f"Error during search: {e}")
    
    return None

def run_assistant():
    """Main function to handle commands and perform actions."""
    speak("Hello, how can I help you today?")
    while True:
        command = listen()
        
        if command:
            if 'time' in command:
                current_time = datetime.datetime.now().strftime('%I:%M %p')
                speak(f"The current time is {current_time}.")
            
            elif 'play' in command:
                song = command.replace('play', '').strip()
                speak(f"Playing {song}")
                pywhatkit.playonyt(song)

            elif 'search for' in command:
                search_query = command.replace('search for', '').strip()
                speak(f"Searching for {search_query} on Google")
                
                first_result_url = search_google(search_query)
                if first_result_url:
                    speak(f"Opening the top result for {search_query}")
                    webbrowser.open(first_result_url)
                else:
                    speak("I couldn't retrieve the search results. Please try again.")

            elif 'open google' in command:
                speak("Opening Google")
                webbrowser.open("https://www.google.com")

            elif 'open youtube' in command:
                speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com")

            elif 'exit' in command:
                speak("Goodbye!")
                break

            else:
                speak("I'm sorry, I didn't understand that command. Can you please repeat?")
        else:
            continue

# Run the assistant
if __name__ == "__main__":
    run_assistant()
