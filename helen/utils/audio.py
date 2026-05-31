import json
from pathlib import Path
from threading import Lock

from utils.events import emit_event

_engine = None
_lock = Lock()
_settings_path = Path.home() / ".helen" / "voice.json"
_settings = {
    "voice_id": "",
    "rate": 158,
    "volume": 0.88,
}


def _load_settings():
    if _settings_path.exists():
        try:
            _settings.update(json.loads(_settings_path.read_text(encoding="utf-8")))
        except (OSError, ValueError, TypeError):
            pass


def _save_settings():
    _settings_path.parent.mkdir(parents=True, exist_ok=True)
    _settings_path.write_text(json.dumps(_settings, indent=2), encoding="utf-8")


def _voice_name(voice):
    return str(getattr(voice, "name", "") or getattr(voice, "id", "System voice"))


def _preferred_voice(voices):
    if _settings["voice_id"]:
        for voice in voices:
            if voice.id == _settings["voice_id"]:
                return voice

    preferred_names = ("zira", "hazel", "susan", "female")
    for name in preferred_names:
        for voice in voices:
            if name in _voice_name(voice).lower() or name in voice.id.lower():
                return voice
    return voices[0] if voices else None


def _apply_settings(engine):
    voices = engine.getProperty("voices") or []
    voice = _preferred_voice(voices)
    if voice is not None:
        engine.setProperty("voice", voice.id)
    engine.setProperty("rate", int(_settings["rate"]))
    engine.setProperty("volume", float(_settings["volume"]))


def _get_engine():
    global _engine
    if _engine is None:
        import pyttsx3

        _load_settings()
        _engine = pyttsx3.init()
        _apply_settings(_engine)
    return _engine


def list_voices():
    engine = _get_engine()
    return [
        {"id": voice.id, "name": _voice_name(voice)}
        for voice in (engine.getProperty("voices") or [])
    ]


def get_voice_settings():
    engine = _get_engine()
    voices = engine.getProperty("voices") or []
    current_id = str(engine.getProperty("voice") or "")
    current_name = next(
        (_voice_name(voice) for voice in voices if voice.id == current_id),
        "System voice",
    )
    return {
        "voice_id": current_id,
        "voice_name": current_name,
        "rate": int(_settings["rate"]),
        "volume": float(_settings["volume"]),
    }


def update_voice_settings(voice_id=None, rate=None, volume=None):
    engine = _get_engine()
    if voice_id:
        _settings["voice_id"] = voice_id
    if rate is not None:
        _settings["rate"] = max(110, min(220, int(rate)))
    if volume is not None:
        _settings["volume"] = max(0.2, min(1.0, float(volume)))
    _apply_settings(engine)
    _save_settings()
    return get_voice_settings()


def speak(text):
    if not text:
        return

    emit_event("speaking", str(text))
    with _lock:
        engine = _get_engine()
        engine.say(str(text))
        engine.runAndWait()
    emit_event("idle")
