
import datetime

def log_info(message):
    print(f"[INFO] {datetime.datetime.now().isoformat()}: {message}")

def log_error(error_message):
    print(f"[ERROR] {datetime.datetime.now().isoformat()}: An error occurred: {error_message}")