from domain.config import Config


class Patch:
    def __init__(self):
        self.__patch_dir = None
        self.__config = None

    def set_patch_dir(self, patch_dir: str):
        self.__patch_dir = patch_dir

    def set_config(self, config: Config):
        self.__config = config

    def get_patch_info(self) -> TransferInfo:
        pass
