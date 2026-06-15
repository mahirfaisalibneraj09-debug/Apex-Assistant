import sys
import subprocess
import spacy
import os
import pyautogui
# Your App Registry
app_paths = {
    "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "notepad": r"C:\Windows\System32\notepad.exe",
    "calculator": "calc.exe"}
nlp = spacy.load("en_core_web_sm")
# FIX: Prevents sounddevice from poisoning Windows console handles
if sys.platform == "win32":
    original_popen_init = subprocess.Popen.__init__
    def patched_popen_init(self, *args, **kwargs):
        if kwargs.get('stdin') is None:
            kwargs['stdin'] = subprocess.DEVNULL
        if kwargs.get('stdout') is None:
            kwargs['stdout'] = subprocess.PIPE
        if kwargs.get('stderr') is None:
            kwargs['stderr'] = subprocess.PIPE
        original_popen_init(self, *args, **kwargs)
    subprocess.Popen.__init__ = patched_popen_init
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import webbrowser
import urllib.parse
from pytube import Search
import pyttsx3
import logging
logging.getLogger("pytube").setLevel(logging.CRITICAL)
engine = pyttsx3.init()
engine.say("Testing, one, two, three.")
engine.runAndWait()
def main():
    ask_question()
    print("Speak something....")
    speech_01=speech()
    if not speech_01:
        speech_01=input("Sorry, I didn't catch that. Could you please type your command? ")
    print(f"Your messege was: {speech_01}")
    if "volume" in speech_01:
        try:
            volume_change=set_volume(speech_01)
            #will increase 25%percent if possible
            if volume_change==.25:
                for i in range(5):
                    pyautogui.press('volumeup')
            #will decrease 25%percent if possible
            elif volume_change==-.25:
                for i in range(5):
                    pyautogui.press('volumedown')
            else:
                print("what are u saying, man? we cant do it is already how you want it to be")
        except:
            print("wrong command")
    elif "open" in command_01 and "youtube" not in command_01:
        success=opening_app(speech_01)
        if not success:
            print("app not found")
    else:
        command_01=command_to_search(speech_01)
        if command_01.startswith("Caught either UnknownValueError or RequestError:"):
            sys.exit("Sorry we can't proceed")
        play_on_yt(command_01)
def opening_app(app):
    for app_name in app_paths:
        if app_name in app:
            try:
                os.startfile(app_paths[app_name])
                print(f"Opening {app_name}...")
                return True
            except FileNotFoundError:
                print(f"Error: Could not find the file for {app_name}")
                return False
    return False
def ask_question():
    engine= pyttsx3.init()
    engine.say("Hey, My name is Mahir... How can i help you?")
    engine.runAndWait()
def set_volume(sound):
    
    sound_decrease=["decrease", "lower", "quieter", "down"]
    sound_increase= ["increase", "higher", "louder", "up"]
    for word in sound_decrease:
        if word in sound:
            return 0.25
    for word in sound_increase:
        if word in sound:
            return -0.25
    return 0
def speech():
    # Initialize the recognizer
    r = sr.Recognizer()
  # Falls back to system default if index query fails

    # Audio recording parameters
    sample_rate = 48000  # Standard for speech recognition
    duration = 5       # Record for 5 seconds

    # Record audio from the default microphone
    # sounddevice records as a numpy array; we convert it to bytes
    # Change device=1 to match your Microphone ID
    # Get the default input device information
    try:
        default_device = sd.default.device[0]  # Gets the default index
    except Exception:
        default_device = None  # Falls back to system default if index query fails
        
    print(f"Using microphone index: {default_device}")

    # Record using the dynamic device index
    audio_data = sd.rec(
        int(duration * sample_rate), 
        samplerate=sample_rate, 
        channels=1, 
        dtype='int16', 
        device=default_device
    )
    sd.wait() # Wait for recording to finish

    # Convert numpy array to bytes compatible with speech_recognition
    audio_bytes = audio_data.tobytes()

    # Create an AudioData object manually
    audio = sr.AudioData(audio_bytes, sample_rate, 2) # 2 bytes per sample for int16

    try:
        # Convert speech to text
        text = r.recognize_google(audio)
        return text
    except (sr.RequestError, sr.UnknownValueError) as e:
        return f"Caught either UnknownValueError or RequestError: {e}"
        
def command_to_search(m):
    words_to_remove = [ "open youtube and play", "play", "please", "please play"]
    doc = nlp(m)
    m_01 = m.lower()
    # This checks if any word in the list exists inside the user string
    if any(word in m_01 for word in words_to_remove):
        for word in words_to_remove:
            if word in m_01:
                m_01 = m_01.replace(word, "").strip()
    elif doc.ents:
    # 3. Fallback: If no 'play' verb, just return entities or the whole string
        m_01 = doc.ents[0].text
    return m_01
def play_on_yt(r):
    s = Search(r)
    i=0
    print("Here are your recomendations: ")
    while i<5:
        video = s.results[i]
        print(f"{i+1}. {video.title}")
        i+=1
    engine= pyttsx3.init()
    engine.say("which one will u prefer to play? ")
    engine.runAndWait()
    try:
        number = int(input("which one will u prefer to play? "))
        first_video = s.results[number-1]
    except (ValueError, IndexError):
        print("Invalid choice, defaulting to the first video.")
        first_video = s.results[0]
    watch_url = first_video.watch_url

    # 4. Open it instantly in your browser!
    print(f"Playing video: {first_video.title}")
    webbrowser.open(watch_url)

if __name__ == "__main__":
    main()
