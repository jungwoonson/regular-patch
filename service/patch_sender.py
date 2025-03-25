from service.sftp_client import SFtpClient

class PatchSender:
    def __init__(self, logger, source_dir_getter):
        self.logger = logger
        self.get_source_dir = source_dir_getter  # 함수로 받아옴

    def _make_client(self, config):
        return SFtpClient(
            config.remote_host,
            config.remote_port,
            config.remote_username,
            config.remote_key_path
        )

    def send_patch_list_import(self, config):
        client = self._make_client(config)
        source = self.get_source_dir() + config.get_patch_webroot()
        client.send_file(source, config.remote_webroot, "patch_list_import.sql")

    def send_webroot(self, config):
        client = self._make_client(config)
        source = self.get_source_dir() + config.get_patch_webroot()
        exclude_list = ["patch_list_import.sql", "WEB-INF"]
        self.logger.message(f"[{config.remote_host}:{config.remote_port}] webroot 전송 시작")
        client.transfer_directory(source, config.remote_webroot, exclude_list)
        self.logger.message(f"[{config.remote_host}:{config.remote_port}] webroot 전송 완료")

    def send_classes(self, config):
        client = self._make_client(config)
        source = f"{self.get_source_dir()}{config.get_patch_webroot()}/WEB-INF/{config.get_classes_dir()}"
        target = f"{config.remote_webroot}/WEB-INF/classes"
        self.logger.message(f"[{config.remote_host}:{config.remote_port}] classes 전송 시작")
        client.transfer_directory(source, target)
        self.logger.message(f"[{config.remote_host}:{config.remote_port}] classes 전송 완료")
