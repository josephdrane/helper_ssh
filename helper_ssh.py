""" TODO: Add a docstring here.
"""

import re
import socket
import time
from typing import List

import paramiko


class Ssh:
    """ Example:
    import helper_ssh
    conn = helper_ssh.ssh('10.10.10.10','some.Username','somePassword')
    commands = ['cat /etc/centos-release | grep Cent', 'cat /etc/issue', 'cat /proc/version']
    response = conn.commands(commands=commands, sudo=True)
    commands = ['cat /etc/issue','cat /proc/version']
    response = conn.command(commands=commands)
    """

    def __init__(self, device: str, username: str, password: str):
        """ TODO: Add a docstring here.
        """
        self.device = device
        self.username = username
        self.password = password
        self._connect()

    def _connect(self) -> None:
        """ TODO: Add a docstring here.
        """
        self.ssh_connection = paramiko.SSHClient()
        self.ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh_connection.connect(
                self.device, username=self.username, password=self.password
            )
        except Exception as error:
            print(f"{self.device}, {error}")

        try:
            self.ssh_channel = self.ssh_connection.invoke_shell()
        except Exception as error:
            print(f"{self.device}, {error}")

    def send(self, commands: List[str]) -> List[str]:
        """ TODO: Add a docstring here.
        """
        buffer = []
        for command in commands:
            self.ssh_channel.send(command + "\n")
            while self.ssh_channel.recv_ready() is not True:
                time.sleep(1)
            buffer.append(self.ssh_channel.recv(99999).decode("utf-8").split("\n"))

        return buffer

    def sudo(self, commands: List[str], read_until=r"#"):
        """ TODO: Add a docstring here.
        """
        sudo_commands = ["sudo -s", self.password]
        command_set = sudo_commands + commands
        buffer = ""

        for command in command_set:
            self.ssh_channel.send(command + "\n")
            time.sleep(1)

            while not re.search(read_until, buffer):
                if self.ssh_channel.recv_ready():
                    try:
                        resp = self.ssh_channel.recv(8096)
                    except socket.timeout:
                        error = (
                            f"Timeout exceeded while attempting to read "
                            f"response after issuing {command} to {self.device}"
                        )
                        raise Exception(error)
                    buffer += resp.decode("utf-8")
                else:
                    time.sleep(1)

                return buffer

    def exit(self):
        """ TODO: Add a docstring here.
        """
        self.ssh_channel.close()
        self.ssh_connection.close()
