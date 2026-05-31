import sys
import threading
from pathlib import Path

from PySide6.QtCore import QObject, Property, QUrl, Signal, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from assistant import announce_capabilities, listen, route_command
from utils.events import set_event_listener


class HelenBridge(QObject):
    stateChanged = Signal()
    messageChanged = Signal()
    historyChanged = Signal()
    busyChanged = Signal()

    def __init__(self):
        super().__init__()
        self._state = "idle"
        self._message = "Ready. Ask naturally or choose an action."
        self._history = []
        self._busy = False
        set_event_listener(self._receive_event)

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

    def _listen_and_route(self):
        command = listen()
        if command:
            route_command(command)

    def _receive_event(self, state, message=""):
        self._state = state
        self.stateChanged.emit()
        if message:
            self._message = message
            self.messageChanged.emit()
            self._history = ([message] + self._history)[:8]
            self.historyChanged.emit()

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

    bridge.announceCapabilities()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
