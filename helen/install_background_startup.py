import argparse
import os
import sys
from pathlib import Path


STARTUP_NAME = "HelenBackground.cmd"


def _startup_dir():
    appdata = os.getenv("APPDATA")
    if not appdata:
        raise RuntimeError("APPDATA is not available on this system.")
    return (
        Path(appdata)
        / "Microsoft"
        / "Windows"
        / "Start Menu"
        / "Programs"
        / "Startup"
    )


def _pythonw_path():
    executable = Path(sys.executable)
    candidate = executable.with_name("pythonw.exe")
    return candidate if candidate.exists() else executable


def install():
    if os.name != "nt":
        raise RuntimeError("Automatic startup installation is currently Windows-only.")

    startup_dir = _startup_dir()
    startup_dir.mkdir(parents=True, exist_ok=True)
    daemon_path = Path(__file__).resolve().parent / "background_daemon.py"
    command_path = startup_dir / STARTUP_NAME
    command_path.write_text(
        "\n".join(
            [
                "@echo off",
                f'cd /d "{daemon_path.parent}"',
                f'start "" /min "{_pythonw_path()}" "{daemon_path}"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Helen background startup installed: {command_path}")


def remove():
    command_path = _startup_dir() / STARTUP_NAME
    if command_path.exists():
        command_path.unlink()
        print(f"Removed: {command_path}")
    else:
        print("Helen background startup was not installed.")


def main():
    parser = argparse.ArgumentParser(
        description="Install or remove Helen's background wake listener at login."
    )
    parser.add_argument("--remove", action="store_true", help="Remove startup entry.")
    args = parser.parse_args()

    if args.remove:
        remove()
    else:
        install()


if __name__ == "__main__":
    main()
