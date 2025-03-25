from service.ssh_client import SshClient

class LogMonitor:
    def __init__(self, logger):
        self.logger = logger
        self.client = None

    def start(self, config):
        if self.client is not None:
            self.logger.message("이미 실행 중인 로그가 있습니다.")
            return

        self.client = SshClient(config)
        self.client.connect()
        self.client.tail_follow(config.server_log)
        self.client = None  # tail_follow 종료 후 해제

    def stop(self):
        if self.client is None:
            self.logger.message("실행 중인 로그가 없습니다.")
            return

        self.client.stop_tail()
