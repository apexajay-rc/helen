import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "helen"))

from background_daemon import _strip_wake_phrase


class WakePhraseTests(unittest.TestCase):
    def test_extracts_command_after_wake_phrase(self):
        self.assertEqual(
            _strip_wake_phrase("Helen, read my screen"),
            "read my screen",
        )

    def test_detects_wake_word_without_command(self):
        self.assertEqual(_strip_wake_phrase("Helen"), "")

    def test_ignores_speech_without_wake_word(self):
        self.assertIsNone(_strip_wake_phrase("read my screen"))


if __name__ == "__main__":
    unittest.main()
