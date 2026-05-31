from pathlib import Path

import pytesseract

from utils.audio import speak


def _configure_tesseract():
    common_windows_paths = (
        Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
        Path(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"),
    )
    for path in common_windows_paths:
        if path.exists():
            pytesseract.pytesseract.tesseract_cmd = str(path)
            break


def read_screen():
    _configure_tesseract()
    try:
        from PIL import ImageGrab

        screenshot = ImageGrab.grab(all_screens=True)
        text = pytesseract.image_to_string(screenshot).strip()
    except pytesseract.TesseractNotFoundError:
        speak("Tesseract OCR is not installed or is not available on your path.")
        return ""
    except Exception:
        speak("Sorry, I could not capture your screen on this system.")
        return ""

    if not text:
        speak("I could not find readable text on your screen.")
        return ""

    spoken_text = text[:1600]
    speak(f"I found this on your screen. {spoken_text}")
    return spoken_text
