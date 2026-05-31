import os
import re
from difflib import SequenceMatcher

from utils.events import emit_event


INTENTS = {
    "help": {
        "label": "capability guide",
        "examples": (
            "what can you do",
            "tell me your features",
            "show me the menu",
            "help me",
            "what are my options",
        ),
        "keywords": (
            "help",
            "menu",
            "feature",
            "features",
            "capability",
            "capabilities",
            "option",
            "options",
        ),
    },
    "read_text": {
        "label": "read visible text",
        "examples": (
            "read this text",
            "scan this document",
            "read the sign in front of me",
            "can you read this label",
            "tell me what is written here",
        ),
        "keywords": (
            "read",
            "scan",
            "document",
            "text",
            "written",
            "label",
            "sign",
            "letter",
        ),
    },
    "read_screen": {
        "label": "read the current screen",
        "examples": (
            "read my screen",
            "what is on my screen",
            "read this window",
            "tell me what is displayed",
            "explain the popup on my screen",
        ),
        "keywords": (
            "screen",
            "window",
            "popup",
            "displayed",
            "desktop",
            "dialog",
        ),
    },
    "describe_objects": {
        "label": "describe surroundings",
        "examples": (
            "describe the objects around me",
            "what can you see",
            "tell me what is in front of me",
            "identify nearby objects",
            "describe my surroundings",
        ),
        "keywords": (
            "describe",
            "see",
            "object",
            "surrounding",
            "front",
            "ahead",
            "nearby",
            "around",
            "identify",
        ),
    },
    "play_music": {
        "label": "play music with gesture control",
        "examples": (
            "play music",
            "i want to listen to music right now",
            "start a song",
            "put on some music",
            "open gesture music control",
        ),
        "keywords": ("music", "song", "songs", "tune", "tunes", "listen", "audio", "gesture", "play"),
    },
    "web_search": {
        "label": "search the web",
        "examples": (
            "search the web",
            "look this up online",
            "google artificial intelligence",
            "find information about accessibility",
            "search for python programming",
        ),
        "keywords": (
            "search",
            "google",
            "online",
            "web",
            "lookup",
            "look",
            "find",
            "information",
        ),
    },
    "quit": {
        "label": "exit Helen",
        "examples": (
            "quit",
            "exit the assistant",
            "close helen",
            "goodbye",
            "stop listening",
        ),
        "keywords": ("quit", "exit", "close", "goodbye"),
    },
}

CAPABILITY_GUIDE = (
    "Here is what I can do. "
    "I can read visible text from documents, signs, or labels. "
    "I can read text from your computer screen. "
    "I can describe objects in front of you. "
    "I can search the web for information. "
    "I can start gesture controlled music. "
    "You can ask in your own words. "
    "For example, say: read this label, read my screen, what can you see, "
    "look up assistive technology, or I want to listen to music. "
    "Say help at any time to hear these options again."
)

_classifier = None
_classifier_unavailable = False


def normalize(text):
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def _rule_score(command, examples, keywords):
    words = set(command.split())
    keyword_hits = sum(keyword in words for keyword in keywords)
    keyword_score = min(0.9, keyword_hits * 0.62)
    phrase_score = max(
        SequenceMatcher(None, command, normalize(example)).ratio()
        for example in examples
    )
    return max(keyword_score, phrase_score)


def _classify_with_transformers(command):
    global _classifier, _classifier_unavailable
    if os.getenv("HELEN_ENABLE_SEMANTIC_INTENTS", "0") != "1":
        return None, 0.0
    if _classifier_unavailable:
        return None, 0.0

    try:
        if _classifier is None:
            from transformers import pipeline

            emit_event("processing", "Loading semantic intent model...")
            _classifier = pipeline(
                "zero-shot-classification",
                model="typeform/distilbert-base-uncased-mnli",
            )
        labels = [config["label"] for config in INTENTS.values()]
        result = _classifier(command, labels)
        label = result["labels"][0]
        score = float(result["scores"][0])
        intent = next(
            name for name, config in INTENTS.items() if config["label"] == label
        )
        return intent, score
    except Exception:
        _classifier_unavailable = True
        return None, 0.0


def classify_intent(text):
    command = normalize(text)
    if not command:
        return "unknown", 0.0

    scored = [
        (
            name,
            _rule_score(command, config["examples"], config["keywords"]),
        )
        for name, config in INTENTS.items()
    ]
    best_intent, best_score = max(scored, key=lambda item: item[1])
    if best_score >= 0.5:
        return best_intent, best_score

    semantic_intent, semantic_score = _classify_with_transformers(command)
    if semantic_intent and semantic_score >= 0.42:
        return semantic_intent, semantic_score
    return "conversation", best_score


def extract_search_query(text):
    query = normalize(text)
    patterns = (
        r"^(?:please\s+|can you\s+|could you\s+|i want you to\s+)*search the web for\s+",
        r"^(?:please\s+|can you\s+|could you\s+|i want you to\s+)*search online for\s+",
        r"^(?:please\s+|can you\s+|could you\s+|i want you to\s+)*search for\s+",
        r"^(?:please\s+|can you\s+|could you\s+|i want you to\s+)*look this up\s+",
        r"^(?:please\s+|can you\s+|could you\s+|i want you to\s+)*look up\s+",
        r"^(?:please\s+|can you\s+|could you\s+|i want you to\s+)*google\s+",
        r"^(?:please\s+|can you\s+|could you\s+|i want you to\s+)*find information about\s+",
        r"^(?:please\s+|can you\s+|could you\s+|i want you to\s+)*find\s+",
        r"^(?:please\s+|can you\s+|could you\s+|i want you to\s+)*search\s+",
    )
    for pattern in patterns:
        cleaned = re.sub(pattern, "", query)
        if cleaned != query:
            return cleaned.strip()
    return query
