from pathlib import Path
from shutil import copyfileobj
from tempfile import NamedTemporaryFile
from urllib.request import Request, urlopen
from zipfile import ZipFile

from utils.config import (
    HAND_LANDMARKER_MODEL,
    MODEL_DIR,
    OBJECT_MODEL_CONFIG,
    OBJECT_MODEL_WEIGHTS,
    VOSK_WAKE_MODEL,
)


MODEL_DOWNLOADS = {
    HAND_LANDMARKER_MODEL: (
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
        "hand_landmarker/float16/1/hand_landmarker.task"
    ),
    OBJECT_MODEL_WEIGHTS: (
        "https://raw.githubusercontent.com/zafarRehan/"
        "object_detection_COCO/main/frozen_inference_graph.pb"
    ),
    OBJECT_MODEL_CONFIG: (
        "https://raw.githubusercontent.com/zafarRehan/"
        "object_detection_COCO/main/"
        "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
    ),
}

VOSK_WAKE_MODEL_URL = (
    "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
)


def download_file(destination: Path, url: str):
    if destination.exists() and destination.stat().st_size > 0:
        print(f"Already present: {destination.name}")
        return

    print(f"Downloading: {destination.name}")
    request = Request(url, headers={"User-Agent": "Helen-Model-Setup/1.0"})
    with urlopen(request, timeout=45) as response:
        destination.write_bytes(response.read())
    print(f"Saved: {destination.name} ({destination.stat().st_size:,} bytes)")


def download_vosk_model():
    if VOSK_WAKE_MODEL.exists():
        print(f"Already present: {VOSK_WAKE_MODEL.name}")
        return

    print(f"Downloading: {VOSK_WAKE_MODEL.name}")
    request = Request(
        VOSK_WAKE_MODEL_URL,
        headers={"User-Agent": "Helen-Model-Setup/1.0"},
    )
    with NamedTemporaryFile(delete=False, suffix=".zip") as temp_file:
        archive_path = Path(temp_file.name)
        with urlopen(request, timeout=90) as response:
            copyfileobj(response, temp_file)

    try:
        with ZipFile(archive_path) as archive:
            archive.extractall(MODEL_DIR)
    finally:
        archive_path.unlink(missing_ok=True)
    print(f"Saved: {VOSK_WAKE_MODEL.name}")


def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    for destination, url in MODEL_DOWNLOADS.items():
        download_file(destination, url)
    download_vosk_model()
    print("\nHelen model assets are ready.")


if __name__ == "__main__":
    main()
