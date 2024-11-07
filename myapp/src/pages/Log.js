import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
    const [message, setMessage] = useState('Welcome to the audio interactive login and signup system.');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [step, setStep] = useState(1); // Step 1: email prompt, Step 2: password prompt
    const [isProcessing, setIsProcessing] = useState(false);

    useEffect(() => {
        if (step <= 2) {
            promptUser();
        }
    }, [step]);

    const speak = (text, callback) => {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.onend = callback;  // Trigger callback once the speech ends
        window.speechSynthesis.speak(utterance);
    };

    const promptUser = () => {
        if (step === 1) {
            setMessage("Please say your email address.");
            speak("Please say your email address.", () => {
                setTimeout(() => listenForInput(setEmail), 2000); // Start listening after 2-second delay
            });
        } else if (step === 2) {
            setMessage("Please say your password.");
            speak("Please say your password.", () => {
                setTimeout(() => listenForInput(setPassword), 2000); // Start listening after 2-second delay
            });
        }
    };

    const listenForInput = (setInput) => {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        let isFinished = false;

        recognition.onstart = () => console.log("Voice recognition started...");
        
        recognition.onresult = (event) => {
            if (isFinished) return;  // Prevent further processing after timeout

            const text = event.results[0][0].transcript;
            const processedText = text
                .replace(/\bat\b/g, '@')     // Replace 'at' with '@'
                .replace(/\bdot\b/g, '.')    // Replace 'dot' with '.'
                .trim();

            setInput(processedText);
            setMessage(`You said: ${processedText}`);
            isFinished = true;

            if (step === 1) {
                setStep(2); // Move to the password step
            } else if (step === 2) {
                handleSubmit(); // Submit after getting password
            }

            recognition.stop();  // Stop recognition after result is received
        };

        recognition.onerror = () => {
            setMessage("Sorry, I didn't catch that. Please try again.");
            speak("Sorry, I didn't catch that. Please try again.", () => listenForInput(setInput));
        };

        recognition.start();

        // Set a 20-second timeout to stop listening if no result
        setTimeout(() => {
            if (!isFinished) {
                setMessage("Time expired. Please try again.");
                speak("Time expired. Please try again.", () => promptUser()); // Restart the prompt if time expires
                recognition.stop();  // Stop recognition after timeout
            }
        }, 20000);  // 20 seconds
    };

    const handleSubmit = async () => {
        setIsProcessing(true);
        setMessage("Processing, please wait...");
        speak("Processing, please wait...");

        const data = { mail: email, password: password };
        const url = 'http://localhost:5000/login'; // Change to '/signup' for signup

        try {
            const response = await axios.post(url, data);
            if (response.data.message === 'Login successful') {
                setMessage('Welcome to the platform!');
                speak("Welcome to the platform!");
            } else if (response.data.message === 'Signup successful') {
                setMessage("Your signup was successful.");
                speak("Your signup was successful.");
            } else {
                setMessage("Invalid email or password. Please try again.");
                speak("Invalid email or password. Please try again.");
            }
        } catch (error) {
            setMessage("An error occurred. Please try again later.");
            speak("An error occurred. Please try again later.");
        } finally {
            setIsProcessing(false);
            setStep(1); // Reset the flow for future use
        }
    };

    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <h1>Voice Interactive System</h1>
            <p>{message}</p>
            {isProcessing && <p>Processing...</p>}
        </div>
    );
}

export default App;
