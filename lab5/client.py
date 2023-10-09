import socket
import threading
import json


# Host parameters
HOST = '127.0.0.1'
POST = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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

    # TODO: Add connect_ack handling
    while True:
        message = input("")
        message_payload = {}

        if message.lower() == '/exit':
            message_payload = {"type": "exit", "payload": {}}
            break
        elif message.lower() == '/help':
            print("'/exit' to quit the chat")
            print("'/leave' to leave the room")
            print("'/connect' to connect to a room")
            print("'/help' to display available commands")
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
                print("You are not in a room. Type '/connect' to enter a room.")
        elif in_room:
            if message.lower() == '/leave':
                # TODO: Leave the room
                message_payload["type"] = "disconnect"
                message_payload["payload"] = {}
                message_payload["payload"]["sender"] = sender
                message_payload["payload"]["room"] = room
                sender = ""
                room = ""
                in_room = False
            elif message.lower() == '/connect':
                print("You are already in a room. Type '/leave' to exit the room.")
            else:
                message_payload["type"] = "message"
                message_payload["payload"] = {}
                message_payload["payload"]["sender"] = sender
                message_payload["payload"]["room"] = room
                message_payload["payload"]["text"] = message
        elif message.lower()[0] == '/':
            print("Unknown command, type '/help' to see a list of available commands.")

        client_socket.send(json.dumps(message_payload).encode('utf-8'))

    client_socket.close()


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
