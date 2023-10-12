import socket
import threading
import json
import re
import base64
from os import mkdir

# Host parameters
HOST = '127.0.0.1'
PORT = 8080

# List of active clients
rooms = {}
file_queue = {}
clients = []


# Client handler
def handle_client(client_socket, client_address):
    print("Accepted connection from {}:{}".format(*client_address))

    while True:
        message = client_socket.recv(1024).decode('utf-8')

        if message:
            print(message)
            message_payload = json.loads(message)
            # print(json.dumps(message_payload, indent=4), end='\n\n')
            client_message_payload = {}
            m_type = message_payload["type"]
            m_payload = message_payload["payload"]
            m_room = m_payload["room"]
            m_sender = m_payload["sender"]

            # TODO: Add message display to server console
            if m_type == "connect":
                if m_payload["room"] not in rooms.keys():
                    rooms[m_room] = {}

                rooms[m_room][client_socket] = m_sender
                client_message_payload["type"] = "notification"
                client_message_payload["payload"] = {}
                client_message_payload["payload"]["message"] = m_sender + " has connected to " + m_room
            elif m_type == "disconnect":
                client_message_payload["type"] = "notification"
                client_message_payload["payload"] = {}
                client_message_payload["payload"]["message"] = m_sender + " has disconnected from " + m_room

                del rooms[m_room][client_socket]
            elif m_type == "message":
                client_message_payload["type"] = "message"
                client_message_payload["payload"] = {}
                client_message_payload["payload"]["sender"] = m_sender
                client_message_payload["payload"]["room"] = m_room
                client_message_payload["payload"]["text"] = m_payload["text"]
            elif m_type == "upload":
                try:
                    mkdir("remote/" + m_room)
                except FileExistsError:
                    pass

                try:
                    open("remote/" + m_room + "/" + "file_data.json", "r").close()
                except FileNotFoundError:
                    with open("remote/" + m_room + "/file_data.json", "w") as file:
                        file.write("[]")
                        file.close()

                with open("remote/" + m_room + "/file_data.json", "r") as file:
                    file_content = json.loads(file.read())
                    file.close()

                with open("remote/" + m_room + "/file_data.json", "w") as file:
                    file_data = {"file_name": m_payload["file_name"], "file_hash": m_payload["file_hash"]}
                    file_content.append(file_data)
                    file.write(json.dumps(file_content, indent=4))
                    file.close()

            elif m_type == "file":
                if m_payload["file_hash"] not in file_queue.keys():
                    file_queue[m_payload["file_hash"]] = {}
                file_queue[m_payload["file_hash"]][m_payload["piece"]] = m_payload["data"]
            elif m_type == "end_file":
                with open("remote/" + m_room + "/" + m_payload["file_name"], "wb") as file:
                    for i in range(len(file_queue[m_payload["file_hash"]].keys())):
                        file.write(file_queue[m_payload["file_hash"]][i])
                    file.close()
                del file_queue[m_payload["file_hash"]]
            elif m_type == "download":
                ...
            elif m_type == "list":
                ...
            elif m_type == "exit":
                break

            for client in rooms[m_room].keys():
                if client != client_socket:
                    client.send(json.dumps(client_message_payload).encode('utf-8'))
                elif client == client_socket and m_type == "connect":
                    client.send(
                        json.dumps({"type": "connect_ack", "payload": {"message": "Connected to room " + m_room,
                                                                       "room": m_room}}).encode('utf-8'))

    clients.remove(client_socket)
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Listening on {}:{}".format(HOST, PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == '__main__':
    main()
