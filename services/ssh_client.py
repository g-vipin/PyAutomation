import paramiko


class SSHClient:
    def __init__(self, host, username, password=None, pkey_path=None):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if pkey_path:
            key = paramiko.RSAKey.from_private_key_file(pkey_path)
            self.client.connect(hostname=host, username=username, pkey=key)
        else:
            self.client.connect(hostname=host, username=username, password=password)

    def execute(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode().strip()

    def close(self):
        self.client.close()
