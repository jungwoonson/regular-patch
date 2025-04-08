from typing import override

from infra.shared.logger import Logger
from domain.config import Config
from domain.config_list import ConfigList
from domain.patch import Patch
from ui.button_command import ButtonCommand


class DefaultButtonCommand(ButtonCommand):

    def __init__(self, config_list: ConfigList):
        self.config_list = config_list
        self.patch: Patch = Patch()

    @override
    def set_patch_dir(self, patch_dir: str):
        self.patch.set_source_dir(patch_dir)
        Logger().log(f"패치폴더선택: {patch_dir}")

    @override
    def choose_remote(self, remote_name) -> Config:
        config: Config = self.config_list.find_config(remote_name)
        self.patch.set_config(config)
        Logger().log(f"서버 변경: [{config.get_company_name()}] {config.get_remote_host()}:{config.get_remote_port()}")
        return config

    @override
    def transfer_patch_sql(self):
        pass

    @override
    def start_browser_for_db_patch(self):
        pass

    @override
    def transfer_webroot(self):
        pass

    @override
    def transfer_classes(self):
        pass

    @override
    def deploy_system_properties(self):
        pass

    @override
    def start_server(self):
        pass

    @override
    def stop_server(self):
        pass

    @override
    def start_server_log(self):
        pass

    @override
    def stop_server_log(self):
        pass

    @override
    def check_process(self):
        pass
