import keyboard
import webbrowser

# Function to open the website
def open_website():
    url = "http://127.0.0.1:5500/template/fp.html"  # Replace with the desired website URL
    webbrowser.open(url)
    print(f"Opened {url}")

# Detect 'Shift + A' as a hotkey
keyboard.add_hotkey('shift+a', open_website)

# Keep the program running
print("Press Shift + A to open the website.")
keyboard.wait('esc')  # Program ends when 'esc' is pressed
