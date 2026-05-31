import cv2
from utils.audio import speak
from utils.config import CAMERA_INDEX, SONGS_DIR

def start_gesture_control():
    import os

    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    import mediapipe as mp
    import pygame

    speak("Starting gesture-based music control...")
    if not hasattr(mp, "solutions"):
        speak(
            "Gesture control is not available with this MediaPipe build. "
            "The module needs to be upgraded to the new hand landmarker model."
        )
        return

    mp_hands = mp.solutions.hands.Hands()
    pygame.mixer.init()
    music_files = sorted(SONGS_DIR.glob("*.mp3"))
    if not music_files:
        speak("I could not find any songs to play.")
        return

    song_idx = 0
    pygame.mixer.music.load(str(music_files[song_idx]))
    pygame.mixer.music.play()

    cap = cv2.VideoCapture(CAMERA_INDEX)
    frames_checked = 0
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            speak("Sorry, I could not access the camera.")
            break

        frames_checked += 1
        results = mp_hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            song_idx = (song_idx + 1) % len(music_files)
            pygame.mixer.music.load(str(music_files[song_idx]))
            pygame.mixer.music.play()
            speak(f"Switched to {music_files[song_idx].name}")
            break
        if frames_checked > 300:
            speak("I did not detect a hand gesture.")
            break
    cap.release()
