import cv2
import pytesseract
from utils.audio import speak

def read_text_from_image():
    cam = cv2.VideoCapture(0)
    _, frame = cam.read()
    cam.release()
    cv2.imwrite("temp.png", frame)
    text = pytesseract.image_to_string("temp.png")
    speak(f"I read: {text}")
