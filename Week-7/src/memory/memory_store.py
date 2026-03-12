import json
import os
from datetime import datetime

os.makedirs("src/logs", exist_ok=True)

MEMORY_FILE = "src/logs/CHAT-LOGS.json"
MAX_HISTORY = 5

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump([], f)


class MemoryStore:
    def load(self):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)

    def save(self, role, content):
        history = self.load()

        history.append({
            "timestamp": str(datetime.utcnow()),
            "role": role,
            "content": content
        })

        history = history[-MAX_HISTORY:]

        with open(MEMORY_FILE, "w") as f:
            json.dump(history, f, indent=4)

    def get(self):
        return self.load()