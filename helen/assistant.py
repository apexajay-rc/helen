import speech_recognition as sr
from utils.audio import speak
from utils.events import emit_event
from core.nlp import process_nlp
from core.ocr import read_text_from_image
from core.object_detection import detect_objects
from core.gesture_music_control import start_gesture_control
from core.voice_search import search_web
from core.screen_reader import read_screen
from core.intents import CAPABILITY_GUIDE, INTENTS, classify_intent, extract_search_query


def announce_capabilities():
    emit_event("guide", CAPABILITY_GUIDE)
    speak(CAPABILITY_GUIDE)

def route_command(command):
    command = command.strip()
    if not command:
        return

    intent, confidence = classify_intent(command)
    intent_label = INTENTS.get(intent, {}).get("label", "conversation")
    emit_event(
        "processing",
        f'You said: "{command}"\nDetected intent: {intent_label}',
    )
    print(f"Detected intent: {intent_label} ({confidence:.0%})")

    if intent == "help":
        announce_capabilities()
    elif intent == "quit":
        speak("Goodbye!")
        raise KeyboardInterrupt
    elif intent == "read_text":
        read_text_from_image()
    elif intent == "read_screen":
        read_screen()
    elif intent == "describe_objects":
        detect_objects()
    elif intent == "play_music":
        start_gesture_control()
    elif intent == "web_search":
        query = extract_search_query(command)
        search_web(query)
    else:
        process_nlp(command)

def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            emit_event("listening", "Listening...")
            print("\nListening... Speak a command.")
            r.adjust_for_ambient_noise(source, duration=0.6)
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
    except sr.WaitTimeoutError:
        print("No speech detected.")
        speak("I did not hear anything. Please try again.")
        return ""
    except (OSError, AttributeError):
        print("Microphone unavailable.")
        speak("Sorry, I could not access the microphone.")
        return ""

    try:
        print("Recognizing speech...")
        command = r.recognize_google(audio)
        print(f"You said: {command}")
        emit_event("processing", command)
        return command
    except sr.UnknownValueError:
        print("Speech was captured, but it could not be understood.")
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Google speech recognition service is unavailable.")
        speak("Sorry, speech service is unavailable.")
        return ""

def main():
    speak("Hello, I'm Helen. How can I assist you today?")
    announce_capabilities()
    print("Helen is ready. Say 'quit' to exit.")
    try:
        while True:
            route_command(listen())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
