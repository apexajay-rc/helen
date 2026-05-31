import os
import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "helen"))
os.environ["HELEN_ENABLE_SEMANTIC_INTENTS"] = "0"

from core.intents import classify_intent, extract_search_query


class IntentClassificationTests(unittest.TestCase):
    def test_understands_natural_paraphrases(self):
        cases = {
            "I want to listen to music right now": "play_music",
            "Could you read this medicine label for me": "read_text",
            "Please read what is on my computer screen": "read_screen",
            "Explain this popup on my screen": "read_screen",
            "Is there anything ahead of me": "describe_objects",
            "Tell me your features": "help",
            "Goodbye Helen": "quit",
        }
        for command, expected in cases.items():
            with self.subTest(command=command):
                intent, _ = classify_intent(command)
                self.assertEqual(intent, expected)

    def test_extracts_polite_search_query(self):
        self.assertEqual(
            extract_search_query("Please look up affordable smart glasses online"),
            "affordable smart glasses online",
        )


if __name__ == "__main__":
    unittest.main()
