# Helen – AI Assistant for the Visually Impaired

Helen is an experimental **multimodal AI assistant** designed to help visually impaired users interact with their surroundings using **voice commands, computer vision, and natural language processing**.

The project explores how multiple AI technologies can be combined into a single assistant capable of perceiving the environment, reading text, and responding conversationally.

This prototype was originally developed in **2023** as an early exploration of accessible AI systems.

---

## Problem

Many visually impaired individuals rely heavily on assistive technologies to interact with their environment. However, most existing systems either focus only on voice queries or require specialized hardware.

Helen explores a software-based approach that integrates:

* Speech interaction
* Computer vision
* Optical character recognition
* Natural language processing

The goal is to create an assistant capable of **interpreting the environment and communicating useful information through voice feedback.**

---

## Features

### Voice Interaction

Helen listens for voice commands and responds with synthesized speech.

Capabilities:

* Speech recognition
* Spoken responses
* Conversational interaction

---

### Object Detection

Using computer vision, Helen can detect objects through a camera feed and describe them.

Potential uses:

* Identifying objects in front of the user
* Understanding surroundings

---

### OCR Text Reader

Helen can capture an image and read printed text aloud using OCR.

Useful for:

* Reading documents
* Reading signs or labels

---

### Gesture-Based Music Control

Helen allows users to control music playback using hand gestures detected through the webcam.

---

### Voice Web Search

Helen can perform voice-triggered web searches and read relevant results.

---

## Technology Stack

Language:

* Python

Libraries:

Computer Vision:

* OpenCV
* MediaPipe

Natural Language Processing:

* HuggingFace Transformers

Speech Processing:

* SpeechRecognition
* pyttsx3

OCR:

* Tesseract

Other libraries:

* NumPy
* BeautifulSoup
* Requests
* Pygame

---

## Installation

Clone the repository:

```
git clone https://github.com/apexajay-rc/helen.git
cd helen
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the assistant:

```
python assistant.py
```

---

## Example Voice Commands

Examples of commands Helen can respond to:

```
"read text"
"describe objects"
"search python programming"
"play music with gestures"
```

---

## Project Structure

```
assistant.py                Main assistant controller
nlp.py                      NLP processing module
ocr.py                      Optical character recognition
object_detection.py         Object detection module
voice_search.py             Voice-triggered web search
gesture_music_control.py    Gesture-based music control
audio.py                    Speech output utilities
config.py                   Configuration settings
```

---

## Future Improvements

Possible improvements for future versions:

* Improved object detection models
* More advanced conversational AI
* Conversation memory and context awareness
* Mobile or embedded deployment
* Improved accessibility features

---

## Motivation

This project explores how AI systems can assist visually impaired individuals by providing **audio feedback about their surroundings and environment**.

Helen represents an early prototype toward building **accessible multimodal AI assistants.**

---
