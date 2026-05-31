from pathlib import Path

# Configuration settings
LANGUAGE = "en"

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
SONGS_DIR = DATA_DIR / "songs"
MODEL_DIR = BASE_DIR / "models"

CAMERA_INDEX = 0
OBJECT_CONFIDENCE_THRESHOLD = 0.6
OBJECT_MODEL_WEIGHTS = MODEL_DIR / "frozen_inference_graph.pb"
OBJECT_MODEL_CONFIG = MODEL_DIR / "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
