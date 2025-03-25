from service.config_reader import ConfigReader
from service.patch_manager import PatchManager
from ui.view import PatchGUI

class AppController:
    def __init__(self, config_path="./config.json"):
        self.config_reader = ConfigReader(config_path)
        self.patch_manager = PatchManager()
        self.gui = None

    def run(self):
        config_list = self._load_config()
        self.gui = self._create_gui(config_list)
        self.gui.run()

    def _load_config(self):
        return self.config_reader.read_config()

    def _create_gui(self, config_list):
        gui = PatchGUI(set_source_callback=self.patch_manager.set_source_dir)
        gui.create_config_buttons(config_list)
        gui.init_action_buttons(config_list, self._get_commands())
        return gui

    def _get_commands(self):
        pm = self.patch_manager
        return {
            "send_list_import": pm.send_patch_list_import,
            "start_db_patch": pm.start_db_patch,
            "check_server_process": pm.check_server_process,
            "start_server": pm.start_server,
            "stop_server": pm.stop_server,
            "start_server_log": pm.start_server_log,
            "stop_server_log": pm.stop_server_log,
            "deploy_properties": pm.deploy_properties,
            "send_webroot": pm.send_webroot,
            "send_classes": pm.send_classes,
        }
