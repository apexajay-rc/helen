import json
import logging

from utils.config import VOSK_WAKE_MODEL


WAKE_PHRASES = ("helen", "hey helen", "hello helen")


class OfflineWakeWordDetector:
    def __init__(self, sample_rate):
        if not VOSK_WAKE_MODEL.exists():
            raise FileNotFoundError(
                "Offline wake-word model is missing. Run python setup_models.py."
            )

        logging.getLogger("vosk").setLevel(logging.ERROR)
        from vosk import KaldiRecognizer, Model, SetLogLevel

        SetLogLevel(-1)
        grammar = json.dumps([*WAKE_PHRASES, "[unk]"])
        self._recognizer = KaldiRecognizer(
            Model(str(VOSK_WAKE_MODEL)),
            sample_rate,
            grammar,
        )

    @staticmethod
    def _contains_wake_word(text):
        normalized = " ".join(text.lower().split())
        return any(phrase in normalized for phrase in WAKE_PHRASES)

    def process(self, audio_bytes):
        if self._recognizer.AcceptWaveform(audio_bytes):
            text = json.loads(self._recognizer.Result()).get("text", "")
            return self._contains_wake_word(text)

        partial = json.loads(self._recognizer.PartialResult()).get("partial", "")
        return self._contains_wake_word(partial)

    def reset(self):
        self._recognizer.Reset()
