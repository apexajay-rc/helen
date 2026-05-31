import cv2
import pytesseract
from pathlib import Path
from utils.audio import speak
from utils.config import CAMERA_INDEX


def _configure_tesseract():
    common_windows_paths = (
        Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
        Path(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"),
    )
    for path in common_windows_paths:
        if path.exists():
            pytesseract.pytesseract.tesseract_cmd = str(path)
            break


def read_text_from_image():
    _configure_tesseract()
    cam = cv2.VideoCapture(CAMERA_INDEX)
    ok, frame = False, None
    for _ in range(5):
        ok, frame = cam.read()
    cam.release()
    if not ok or frame is None:
        speak("Sorry, I could not access the camera.")
        return ""

    try:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(rgb_frame).strip()
    except pytesseract.TesseractNotFoundError:
        speak(
            "Tesseract OCR is not installed or is not available on your path."
        )
        return ""
    if not text:
        speak("I could not find readable text in the image.")
        return ""

    speak(f"I read: {text}")
    return text
