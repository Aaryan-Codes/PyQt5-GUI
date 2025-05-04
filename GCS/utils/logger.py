import os
import csv
from datetime import datetime

class DataLogger:
    def __init__(self, save_dir="logs"):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        self.file = None
        self.writer = None
        self.fields = []
        self.logging = False

    def start(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filepath = os.path.join(self.save_dir, f"log_{timestamp}.csv")
        self.file = open(self.filepath, mode='w', newline='')
        self.writer = None
        self.logging = True
        print(f"[Logger] Started logging to {self.filepath}")

    def stop(self):
        self.logging = False
        if self.file:
            self.file.close()
            print(f"[Logger] Stopped logging.")

    def log(self, data: dict):
        if not self.logging or self.file is None:
            return

        flat_data = self._flatten(data)

        if self.writer is None:
            self.fields = list(flat_data.keys())
            self.writer = csv.DictWriter(self.file, fieldnames=self.fields)
            self.writer.writeheader()

        # consistent headers
        for key in self.fields:
            flat_data.setdefault(key, None)

        self.writer.writerow(flat_data)

    def _flatten(self, data):
        flat = {}
        for key, value in data.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    flat[f"{key}_{subkey}"] = subvalue
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    flat[f"{key}_{i}"] = item
            else:
                flat[key] = value
        return flat
