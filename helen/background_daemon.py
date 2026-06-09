import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import speech_recognition as sr

from assistant import route_command
from core.wake_word import OfflineWakeWordDetector
from setup_models import download_vosk_model
from utils.audio import speak
from utils.events import emit_event

STATUS_PATH = Path.home() / ".helen" / "daemon_status.json"


def _write_status(state, detail=""):
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATUS_PATH.write_text(
        json.dumps(
            {
                "pid": os.getpid(),
                "state": state,
                "detail": detail,
                "wake_detection": "offline_vosk",
                "updated_at": datetime.now(timezone.utc).isoformat(),
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def _recognize_command(recognizer, audio):
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        speak("I did not understand the command.")
        return ""
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""


def _listen_for_command(recognizer, source):
    try:
        audio = recognizer.listen(
            source,
            timeout=5,
            phrase_time_limit=10,
        )
    except sr.WaitTimeoutError:
        speak("I did not hear a command.")
        return ""
    return _recognize_command(recognizer, audio)


def run_daemon(acknowledge=True):
    _write_status("starting", "Preparing offline wake-word model.")
    download_vosk_model()
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        detector = OfflineWakeWordDetector(source.SAMPLE_RATE)
        emit_event("idle", "Helen is listening locally for the wake word.")
        _write_status("listening", "Waiting locally for the wake word Helen.")
        print("Helen is listening locally. Say 'Helen' to wake it.")
        last_heartbeat = time.monotonic()

        while True:
            audio_bytes = source.stream.read(source.CHUNK)
            if time.monotonic() - last_heartbeat >= 5:
                _write_status(
                    "listening",
                    "Waiting locally for the wake word Helen.",
                )
                last_heartbeat = time.monotonic()
            if not detector.process(audio_bytes):
                continue

            detector.reset()
            emit_event("listening", "Wake word detected. Listening for a command.")
            _write_status("awake", "Wake word detected. Listening for command.")
            if acknowledge:
                speak("Yes?")
            command = _listen_for_command(recognizer, source)
            if command:
                emit_event("processing", f'Wake command: "{command}"')
                _write_status("processing", command)
                route_command(command)
            _write_status("listening", "Waiting locally for the wake word Helen.")
            time.sleep(0.4)


def main():
    parser = argparse.ArgumentParser(
        description="Run Helen with local offline wake-word detection."
    )
    parser.add_argument(
        "--no-ack",
        action="store_true",
        help="Do not speak after detecting the wake word.",
    )
    args = parser.parse_args()
    run_daemon(acknowledge=not args.no_ack)


if __name__ == "__main__":
    main()
