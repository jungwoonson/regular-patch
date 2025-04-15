from domain.transfer_info import TransferInfo
from infra.shared.logger import Logger
from service.sftp_client import SFtpClient

class PatchTransfer:
    def __init__(self, transfer_info: TransferInfo):
        self.transfer_info = transfer_info

    def _make_client(self, config):
        return SFtpClient(
            config.remote_host,
            config.remote_port,
            config.remote_username,
            config.remote_key_path
        )

    def send_patch_list_import(self, ):
        client = self._make_client(config)
        client.send_file(self.transfer_info.source_dir, self.transfer_info.target_dir, "patch_list_import.sql")

    def send_webroot(self, config):
        client = self._make_client(config)
        source = self.get_source_dir() + config.get_patch_webroot()
        exclude_list = ["patch_list_import.sql", "WEB-INF"]
        Logger().server_log(f"[{config.remote_host}:{config.remote_port}] webroot 전송 시작")
        client.transfer_directory(source, config.remote_webroot, exclude_list)
        Logger().server_log(f"[{config.remote_host}:{config.remote_port}] webroot 전송 완료")

    def send_classes(self, config):
        client = self._make_client(config)
        source = f"{self.get_source_dir()}{config.get_patch_webroot()}/WEB-INF/{config.get_classes_dir()}"
        target = f"{config.remote_webroot}/WEB-INF/classes"
        Logger().server_log(f"[{config.remote_host}:{config.remote_port}] classes 전송 시작")
        client.transfer_directory(source, target)
        Logger().server_log(f"[{config.remote_host}:{config.remote_port}] classes 전송 완료")
