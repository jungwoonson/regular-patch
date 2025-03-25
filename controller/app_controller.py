from service.config_reader import ConfigReader
from service.patch_manager import PatchManager
from ui.view import PatchGUI

CONFIG_PATH = "./config.json"

class AppController:
    def __init__(self):
        self.config_reader = ConfigReader(CONFIG_PATH)
        self.patch_manager = PatchManager()
        self.gui = None

    def run(self):
        config_list = self.config_reader.read_config()
        self.gui = PatchGUI(set_source_callback=self.patch_manager.set_source_dir)

        self.gui.create_config_buttons(config_list)
        self.gui.init_action_buttons(config_list, self._get_commands())
        self.gui.run()

    def _get_commands(self):
        return {
            "send_list_import": self.patch_manager.send_patch_list_import,
            "start_db_patch": self.patch_manager.start_db_patch,
            "check_server_process": self.patch_manager.check_server_process,
            "start_server": self.patch_manager.start_server,
            "stop_server": self.patch_manager.stop_server,
            "start_server_log": self.patch_manager.start_server_log,
            "stop_server_log": self.patch_manager.stop_server_log,
            "deploy_properties": self.patch_manager.deploy_properties,
            "send_webroot": self.patch_manager.send_webroot,
            "send_classes": self.patch_manager.send_classes,
        }
