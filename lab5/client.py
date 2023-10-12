import socket
import threading
import json
import hashlib
import base64
from time import sleep

# Host parameters
HOST = '127.0.0.1'
POST = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def hash_file(file_path: str):
    h = hashlib.sha1()

    with open(file_path, 'rb') as file:
        chunk = 0

        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)

        file.close()

    return h.hexdigest()


def receive_message():
    while True:
        message = client_socket.recv(1024).decode('utf-8')

        if message:
            message_payload = json.loads(message)
            # print(message_payload)

            if message_payload["type"] == "connect_ack":
                print(message_payload["payload"]["message"])
            elif message_payload["type"] == "notification":
                print(message_payload["payload"]["message"])
            elif message_payload["type"] == "message":
                print(
                    message_payload["payload"]["sender"] + "@" +
                    message_payload["payload"]["room"] + ": " +
                    message_payload["payload"]["text"]
                )


def send_message():
    in_room = False
    room = ""
    sender = ""

    try:
        while True:
            message = input("")
            message_payload = {}

            if message.lower() == '/exit':
                message_payload = {"type": "exit", "payload": {"sender": sender, "room": room}}
                client_socket.send(json.dumps(message_payload).encode('utf-8'))
                break
            elif message.lower() == '/help':
                print("'/exit' to quit the chat")
                print("'/leave' to leave the room")
                print("'/connect' to connect to a room")
                print("'/help' to display available commands")
                print("/upload <path> to upload a file")
                print("/list to list all files in the room")
                print("/download <file_no> to download a file")
            elif not in_room:
                if message.lower() == '/connect':
                    in_room = True
                    sender = input("name: ")
                    room = input("room: ")
                    message_payload["type"] = "connect"
                    message_payload["payload"] = {}
                    message_payload["payload"]["sender"] = sender
                    message_payload["payload"]["room"] = room
                else:
                    print("You are not in a room. Type '/connect' to enter a room or '/help' to see commands.")
            elif in_room:
                if message.lower() == '/leave':
                    message_payload["type"] = "disconnect"
                    message_payload["payload"] = {}
                    message_payload["payload"]["sender"] = sender
                    message_payload["payload"]["room"] = room
                    sender = ""
                    room = ""
                    in_room = False
                elif message.lower() == '/connect':
                    print("You are already in a room. Type '/leave' to exit the room.")
                elif message.lower() == '/list':
                    message_payload["type"] = "list"
                    message_payload["payload"] = {}
                    message_payload["payload"]["sender"] = sender
                    message_payload["payload"]["room"] = room
                elif message.lower().split()[0] == '/upload':
                    try:
                        with open(message.split()[1], "rb") as file:
                            file_name = message.split()[1].split("/")[-1]
                            file_hash = hash_file(message.split()[1])
                            message_payload["type"] = "upload"
                            message_payload["payload"] = {}
                            message_payload["payload"]["sender"] = sender
                            message_payload["payload"]["room"] = room
                            message_payload["payload"]["file_name"] = file_name
                            message_payload["payload"]["file_hash"] = file_hash
                            client_socket.send(json.dumps(message_payload).encode('utf-8'))

                            encoded_image = base64.b64encode(open(message.split()[1], "rb").read()).decode("utf-8")
                            n = 0
                            file_id = sender + "@" + room + "@" + file_name + "@"
                            blob_size = 1024 - len(file_id)
                            while True:
                                blob = encoded_image[n * blob_size: (n + 1) * blob_size]
                                # print("Enc: ", len(blob))
                                # print("Blb: ", len(file_id + "@" + blob))
                                if blob == "":
                                    break
                                n += 1
                                client_socket.send((file_id + blob).encode("utf-8"))
                            sleep(0.5)
                            client_socket.send((file_id + "end").encode("utf-8"))
                            message_payload = {}
                    except FileNotFoundError:
                        print("File not found.")
                elif message.lower().split()[0] == '/download':
                    message_payload["type"] = "download"
                    message_payload["payload"] = {}
                    message_payload["payload"]["sender"] = sender
                    message_payload["payload"]["room"] = room
                    message_payload["payload"]["file_no"] = message.lower().split()[1]
                elif message[0] == '/':
                    print("Unknown command, type '/help' to see a list of available commands.")
                else:
                    message_payload["type"] = "message"
                    message_payload["payload"] = {}
                    message_payload["payload"]["sender"] = sender
                    message_payload["payload"]["room"] = room
                    message_payload["payload"]["text"] = message
            elif message.lower()[0] == '/':
                print("Unknown command, type '/help' to see a list of available commands.")

            if message_payload != {}:
                client_socket.send(json.dumps(message_payload).encode('utf-8'))

        client_socket.close()
    except UnicodeDecodeError as e:
        message_payload = {"type": "exit", "payload": {"sender": sender, "room": room}}
        client_socket.send(json.dumps(message_payload).encode('utf-8'))
        client_socket.close()
        raise e
    except TypeError as e:
        message_payload = {"type": "exit", "payload": {"sender": sender, "room": room}}
        client_socket.send(json.dumps(message_payload).encode('utf-8'))
        client_socket.close()
        raise e
    except IndexError as e:
        message_payload = {"type": "exit", "payload": {"sender": sender, "room": room}}
        client_socket.send(json.dumps(message_payload).encode('utf-8'))
        client_socket.close()
        raise e


def main():
    client_socket.connect((HOST, POST))
    print("Connected to {}:{}".format(HOST, POST))

    receive_thread = threading.Thread(target=receive_message)
    receive_thread.daemon = True
    receive_thread.start()

    send_thread = threading.Thread(target=send_message)
    send_thread.start()

    # TODO: Add file upload
    # TODO: Add file upload notification (client -> server -> clients)
    # TODO: Add file download
    # TODO: Add image file upload/download support


if __name__ == '__main__':
    main()
