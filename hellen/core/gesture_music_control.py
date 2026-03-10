import cv2
import mediapipe as mp
import pygame
import os
from utils.audio import speak

def start_gesture_control():
    speak("Starting gesture-based music control...")
    mp_hands = mp.solutions.hands.Hands()
    pygame.mixer.init()
    music_files = [f for f in os.listdir("data/songs") if f.endswith(".mp3")]
    song_idx = 0
    pygame.mixer.music.load(f"data/songs/{music_files[song_idx]}")
    pygame.mixer.music.play()

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        results = mp_hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            song_idx = (song_idx + 1) % len(music_files)
            pygame.mixer.music.load(f"data/songs/{music_files[song_idx]}")
            pygame.mixer.music.play()
            speak(f"Switched to {music_files[song_idx]}")
            break
    cap.release()
