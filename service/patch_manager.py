from service.browser_automator import BrowserAutomator
from service.log_monitor import LogMonitor
from service.patch_sender import PatchSender
from service.properties_deployer import PropertiesDeployer
from service.server_manager import ServerManager
from ui.logger import global_logger


class PatchManager:
    def __init__(self, logger=global_logger):
        self.logger = logger
        self.source_dir = ""
        self.log_client = None

        self.server_manager = ServerManager(self.logger)
        self.log_monitor = LogMonitor(self.logger)
        self.patch_sender = PatchSender(self.logger, self.get_source_dir)
        self.properties_deployer = PropertiesDeployer(self.logger, self.get_source_dir)
        self.browser_automator = BrowserAutomator(self.logger)

    def get_source_dir(self):
        if not self.source_dir:
            self.logger.message("패치루트를 설정해주세요.")
            raise Exception("패치루트를 설정해주세요.")
        return self.source_dir

    def set_source_dir(self, dir_path):
        self.source_dir = dir_path
        self.logger.message("패치 루트 설정: " + dir_path)

    def send_patch_list_import(self, config):
        self.patch_sender.send_patch_list_import(config)

    def start_db_patch(self, config):
        self.browser_automator.start_db_patch(config)

    def patch_multilingual(self, config):
        self.browser_automator.patch_multilingual(config)

    def check_server_process(self, config):
        self.server_manager.check_process(config)

    def start_server(self, config):
        self.server_manager.start(config)

    def stop_server(self, config):
        self.server_manager.stop(config)

    def start_server_log(self, config):
        self.log_monitor.start(config)

    def stop_server_log(self, config):
        self.log_monitor.stop()

    def deploy_properties(self, config):
        self.properties_deployer.deploy(config)

    def send_webroot(self, config):
        self.patch_sender.send_webroot(config)

    def send_classes(self, config):
        self.patch_sender.send_classes(config)
