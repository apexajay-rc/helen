import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "helen"))

from core.wake_word import OfflineWakeWordDetector


class WakePhraseTests(unittest.TestCase):
    def test_detects_supported_wake_phrases(self):
        for phrase in ("helen", "hey helen", "hello helen"):
            with self.subTest(phrase=phrase):
                self.assertTrue(OfflineWakeWordDetector._contains_wake_word(phrase))

    def test_ignores_unrelated_speech(self):
        self.assertFalse(
            OfflineWakeWordDetector._contains_wake_word("read my screen")
        )


if __name__ == "__main__":
    unittest.main()
