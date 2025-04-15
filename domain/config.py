class Config:
    __company_name: str = ""
    __company_code: str = ""
    __browser_id: str = ""
    __browser_pw: str = ""
    __browser_url: str = ""
    __remote_host: str = ""
    __remote_port: int = 22
    __remote_username: str = ""
    __remote_key_path: str = ""
    __remote_webroot: str = ""
    __jdk_version: str = ""
    __server_start: str = ""
    __server_stop: str = ""
    __server_log: str = ""
    __server_ps: str = ""
    __mobile_yn: str = ""
    __jade_version: str = ""

    def __init__(self, **kwargs):
        self.__company_name = kwargs.get("company_name", "")
        self.__company_code = kwargs.get("company_code", "")
        self.__browser_id = kwargs.get("browser_id", "")
        self.__browser_pw = kwargs.get("browser_pw", "")
        self.__browser_url = kwargs.get("browser_url", "")
        self.__remote_host = kwargs.get("remote_host", "")
        self.__remote_port = kwargs.get("remote_port", 22)
        self.__remote_username = kwargs.get("remote_username", "")
        self.__remote_key_path = kwargs.get("remote_key_path", "")
        self.__remote_webroot = kwargs.get("remote_webroot", "")
        self.__jdk_version = kwargs.get("jdk_version", "")
        self.__server_start = kwargs.get("server_start", "")
        self.__server_stop = kwargs.get("server_stop", "")
        self.__server_log = kwargs.get("server_log", "")
        self.__server_ps = kwargs.get("server_ps", "")
        self.__mobile_yn = kwargs.get("mobile_yn", "")
        self.__jade_version = kwargs.get("jade_version", "")

    def is_v03(self) -> bool:
        return self.__jade_version == "V03"

    def is_mobile(self) -> bool:
        return self.__mobile_yn.strip().upper() == "Y"

    def get_patch_webroot(self) -> str:
        if self.is_mobile():
            return "/vmobile/WebRoot"
        return "/Source/WebRoot"

    def get_classes_dir(self) -> str:
        jdk_version = self.__jdk_version
        if jdk_version == "1.8":
            return "classes 1.8"
        elif jdk_version == "1.7":
            return "classes 1.7"
        else:
            msg = "잘못된 JDK 버전입니다. config.json의 jdk_version을 확인하세요."
            raise Exception(msg)

    def is_equal(self, company_name) -> bool:
        return self.__company_name == company_name

    def get_company_name(self):
        return self.__company_name

    def get_remote_host(self):
        return self.__remote_host

    def get_remote_port(self):
        return self.__remote_port

    def get_remote_username(self):
        return self.__remote_username

    def get_remote_webroot(self):
        return self.__remote_webroot

    def get_jdk_version(self):
        return self.__jdk_version

    def get_browser_url(self):
        return self.__browser_url

    def get_browser_id(self):
        return self.__browser_id

    def get_browser_pw(self):
        return self.__browser_pw

    def get_company_code(self):
        return self.__company_code

    def get_remote_key_path(self):
        return self.__remote_key_path
