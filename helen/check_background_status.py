import json
import os
from datetime import datetime, timezone
from pathlib import Path


STATUS_PATH = Path.home() / ".helen" / "daemon_status.json"


def main():
    if not STATUS_PATH.exists():
        print("Helen background listener has not reported a status yet.")
        raise SystemExit(1)

    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    updated = datetime.fromisoformat(status["updated_at"])
    age = (datetime.now(timezone.utc) - updated).total_seconds()
    try:
        os.kill(int(status["pid"]), 0)
        process_running = True
    except OSError:
        process_running = False

    healthy = process_running and age < 15 and status["state"] in {
        "listening",
        "awake",
        "processing",
    }
    print(f"Healthy: {'yes' if healthy else 'no'}")
    print(f"State: {status['state']}")
    print(f"Detail: {status['detail']}")
    print(f"Wake detection: {status['wake_detection']}")
    print(f"Process ID: {status['pid']}")
    print(f"Last updated: {age:.0f} seconds ago")
    if not healthy:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
