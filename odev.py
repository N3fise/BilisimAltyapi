import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# İzleme yapılacak dizin ve log dosyasının yolu
WATCH_DIRECTORY = "/home/ubuntu/bsm/test"
LOG_FILE = "/home/ubuntu/bsm/logs/changes.json"

# Olayları işlemek için bir sınıf tanımlıyoruz
class WatchdogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        self.log_event("modified", event)

    def on_created(self, event):
        self.log_event("created", event)

    def on_deleted(self, event):
        self.log_event("deleted", event)

    def log_event(self, event_type, event):
        # Değişikliği JSON formatında kaydediyoruz
        log_entry = {
            "event": event_type,
            "path": event.src_path,
            "is_directory": event.is_directory,
        }
        try:
            with open(LOG_FILE, "a") as log_file:
                log_file.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Log kaydedilirken hata oluştu: {e}")

if __name__ == "__main__":
    # Observer ile dizini izliyoruz
    event_handler = WatchdogHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIRECTORY, recursive=True)

    print(f"{WATCH_DIRECTORY} dizini izleniyor...")
    try:
        observer.start()
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
