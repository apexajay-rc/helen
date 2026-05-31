from threading import Lock

from utils.events import emit_event

_engine = None
_lock = Lock()


def _get_engine():
    global _engine
    if _engine is None:
        import pyttsx3

        _engine = pyttsx3.init()
    return _engine

def speak(text):
    if not text:
        return

    emit_event("speaking", str(text))
    with _lock:
        engine = _get_engine()
        engine.say(str(text))
        engine.runAndWait()
    emit_event("idle", "Ready")
