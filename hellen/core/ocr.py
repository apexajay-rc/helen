import cv2
import pytesseract
from utils.audio import speak
from utils.config import CAMERA_INDEX

def read_text_from_image():
    cam = cv2.VideoCapture(CAMERA_INDEX)
    ok, frame = cam.read()
    cam.release()
    if not ok or frame is None:
        speak("Sorry, I could not access the camera.")
        return ""

    text = pytesseract.image_to_string(frame).strip()
    if not text:
        speak("I could not find readable text in the image.")
        return ""

    speak(f"I read: {text}")
    return text
