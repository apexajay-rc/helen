import argparse
import re
import time

import speech_recognition as sr

from assistant import route_command
from utils.audio import speak
from utils.events import emit_event


WAKE_WORDS = ("helen", "hey helen", "hello helen")


def _strip_wake_phrase(text):
    command = text.strip()
    for wake in sorted(WAKE_WORDS, key=len, reverse=True):
        pattern = rf"^\s*{re.escape(wake)}[\s,.:;-]*(.*)$"
        match = re.match(pattern, command, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def _recognize(recognizer, audio):
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        emit_event("idle", "Speech recognition service is unavailable.")
        return ""


def _listen_once(recognizer, source, timeout=None, phrase_time_limit=5):
    try:
        audio = recognizer.listen(
            source,
            timeout=timeout,
            phrase_time_limit=phrase_time_limit,
        )
    except sr.WaitTimeoutError:
        return ""
    return _recognize(recognizer, audio)


def run_daemon(acknowledge=True):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        emit_event("idle", "Helen is listening quietly in the background.")
        print("Helen daemon is running. Say 'Helen' followed by a command.")
        while True:
            heard = _listen_once(
                recognizer,
                source,
                timeout=None,
                phrase_time_limit=4,
            )
            if not heard:
                continue

            command = _strip_wake_phrase(heard)
            if command is None:
                continue

            print(f"Wake command: {command}")
            emit_event("processing", f'Wake command: "{command}"')
            if acknowledge:
                speak("Yes?")
                time.sleep(0.1)
            if not command:
                command = _listen_once(
                    recognizer,
                    source,
                    timeout=5,
                    phrase_time_limit=8,
                )
            if command:
                route_command(command)


def main():
    parser = argparse.ArgumentParser(description="Run Helen as a quiet wake-word daemon.")
    parser.add_argument(
        "--no-ack",
        action="store_true",
        help="Do not speak a short acknowledgement after the wake word.",
    )
    args = parser.parse_args()
    run_daemon(acknowledge=not args.no_ack)


if __name__ == "__main__":
    main()
