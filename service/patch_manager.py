from service.browser_controller import BrowserController
from service.properties_updater import PropertiesUpdater
from service.sftp_client import SFtpClient
from service.ssh_client import SshClient
from ui.logger import global_logger


class PatchManager:
    def __init__(self):
        self.logger = global_logger
        self.source_dir = ""
        self.log_client = None

    def send_patch_list_import(self, config):
        file_transfer = SFtpClient(config.remote_host, config.remote_port,
                                   config.remote_username,
                                   config.remote_key_path)
        file_transfer.send_file(self.source_dir + config.get_patch_webroot(), config.remote_webroot,
                                "patch_list_import.sql")

    def start_db_patch(self, config):
        controller = BrowserController(config.browser_url, config.browser_id, config.browser_pw, config.company_code,
                                       config.is_v03())
        controller.patch_db()

    def patch_multilingual(self, config):
        controller = BrowserController(config.browser_id, config.browser_pw, config.company_code)
        controller.create_multilingual(config.browser_url)

    def check_server_process(self, config):
        ssh_client = SshClient(config)
        ssh_client.connect()
        ssh_client.send_command(config.server_ps)
        ssh_client.close()

    def start_server(self, config):
        ssh_client = SshClient(config)
        ssh_client.connect()
        ssh_client.send_command(config.server_start)
        ssh_client.close()

    def stop_server(self, config):
        ssh_client = SshClient(config)
        ssh_client.connect()
        ssh_client.send_command(config.server_stop)
        ssh_client.close()

    def start_server_log(self, config):
        if self.log_client is not None:
            self.logger.message("이미 실행 중인 로그가 있습니다.")
            return

        self.log_client = SshClient(config)
        self.log_client.connect()
        self.log_client.tail_follow(config.server_log)

        self.log_client = None

    def stop_server_log(self, config):
        if self.log_client is None:
            self.logger.message("실행 중인 로그가 없습니다.")
            return

        self.log_client.stop_tail()

    def deploy_properties(self, config):
        file_transfer = SFtpClient(config.remote_host, config.remote_port,
                                   config.remote_username,
                                   config.remote_key_path)
        file_transfer.receive_file("./", f"{config.remote_webroot}/WEB-INF", "system.properties")

        file_manager = PropertiesUpdater()
        file_manager.update_system_properties(source_dir=self.source_dir, is_mobile=config.is_mobile())

        file_transfer.send_file("./", config.remote_webroot + "/WEB-INF",
                                "system.properties")
        file_manager.delete_system_properties()

    def send_webroot(self, config):
        file_transfer = SFtpClient(config.remote_host, config.remote_port,
                                   config.remote_username,
                                   config.remote_key_path)
        exclude_list = ["patch_list_import.sql", "WEB-INF"]
        self.logger.message(f"[{config.remote_host}:{config.remote_port}] webroot 전송 시작")
        file_transfer.transfer_directory(f"{self.source_dir}{config.get_patch_webroot()}", config.remote_webroot,
                                         exclude_list)
        self.logger.message(f"[{config.remote_host}:{config.remote_port}] webroot 전송 완료")

    def send_classes(self, config):
        classes_version = None
        if config.jdk_version == "1.8":
            classes_version = "classes 1.8"
        elif config.jdk_version == "1.7":
            classes_version = "classes 1.7"
        else:
            self.logger.message("잘못된 JDK 버전입니다. config.json의 jdk_version을 확인하세요.")
            raise Exception("잘못된 JDK 버전입니다. config.json의 jdk_version을 확인하세요.")


        file_transfer = SFtpClient(config.remote_host, config.remote_port,
                                   config.remote_username,
                                   config.remote_key_path)
        self.logger.message(f"[{config.remote_host}:{config.remote_port}] classes 전송 시작")
        file_transfer.transfer_directory(f"{self.source_dir}{config.get_patch_webroot()}/WEB-INF/{classes_version}",
                                         f"{config.remote_webroot}/WEB-INF/classes", )
        self.logger.message(f"[{config.remote_host}:{config.remote_port}] classes 전송 완료")

    def set_source_dir(self, dir_path):
        self.source_dir = dir_path
        self.logger.message("패치 루트 설정: " + dir_path)
