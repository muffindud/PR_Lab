# ./
# RAFT.py
from socket import socket, AF_INET, SOCK_DGRAM
from json import dumps, loads


class RAFT:
    def __init__(
            self,
            host: str,
            port: str,
            followers_ct: int,
            params: dict
    ):
        self.host: str = host
        self.port: str = port
        self.followers_ct: int = followers_ct

        # UDP socket object
        self.udp_socket: socket = socket(AF_INET, SOCK_DGRAM)

        try:
            # Try to acquire master role
            self.role: str = "master"

            # Bind UDP socket to host and port
            self.udp_socket.bind((self.host, self.port))

            # Store the followers in a list
            self.slave_params: list = []
            msg_ct: int = 0

            # Listen for messages from slave RAFT nodes
            while True:
                # Receive message from UDP socket
                msg, addr = self.udp_socket.recvfrom(1024)

                # If message is ping, send params
                if msg.decode() == "ping":
                    # If message is ping, send params
                    msg_ct += 1
                    self.udp_socket.sendto(
                        str.encode(dumps(params)),
                        addr
                    )
                else:
                    # If message is params, store slave params
                    msg_ct += 1
                    follower_params = loads(msg.decode())
                    self.slave_params.append(follower_params)

                # If all followers have been stored, stop listening
                if msg_ct == self.slave_params * 2:
                    break
        except:
            # If master role is not available, acquire slave role
            self.role: str = "slave"

            # Send ping to master
            self.udp_socket.sendto(str.encode("ping"), (self.host, self.port))
            self.master_params: dict = loads(self.udp_socket.recv(1024).decode())

            # Send params to master
            self.udp_socket.sendto(
                str.encode(dumps(params)),
                (self.host, self.port)
            )
