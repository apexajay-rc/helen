import cv2
import numpy as np
from utils.audio import speak

def detect_objects():
    net = cv2.dnn.readNet("https://github.com/opencv/opencv/blob/master/samples/dnn/ssd_mobilenet_v1_coco.pb?raw=true",
                          "https://github.com/opencv/opencv/blob/master/samples/dnn/ssd_mobilenet_v1_coco.pbtxt?raw=true")
    cam = cv2.VideoCapture(0)
    _, frame = cam.read()
    cam.release()

    blob = cv2.dnn.blobFromImage(frame, size=(300, 300), swapRB=True)
    net.setInput(blob)
    output = net.forward()

    for detection in output[0, 0]:
        confidence = detection[2]
        if confidence > 0.6:
            idx = int(detection[1])
            speak(f"I see object {idx}")
            break
