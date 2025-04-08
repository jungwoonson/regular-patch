from domain.config import Config


class Patch:
    def __init__(self):
        self.__source_dir = None
        self.__config = None

    def set_source_dir(self, patch_dir: str):
        self.__source_dir = patch_dir

    def set_config(self, config: Config):
        self.__config = config
