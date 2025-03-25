from service.sftp_client import SFtpClient
from service.properties_updater import PropertiesUpdater

class PropertiesDeployer:
    def __init__(self, logger, source_dir_getter):
        self.logger = logger
        self.get_source_dir = source_dir_getter

    def deploy(self, config):
        source_dir = self.get_source_dir()

        client = SFtpClient(
            config.remote_host,
            config.remote_port,
            config.remote_username,
            config.remote_key_path
        )

        self.logger.message("system.properties 다운로드 중...")
        client.receive_file("./", f"{config.remote_webroot}/WEB-INF", "system.properties")

        updater = PropertiesUpdater()
        updater.update_system_properties(source_dir=source_dir, is_mobile=config.is_mobile())

        self.logger.message("system.properties 업로드 중...")
        client.send_file("./", f"{config.remote_webroot}/WEB-INF", "system.properties")

        updater.delete_system_properties()
        self.logger.message("시스템 프로퍼티 배포 완료")
