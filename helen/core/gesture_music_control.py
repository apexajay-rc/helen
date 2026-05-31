import cv2
from utils.audio import speak
from utils.config import CAMERA_INDEX, HAND_LANDMARKER_MODEL, SONGS_DIR


def _legacy_hand_detector(mp):
    detector = mp.solutions.hands.Hands()

    def has_hand(frame):
        results = detector.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return bool(results.multi_hand_landmarks)

    return detector, has_hand


def _task_hand_detector(mp):
    if not HAND_LANDMARKER_MODEL.exists():
        speak(
            "The hand tracking model is missing. "
            "Please run python setup_models.py first."
        )
        return None, None

    options = mp.tasks.vision.HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(
            model_asset_path=str(HAND_LANDMARKER_MODEL)
        ),
        running_mode=mp.tasks.vision.RunningMode.IMAGE,
        num_hands=1,
    )
    detector = mp.tasks.vision.HandLandmarker.create_from_options(options)

    def has_hand(frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        result = detector.detect(image)
        return bool(result.hand_landmarks)

    return detector, has_hand

def start_gesture_control():
    import os
    import warnings

    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    warnings.filterwarnings(
        "ignore",
        message="pkg_resources is deprecated as an API.*",
        category=UserWarning,
    )
    import mediapipe as mp
    import pygame

    speak("Starting gesture-based music control...")
    if hasattr(mp, "solutions"):
        detector, has_hand = _legacy_hand_detector(mp)
    else:
        detector, has_hand = _task_hand_detector(mp)
    if detector is None:
        return

    try:
        pygame.mixer.init()
    except pygame.error:
        detector.close()
        speak("Sorry, I could not access the audio output.")
        return

    music_files = sorted(SONGS_DIR.glob("*.mp3"))
    if not music_files:
        detector.close()
        speak("I could not find any songs to play.")
        return

    song_idx = 0
    pygame.mixer.music.load(str(music_files[song_idx]))
    pygame.mixer.music.play()
    speak(f"Playing {music_files[song_idx].name}. Raise your hand to switch songs.")

    cap = cv2.VideoCapture(CAMERA_INDEX)
    frames_checked = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                speak("Sorry, I could not access the camera.")
                break

            frames_checked += 1
            if has_hand(frame):
                song_idx = (song_idx + 1) % len(music_files)
                pygame.mixer.music.load(str(music_files[song_idx]))
                pygame.mixer.music.play()
                speak(f"Switched to {music_files[song_idx].name}")
                break
            if frames_checked > 300:
                speak("I did not detect a hand gesture.")
                break
    finally:
        cap.release()
        detector.close()
