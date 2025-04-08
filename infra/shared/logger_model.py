import os
import re
from datetime import datetime


class LoggerModel:
    def __init__(self, log_dir="./logs"):
        os.makedirs(log_dir, exist_ok=True)
        self.log_filename = f"{log_dir}/log_{datetime.now().strftime('%Y%m%d')}.txt"
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def clean(self, msg):
        return self.ansi_escape.sub('', msg)

    def save(self, msg):
        with open(self.log_filename, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
