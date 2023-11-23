# src/RAFT.py

from socket import socket, AF_INET, SOCK_DGRAM
from json import dumps, loads
import random


class RAFT:
    def __init__(
            self,
            host: str,
            port: int,
            instance_ct: int,
            server_params: dict,
    ):
        self.host: str = host
        self.port: int = port
        self.instance_ct: int = instance_ct
        self.server_params: dict = server_params

        self.socket: socket = socket(AF_INET, SOCK_DGRAM)

        # Bind socket to host and an available port
        try:
            # Successful bind will assign "main" role
            self.socket.bind((self.host, self.port))
            self.role: str = "main"
            self.token: str = str(random.randint(100000, 999999))
            print(self.server_params["host"] + ":" + str(self.server_params["port"]) + ": Successfully bound socket to host and port, assigned main role")

            self.backup_params: list = []
            while len(self.backup_params) < self.instance_ct - 1:
                print(self.server_params["host"] + ":" + str(self.server_params["port"]) + ": Awaiting backup params from backup server")
                self.server_params["token"] = self.token
                msg, addr = self.socket.recvfrom(1024)
                msg = msg.decode()

                if msg == "ack":
                    # Wait for "ack" message from client
                    # Send server params to client
                    self.socket.sendto(dumps(self.server_params).encode(), addr)
                else:
                    # Received "backup" params
                    self.backup_params.append(loads(msg))
                    print(self.server_params["host"] + ":" + str(self.server_params["port"]) + ": Received backup params from backup server: ", msg)

        except:
            print(self.server_params["host"] + ":" + str(self.server_params["port"]) + ": Failed to bind socket to host and port, assigning backup role")

            # Unsuccessful bind will assign "backup" role
            self.role: str = "backup"

            # Send "ack" message to server
            self.socket.sendto("ack".encode(), (self.host, self.port))

            # Receive server params from server
            self.main_params: dict = loads(self.socket.recvfrom(1024)[0].decode())
            print(self.server_params["host"] + ":" + str(self.server_params["port"]) + ": Received main params from main server: ", self.main_params)

            # Send "backup" params to server
            self.socket.sendto(dumps(self.server_params).encode(), (self.host, self.port))
