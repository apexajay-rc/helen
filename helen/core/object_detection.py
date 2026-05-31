import cv2
from utils.audio import speak
from utils.config import (
    CAMERA_INDEX,
    OBJECT_CONFIDENCE_THRESHOLD,
    OBJECT_MODEL_CONFIG,
    OBJECT_MODEL_WEIGHTS,
)

COCO_LABELS = {
    1: "person",
    2: "bicycle",
    3: "car",
    4: "motorcycle",
    5: "airplane",
    6: "bus",
    7: "train",
    8: "truck",
    9: "boat",
    10: "traffic light",
    11: "fire hydrant",
    13: "stop sign",
    14: "parking meter",
    15: "bench",
    16: "bird",
    17: "cat",
    18: "dog",
    19: "horse",
    20: "sheep",
    21: "cow",
    22: "elephant",
    23: "bear",
    24: "zebra",
    25: "giraffe",
    27: "backpack",
    28: "umbrella",
    31: "handbag",
    32: "tie",
    33: "suitcase",
    34: "frisbee",
    35: "skis",
    36: "snowboard",
    37: "sports ball",
    38: "kite",
    39: "baseball bat",
    40: "baseball glove",
    41: "skateboard",
    42: "surfboard",
    43: "tennis racket",
    44: "bottle",
    46: "wine glass",
    47: "cup",
    48: "fork",
    49: "knife",
    50: "spoon",
    51: "bowl",
    52: "banana",
    53: "apple",
    54: "sandwich",
    55: "orange",
    56: "broccoli",
    57: "carrot",
    58: "hot dog",
    59: "pizza",
    60: "donut",
    61: "cake",
    62: "chair",
    63: "couch",
    64: "potted plant",
    65: "bed",
    67: "dining table",
    70: "toilet",
    72: "tv",
    73: "laptop",
    74: "mouse",
    75: "remote",
    76: "keyboard",
    77: "cell phone",
    78: "microwave",
    79: "oven",
    80: "toaster",
    81: "sink",
    82: "refrigerator",
    84: "book",
    85: "clock",
    86: "vase",
    87: "scissors",
    88: "teddy bear",
    89: "hair dryer",
    90: "toothbrush",
}

def detect_objects():
    if not OBJECT_MODEL_WEIGHTS.exists() or not OBJECT_MODEL_CONFIG.exists():
        speak(
            "Object detection model files are missing. "
            "Please run python setup_models.py first."
        )
        return []

    model = cv2.dnn_DetectionModel(
        str(OBJECT_MODEL_WEIGHTS),
        str(OBJECT_MODEL_CONFIG),
    )
    model.setInputSize(320, 320)
    model.setInputScale(1.0 / 127.5)
    model.setInputMean((127.5, 127.5, 127.5))
    model.setInputSwapRB(True)

    cam = cv2.VideoCapture(CAMERA_INDEX)
    ok, frame = False, None
    for _ in range(5):
        ok, frame = cam.read()
    cam.release()
    if not ok or frame is None:
        speak("Sorry, I could not access the camera.")
        return []

    detected = []
    class_ids, confidences, _ = model.detect(
        frame,
        confThreshold=OBJECT_CONFIDENCE_THRESHOLD,
    )
    for class_id, confidence in zip(class_ids, confidences):
        if float(confidence) > OBJECT_CONFIDENCE_THRESHOLD:
            idx = int(class_id)
            detected.append(COCO_LABELS.get(idx, f"object {idx}"))

    unique_objects = sorted(set(detected))
    if not unique_objects:
        speak("I did not detect any familiar objects.")
    elif len(unique_objects) == 1:
        speak(f"I see a {unique_objects[0]}.")
    else:
        speak("I see " + ", ".join(unique_objects[:5]) + ".")

    return unique_objects
