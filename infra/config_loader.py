import json
import os
from typing import List


class ConfigLoader:
    @staticmethod
    def load(config_path: str = "./config.json") -> List:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"설정 파일 {config_path}을(를) 찾을 수 없습니다.")

        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
