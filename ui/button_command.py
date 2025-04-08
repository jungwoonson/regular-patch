from abc import ABC, abstractmethod


class ButtonCommand(ABC):

    @abstractmethod
    def set_patch_dir(self, patch_dir):
        pass

    @abstractmethod
    def choose_remote(self, remote_name):
        pass

    @abstractmethod
    def transfer_patch_sql(self):
        pass

    @abstractmethod
    def start_browser_for_db_patch(self):
        pass

    @abstractmethod
    def transfer_webroot(self):
        pass

    @abstractmethod
    def transfer_classes(self):
        pass

    @abstractmethod
    def deploy_system_properties(self):
        pass

    @abstractmethod
    def start_server(self):
        pass

    @abstractmethod
    def stop_server(self):
        pass

    @abstractmethod
    def start_server_log(self):
        pass

    @abstractmethod
    def stop_server_log(self):
        pass

    @abstractmethod
    def check_process(self):
        pass
