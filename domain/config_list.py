from typing import List
from domain.config import Config

class ConfigList:
    def __init__(self, config_list: List):
        self.config_list: List[Config] = [Config(**item) for item in config_list]

    def get_button_names(self) -> List[str]:
        return [config.get_company_name() for config in self.config_list]

    def find_config(self, remote_name) -> Config:
        for config in self.config_list:
            if config.is_equal(remote_name):
                return config
        raise ValueError(f"Config not found for company_name: {remote_name}")
