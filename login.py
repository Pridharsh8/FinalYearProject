import speech_recognition as sr
import pyttsx3
import requests
import re

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak a message
def speak(message):
    engine.say(message)
    engine.runAndWait()

# Function to get audio input from the user
def get_audio_input(prompt):
    # Speak the prompt
    speak(prompt)

    # Use microphone for capturing speech
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print(prompt)
        audio = recognizer.listen(source)
    
    try:
        # Recognizing the speech using Google's API
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")

        # Replacing 'at' with '@' and 'dot' with '.' and removing extra spaces
        text = re.sub(r'\bat\b', '@', text)  # Replaces 'at' with '@'
        text = re.sub(r'\bdot\b', '.', text)  # Replaces 'dot' with '.'
        text = re.sub(r'\s+', ' ', text)  # Ensures only single spaces between words
        text = text.strip()  # Remove any leading/trailing spaces

        return text
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please try again.")
        return get_audio_input(prompt)  # Retry if speech is not understood
    except sr.RequestError as e:
        speak("Sorry, there was an error with the speech recognition service.")
        return None

# Main function for the login/signup process
def main():
    speak("Welcome to the audio interactive login system.")
    
    # Ask for email
    email = get_audio_input("Please say your email address.")
    speak(f"Your email is {email}.")
    
    # Ask for password
    password = get_audio_input("Please say your password.")
    speak("Your password has been captured.")
    
    # Send data to the Express server for login/signup
    express_url = 'http://localhost:5000/login'  # Change to '/login' endpoint for login
    data = {
        'mail': email,
        'password': password
    }

    try:
        response = requests.post(express_url, json=data)

        if response.status_code == 200:
            speak("Welcome to the platform!")
            print("Login successful!")
            print(response.json())  # Prints the user data from the response
        elif response.status_code == 404:  # Not found, user doesn't exist
            speak("No account found. You need to register first.")
            print("User does not exist.")
            # Call the signup route
            express_url_signup = 'http://localhost:5000/signup'
            signup_response = requests.post(express_url_signup, json=data)
            if signup_response.status_code == 200:
                speak("Registration successful. You can now log in.")
                print("Signup successful!")
            else:
                speak("There was an error with registration. Please try again.")
                print("Error during signup:", signup_response.status_code)
        else:
            speak("There was an error with your login. Please try again.")
            print("Error:", response.status_code, response.json())
    except requests.exceptions.RequestException as e:
        speak("There was a problem connecting to the server. Please try again later.")
        print("Error:", e)

# Run the main function
if __name__ == '__main__':
    main()
