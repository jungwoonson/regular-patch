import posixpath
import os.path
import paramiko
from ui.logger import global_logger


class SFtpClient:
    def __init__(self, host, port, username, key_path):
        self.logger = global_logger
        self.host = host
        self.port = port
        self.username = username
        self.key_path = key_path

    def send_file(self, local_dir, remote_dir, file_name):
        local_file_path = posixpath.join(local_dir, file_name)
        remote_file_path = posixpath.join(remote_dir, file_name)

        if not os.path.isfile(local_file_path):
            self.logger.message("파일이 존재하지 않습니다:", local_file_path)
            raise FileNotFoundError(f"파일이 존재하지 않습니다: {local_file_path}")

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            key = paramiko.RSAKey.from_private_key_file(self.key_path)
            client.connect(hostname=self.host, port=self.port,
                           username=self.username, pkey=key)
            sftp = client.open_sftp()

            try:
                sftp.stat(remote_dir)
            except IOError:
                self.logger.message("원격 디렉토리가 존재하지 않습니다:", remote_dir)
                raise Exception(f"원격 디렉토리가 존재하지 않습니다: {remote_dir}")

            sftp.put(local_file_path, remote_file_path)
            self.logger.message("파일 전송 완료:", local_file_path, "->", remote_file_path)
            sftp.close()
        except Exception as e:
            self.logger.message("파일 전송 중 오류 발생:", e)
            raise Exception(f"파일 전송 중 오류 발생: {local_file_path}")
        finally:
            client.close()

    def receive_file(self, local_dir, remote_dir, file_name):
        local_file_path = posixpath.join(local_dir, file_name)
        remote_file_path = posixpath.join(remote_dir, file_name)

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            key = paramiko.RSAKey.from_private_key_file(self.key_path)
            client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                pkey=key
            )
            sftp = client.open_sftp()

            try:
                sftp.stat(remote_file_path)
            except IOError:
                self.logger.message("원격 파일이 존재하지 않습니다:", remote_file_path)
                raise Exception(f"원격 파일이 존재하지 않습니다: {remote_file_path}")

            if not os.path.isdir(local_dir):
                os.makedirs(local_dir)

            sftp.get(remote_file_path, local_file_path)
            self.logger.message("파일 수신 완료:", remote_file_path, "->", local_file_path)
            sftp.close()
        except Exception as e:
            self.logger.message("파일 수신 중 오류 발생:", e)
            raise Exception(f"파일 수신 중 오류 발생: {remote_file_path}")
        finally:
            client.close()

    def ensure_remote_directory(self, sftp, remote_directory):
        """
        주어진 원격 디렉토리가 존재하는지 확인하고, 없으면 상위부터 재귀적으로 생성합니다.
        """
        try:
            sftp.stat(remote_directory)
        except IOError:
            parent = posixpath.dirname(remote_directory)
            if parent and parent != remote_directory:
                self.ensure_remote_directory(sftp, parent)
            sftp.mkdir(remote_directory)
            self.logger.message(f"디렉토리생성: {remote_directory}")

    def transfer_directory(self, local_directory, remote_directory, exclude_list=None):
        if exclude_list is None:
            exclude_list = []

        if not os.path.isdir(local_directory):
            self.logger.message("로컬 디렉토리가 존재하지 않습니다:", local_directory)
            raise Exception(f"로컬 디렉토리가 존재하지 않습니다: {local_directory}")

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            key = paramiko.RSAKey.from_private_key_file(self.key_path)
            client.connect(hostname=self.host, port=self.port, username=self.username, pkey=key)
            sftp = client.open_sftp()

            try:
                sftp.stat(remote_directory)
            except IOError:
                self.logger.message("원격 디렉토리가 존재하지 않습니다:", remote_directory)
                raise Exception(f"원격 디렉토리가 존재하지 않습니다: {remote_directory}")

            for root, dirs, files in os.walk(local_directory):
                dirs[:] = [d for d in dirs if d not in exclude_list]

                rel_path = os.path.relpath(root, local_directory)
                if rel_path == ".":
                    current_remote_dir = remote_directory
                else:
                    current_remote_dir = posixpath.join(remote_directory, rel_path).replace("\\", "/")

                try:
                    sftp.stat(current_remote_dir)
                except IOError:
                    self.ensure_remote_directory(sftp, current_remote_dir)

                for file in files:
                    if file in exclude_list:
                        continue
                    local_file = posixpath.join(root, file).replace("\\", "/")
                    remote_file = posixpath.join(current_remote_dir, file).replace("\\", "/")
                    sftp.put(local_file, remote_file)
                    self.logger.message(f"파일전송: {local_file} -> {remote_file}")

            sftp.close()
        except Exception as e:
            self.logger.message("전송 중 오류 발생:", e)
        finally:
            client.close()


