import json
import os
from typing import List
from typing import Self

from domain.config import Config


class ConfigList:
    def __init__(self, config_list:List[Config]):
        self.config_list = config_list

    @classmethod
    def create(cls, config_path:str="./config.json") -> Self:
        return cls(cls.__read_config(config_path))

    @classmethod
    def __read_config(cls, config_path) -> List[Config]:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"설정 파일 {config_path}을(를) 찾을 수 없습니다.")

        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return [Config(**item) for item in data]
            return [Config(**data)]

    def get_button_names(self) -> List[str]:
        return [config.get_company_name() for config in self.config_list]

    def find_config(self, remote_name) -> Config:
        for config in self.config_list:
            if config.is_equal(remote_name):
                return config
        raise ValueError(f"Config not found for company_name: {remote_name}")
