import os
import sys
import threading
from pathlib import Path

os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")

from PySide6.QtCore import QObject, Property, QUrl, Signal, Slot
from PySide6.QtGui import (
    QAccessible,
    QAccessibleAnnouncementEvent,
    QGuiApplication,
)
from PySide6.QtQml import QQmlApplicationEngine

from assistant import announce_capabilities, listen, route_command
from utils.audio import get_voice_settings, list_voices, speak, update_voice_settings
from utils.events import set_event_listener


class HelenBridge(QObject):
    stateChanged = Signal()
    messageChanged = Signal()
    historyChanged = Signal()
    busyChanged = Signal()
    voiceSettingsChanged = Signal()
    accessibilityAnnouncementRequested = Signal(str)

    def __init__(self):
        super().__init__()
        self._state = "idle"
        self._message = "Ready. Ask naturally or choose an action."
        self._history = []
        self._busy = False
        self._voice_options = []
        self._voice_name = "System voice"
        self._voice_engine = "edge"
        self._speech_rate = 158
        self._speech_volume = 88
        self._load_voice_settings()
        set_event_listener(self._receive_event)
        self.accessibilityAnnouncementRequested.connect(
            self._announce_accessibly
        )

    @Property(str, notify=stateChanged)
    def state(self):
        return self._state

    @Property(str, notify=messageChanged)
    def message(self):
        return self._message

    @Property("QStringList", notify=historyChanged)
    def history(self):
        return self._history

    @Property(bool, notify=busyChanged)
    def busy(self):
        return self._busy

    @Property("QStringList", notify=voiceSettingsChanged)
    def voiceOptions(self):
        return [voice["name"] for voice in self._voice_options]

    @Property(str, notify=voiceSettingsChanged)
    def voiceName(self):
        return self._voice_name

    @Property(int, notify=voiceSettingsChanged)
    def speechRate(self):
        return self._speech_rate

    @Property(int, notify=voiceSettingsChanged)
    def speechVolume(self):
        return self._speech_volume

    @Property(bool, notify=voiceSettingsChanged)
    def neuralVoiceEnabled(self):
        return self._voice_engine == "edge"

    @Slot()
    def announceCapabilities(self):
        self._run_background(announce_capabilities)

    @Slot()
    def startListening(self):
        self._run_background(self._listen_and_route)

    @Slot(str)
    def runCommand(self, command):
        command = command.strip()
        if command:
            self._run_background(lambda: route_command(command))

    @Slot(str, int, int)
    def updateVoiceSettings(self, voice_name, rate, volume):
        voice_id = next(
            (
                voice["id"]
                for voice in self._voice_options
                if voice["name"] == voice_name
            ),
            "",
        )
        settings = update_voice_settings(
            voice_id=voice_id,
            rate=rate,
            volume=volume / 100,
        )
        self._apply_voice_settings(settings)
        self.voiceSettingsChanged.emit()

    @Slot(bool)
    def setNeuralVoiceEnabled(self, enabled):
        settings = update_voice_settings(
            engine_name="edge" if enabled else "system"
        )
        self._apply_voice_settings(settings)
        self.voiceSettingsChanged.emit()

    @Slot()
    def exportTranscript(self):
        transcript_dir = Path.home() / "Documents" / "Helen"
        transcript_dir.mkdir(parents=True, exist_ok=True)
        transcript_file = transcript_dir / "helen-transcript.txt"
        transcript_file.write_text("\n\n".join(self._history), encoding="utf-8")
        self._receive_event("idle", f"Transcript saved to {transcript_file}")

    def _apply_voice_settings(self, settings):
        self._voice_engine = settings["engine"]
        self._voice_name = settings["voice_name"]
        self._speech_rate = settings["rate"]
        self._speech_volume = round(settings["volume"] * 100)

    @Slot()
    def previewVoice(self):
        self._run_background(
            lambda: speak("Hello. I'm Helen. How may I help?")
        )

    def _listen_and_route(self):
        command = listen()
        if command:
            route_command(command)

    def _load_voice_settings(self):
        self._voice_options = list_voices()
        settings = get_voice_settings()
        self._apply_voice_settings(settings)

    def _receive_event(self, state, message=""):
        self._state = state
        self.stateChanged.emit()
        if message:
            self._message = message
            self.messageChanged.emit()
            self._history = (self._history + [message])[-20:]
            self.historyChanged.emit()
            self.accessibilityAnnouncementRequested.emit(message)

    @Slot(str)
    def _announce_accessibly(self, message):
        event = QAccessibleAnnouncementEvent(self, message)
        QAccessible.updateAccessibility(event)

    def _run_background(self, operation):
        if self._busy:
            return
        self._busy = True
        self.busyChanged.emit()

        def worker():
            try:
                operation()
            except KeyboardInterrupt:
                QGuiApplication.quit()
            except Exception as error:
                self._receive_event("idle", f"Something went wrong: {error}")
            finally:
                self._busy = False
                self.busyChanged.emit()

        threading.Thread(target=worker, daemon=True).start()


def main():
    app = QGuiApplication(sys.argv)
    app.setApplicationName("Helen")
    app.setOrganizationName("Helen Accessibility")

    engine = QQmlApplicationEngine()
    bridge = HelenBridge()
    engine.rootContext().setContextProperty("helen", bridge)

    qml_file = Path(__file__).resolve().parent / "qml" / "Main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_file)))
    if not engine.rootObjects():
        raise RuntimeError("Helen desktop interface could not be loaded.")

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
