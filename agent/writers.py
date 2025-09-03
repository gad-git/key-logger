import os
from datetime import datetime

class FileWriter:
    def __init__(self, folder: str) -> None:
        os.makedirs(folder, exist_ok=True)   # יוצר את התיקייה אם לא קיימת
        self.folder = folder

    def send_data(self, data: str, machine_name: str = "") -> None:
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = os.path.join(self.folder, f"log_{ts}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)
        print(f"[WRITE] saved to {path}")
