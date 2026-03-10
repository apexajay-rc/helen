# Helen – System Architecture

This document describes the internal architecture of Helen and how different modules interact to process user commands.

---

## High-Level Architecture

Helen follows a modular architecture where the assistant listens for voice commands, interprets the request, and routes it to the appropriate AI module.

```
User Voice Input
        ↓
Speech Recognition
        ↓
Command Processing (assistant.py)
        ↓
┌────────────────────────────┐
│   AI Processing Modules    │
│                            │
│   • OCR Module             │
│   • Object Detection       │
│   • NLP Conversation       │
│   • Web Search             │
│   • Gesture Music Control  │
└────────────────────────────┘
        ↓
Speech Output (Text-to-Speech)
```

---

## Core Components

### 1. Speech Recognition

The assistant listens for voice commands using the SpeechRecognition library.

Responsibilities:

* Capture microphone input
* Convert speech into text
* Pass commands to the assistant controller

---

### 2. Command Router (assistant.py)

The assistant controller acts as the central router for the system.

Responsibilities:

* Interpret user commands
* Determine which module should handle the request
* Trigger the appropriate module

Example routing logic:

```
User Command → Module

"read text" → OCR Module
"describe objects" → Object Detection
"search ..." → Web Search
"play music" → Gesture Music Control
other queries → NLP Module
```

---

### 3. OCR Module

File: `ocr.py`

This module captures an image using the webcam and extracts text using Tesseract OCR.

Workflow:

1. Capture image from camera
2. Process image using pytesseract
3. Extract text
4. Speak the detected text

---

### 4. Object Detection Module

File: `object_detection.py`

This module uses OpenCV’s deep learning framework to detect objects in the environment.

Workflow:

1. Capture camera frame
2. Run object detection model
3. Identify detected object
4. Speak the result

---

### 5. NLP Module

File: `nlp.py`

Handles conversational interactions with the assistant.

Capabilities:

* Question answering
* Simple conversational responses

Implemented using the HuggingFace Transformers pipeline.

---

### 6. Voice Web Search

File: `voice_search.py`

Allows users to search the web using voice commands.

Workflow:

1. Receive search query
2. Send HTTP request to search engine
3. Parse result using BeautifulSoup
4. Speak summarized result

---

### 7. Gesture Music Control

File: `gesture_music_control.py`

Allows users to control music playback using hand gestures.

Uses:

* MediaPipe for hand tracking
* OpenCV for video capture
* Pygame for music playback

---

### 8. Speech Output

File: `audio.py`

Handles all spoken responses using text-to-speech.

Library used:

* pyttsx3

Responsibilities:

* Convert text responses to speech
* Provide auditory feedback to the user

---

## Design Principles

Helen follows several simple design principles:

Modularity
Each capability is implemented as an independent module.

Extensibility
New AI modules can be added without modifying the entire system.

Accessibility
All feedback is delivered through voice output to assist visually impaired users.

---

## Future Architecture Improvements

Possible architectural improvements include:

* Context-aware conversation memory
* Event-driven command system
* More advanced vision models
* Integration with mobile or embedded devices
* Local AI models for offline operation
