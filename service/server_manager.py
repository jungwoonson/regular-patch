from infra.shared.logger import Logger
from service.ssh_client import SshClient

class ServerManager:
    def __init__(self, logger):
        pass

    def _run_ssh_command(self, config, command):
        client = SshClient(config)
        client.connect()
        Logger().server_log(f"[{config.company_name}] 명령 실행: {command}")
        client.send_command(command)
        client.close()

    def check_process(self, config):
        self._run_ssh_command(config, config.server_ps)

    def start(self, config):
        self._run_ssh_command(config, config.server_start)

    def stop(self, config):
        self._run_ssh_command(config, config.server_stop)
