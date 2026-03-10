import speech_recognition as sr
from utils.audio import speak
from core.nlp import process_nlp
from core.ocr import read_text_from_image
from core.object_detection import detect_objects
from core.gesture_music_control import start_gesture_control
from core.voice_search import search_web

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I'm listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Sorry, speech service is unavailable.")
        return ""

def main():
    speak("Hello, I'm Hellen. How can I assist you today?")
    while True:
        command = listen().lower()
        if "read" in command:
            read_text_from_image()
        elif "describe" in command or "object" in command:
            detect_objects()
        elif "music" in command or "gesture" in command:
            start_gesture_control()
        elif "search" in command:
            search_web()
        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break
        else:
            process_nlp(command)

if __name__ == "__main__":
    main()
