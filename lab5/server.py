import socket
import threading
import json
import re
import base64
from os import mkdir
from time import sleep

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
            # print(message)
            try:
                message_payload = json.loads(message)
                print(json.dumps(message_payload, indent=4), end='\n')
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
                    for client in rooms[m_room].keys():
                        if client != client_socket:
                            client.send(json.dumps(client_message_payload).encode('utf-8'))
                        elif client == client_socket and m_type == "connect":
                            client.send(
                                json.dumps({"type": "connect_ack", "payload": {"message": "Connected to room " + m_room,
                                                                               "room": m_room}}).encode('utf-8'))
                elif m_type == "disconnect":
                    client_message_payload["type"] = "notification"
                    client_message_payload["payload"] = {}
                    client_message_payload["payload"]["message"] = m_sender + " has disconnected from " + m_room

                    del rooms[m_room][client_socket]
                    for client in rooms[m_room].keys():
                        if client != client_socket:
                            client.send(json.dumps(client_message_payload).encode('utf-8'))
                elif m_type == "message":
                    client_message_payload["type"] = "message"
                    client_message_payload["payload"] = {}
                    client_message_payload["payload"]["sender"] = m_sender
                    client_message_payload["payload"]["room"] = m_room
                    client_message_payload["payload"]["text"] = m_payload["text"]
                    for client in rooms[m_room].keys():
                        if client != client_socket:
                            client.send(json.dumps(client_message_payload).encode('utf-8'))
                elif m_type == "upload":
                    # TODO: Notify clients of file upload
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

                    client_message_payload["type"] = "notification"
                    client_message_payload["payload"] = {}
                    client_message_payload["payload"]["message"] = m_sender + " has uploaded " + m_payload["file_name"]
                    for client in rooms[m_room].keys():
                        if client != client_socket:
                            client.send(json.dumps(client_message_payload).encode('utf-8'))
                elif m_type == "file":
                    if m_payload["file_hash"] not in file_queue.keys():
                        file_queue[m_payload["file_hash"]] = {}
                    file_queue[m_payload["file_hash"]][m_payload["piece"]] = m_payload["data"]
                elif m_type == "download":
                    try:
                        with open("remote/" + m_room + "/file_data.json", "r") as file:
                            file_content = json.loads(file.read())
                            file.close()
                        file_name = file_content[int(m_payload["file_no"])]["file_name"]
                    except IndexError:
                        client_message_payload["type"] = "notification"
                        client_message_payload["payload"] = {}
                        client_message_payload["payload"]["message"] = "File not found"
                        client_socket.send(json.dumps(client_message_payload).encode('utf-8'))
                        continue
                    except FileNotFoundError:
                        client_message_payload["type"] = "notification"
                        client_message_payload["payload"] = {}
                        client_message_payload["payload"]["message"] = "Room doesn't have files"
                        client_socket.send(json.dumps(client_message_payload).encode('utf-8'))
                        continue
                    else:
                        with open("remote/" + m_room + "/" + file_name, "rb") as file:
                            file_data = base64.b64encode(file.read()).decode("utf-8")
                            file.close()
                    file_id = m_room + "@" + file_name + "@"
                    blob_size = 1024 - len(file_id)
                    n = 0
                    while True:
                        blob = file_data[n * blob_size: (n + 1) * blob_size]
                        if blob == "":
                            break
                        n += 1
                        client_socket.send((file_id + blob).encode("utf-8"))
                    sleep(0.2)
                    client_socket.send((file_id + "end").encode("utf-8"))

                elif m_type == "list":
                    client_message_payload["type"] = "notification"
                    client_message_payload["payload"] = {}
                    client_message_payload["payload"]["message"] = "Files in " + m_room + ":"
                    with open("remote/" + m_room + "/file_data.json", "r") as file:
                        file_content = json.loads(file.read())
                        for i in range(len(file_content)):
                            client_message_payload["payload"]["message"] += "\n" + str(i) + ". " + file_content[i]["file_name"]
                        file.close()
                    client_socket.send(json.dumps(client_message_payload).encode('utf-8'))
                elif m_type == "exit":
                    ...
                    # break

            except json.decoder.JSONDecodeError:
                # TODO: Check hash
                message_payload = message.split("@")
                # print(message_payload)
                sender = message_payload[0]
                room = message_payload[1]
                file_name = message_payload[2]
                message_id = sender + "@" + room + "@" + file_name
                if message_id not in file_queue.keys():
                    file_queue[message_id] = ""
                if message_payload[3] != "end":
                    file_queue[message_id] += message_payload[3]
                else:
                    with open("remote/" + room + "/" + file_name, "wb") as file:
                        file.write(base64.b64decode(file_queue[message_id].encode("utf-8")))
                        file.close()
                    del file_queue[message_id]
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
