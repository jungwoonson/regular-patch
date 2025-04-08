from controller.defualt_button_command import DefaultButtonCommand
from infra.shared.logger import Logger
from domain.config_list import ConfigList
from ui.button_command import ButtonCommand
from ui.patch_gui import PatchGUI


class AppController:
    def __init__(self, config_path="./config.json"):
        self.config_list: ConfigList = ConfigList.create(config_path)
        self.button_command: ButtonCommand = DefaultButtonCommand(self.config_list)
        self.gui = PatchGUI(self.config_list.get_button_names(), self.button_command)
        Logger().bind_text_widget(self.gui.get_log_widget())

    def run(self):
        self.gui.run()
