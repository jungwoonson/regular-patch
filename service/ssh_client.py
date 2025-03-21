import paramiko
import time

from ui.logger import global_logger


class SshClient(object):
    def __init__(self, config):
        self.logger = global_logger
        self.host = config.remote_host
        self.port = int(config.remote_port)
        self.username = config.remote_username
        self.key_path = config.remote_key_path
        self.client = None
        self.channel = None
        self._stop_tail = None

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                key_filename=self.key_path
            )

            self.channel = self.client.invoke_shell()
            time.sleep(1)

            if self.channel.recv_ready():
                output = self.channel.recv(4096).decode('utf-8')
            self.logger.message(f"SSH 연결 성공: {self.host}")
        except Exception as e:
            self.logger.message_error(f"SSH 연결 실패: {e}")
            raise Exception(f"SSH 연결 실패: {e}")

    def send_command(self, command):
        if self.client is None or self.channel is None:
            self.logger.message_error("SSH 클라이언트가 연결되어 있지 않습니다.")
            return

        try:
            self.channel.send(command + "\n")
            time.sleep(1)  # 명령어 실행 후대기

            output = ""
            while self.channel.recv_ready():
                output += self.channel.recv(4096).decode('utf-8')
            if output:
                self.logger.server_message(output)
        except Exception as e:
            self.logger.message_error(f"명령어 실행 중 오류 발생: {e}")

    def close(self):
        if self.channel:
            self.channel.close()
        if self.client:
            self.client.close()
            self.logger.message("SSH 연결 종료")

    def tail_follow(self, command):
        if self.client is None or self.channel is None:
            self.logger.message_error("SSH 클라이언트가 연결되어 있지 않습니다.")
            return

        if self._stop_tail:
            self.logger.message_error("이미 실행 중인 로그가 있습니다.")
            return

        self._stop_tail = False

        try:
            self.channel.send(command + "\n")
            time.sleep(1)

            self.logger.message(f"tail_follow 시작: {command}")

            while not self._stop_tail:
                output = ""
                while self.channel.recv_ready():
                    output += self.channel.recv(4096).decode('utf-8', 'ignore')
                if output:
                    self.logger.server_message(output)
                time.sleep(0.5)

            self.logger.message("로그 출력 종료")
        except Exception as e:
            self.logger.message_error(f"tail_follow 실행 중 오류 발생: {e}")

    def stop_tail(self):
        self._stop_tail = True
