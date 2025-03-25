from dataclasses import dataclass

@dataclass
class Config:
    company_name: str
    company_code: str
    browser_id: str
    browser_pw: str
    browser_url: str
    remote_host: str
    remote_port: int
    remote_username: str
    remote_key_path: str
    remote_webroot: str
    jdk_version: str
    server_start: str
    server_stop: str
    server_log: str
    server_ps: str
    mobile_yn: str
    jade_version: str

    def is_v03(self) -> bool:
        return self.jade_version == "V03"

    def is_mobile(self) -> bool:
        return self.mobile_yn.strip().upper() == "Y"

    def get_patch_webroot(self) -> str:
        if self.is_mobile():
            return "/vmobile/WebRoot"

        return "/Source/WebRoot"

    def get_classes_dir(self) -> str:
        jdk_version = self.jdk_version
        if jdk_version == "1.8":
            return "classes 1.8"
        elif jdk_version == "1.7":
            return "classes 1.7"
        else:
            msg = "잘못된 JDK 버전입니다. config.json의 jdk_version을 확인하세요."
            self.logger.message(msg)
            raise Exception(msg)

    def get(self, field: str) -> str:
        return getattr(self, field)
