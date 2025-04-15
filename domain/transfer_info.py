from domain.config import Config


class TransferInfo:

    def __init__(self, patch_dir: str, config: Config):
        self.__source_dir = patch_dir + ("/vmobile/WebRoot" if config.is_mobile() else "/Source/WebRoot")
        self.__target_dir = config.get_remote_webroot()
        self.__host = config.get_remote_host()
        self.__port = config.get_remote_port()
        self.__username = config.get_remote_username()
        self.__key_path = config.get_remote_key_path()

    @property
    def source_dir(self):
        return self.__source_dir

    @property
    def target_dir(self):
        return self.__target_dir

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def username(self):
        return self.__username

    @property
    def key_path(self):
        return self.__key_path