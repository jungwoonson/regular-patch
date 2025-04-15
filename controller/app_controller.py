from controller.defualt_button_command import DefaultButtonCommand
from domain.config_list import ConfigList
from infra.config_loader import ConfigLoader
from infra.shared.logger import Logger
from ui.button_command import ButtonCommand
from ui.patch_gui import PatchGUI


class AppController:
    def __init__(self, config_path="./config.json"):
        config_list: ConfigList = ConfigList(ConfigLoader.load(config_path))
        self.button_command: ButtonCommand = DefaultButtonCommand(config_list)
        self.gui = PatchGUI(config_list.get_button_names(), self.button_command)
        Logger().bind_text_widget(self.gui.get_log_widget())

    def run(self):
        self.gui.run()
