import json
import os
from typing import List

from domain.config import Config


class ConfigReader:
    def __init__(self, filename: str):
        self.filename = filename
        self.configs: List[Config] = []

    def read_config(self) -> List[Config]:
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"설정 파일 {self.filename}을(를) 찾을 수 없습니다.")

        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, list):
                self.configs = [Config(**item) for item in data]
            else:
                self.configs = [Config(**data)]

        return self.configs
