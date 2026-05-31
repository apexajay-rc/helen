from threading import Lock

_listener = None
_lock = Lock()


def set_event_listener(listener):
    global _listener
    with _lock:
        _listener = listener


def emit_event(state, message=""):
    with _lock:
        listener = _listener
    if listener is not None:
        listener(state, message)
