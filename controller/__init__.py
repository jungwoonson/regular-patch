from service.config_reader import ConfigReader


def __init__(self, config_path="./config.json"):
    self.config_reader = ConfigReader(config_path)