import socket
import threading


# Host parameters
HOST = '127.0.0.1'
PORT = 8080

# List of active clients
clients = []


# Client handler
def handle_client(client_socket, client_address):
    print("Accepted connection from {}:{}".format(*client_address))

    while True:
        message = client_socket.recv(1024).decode('utf-8')

        if not message:
            break

        print("Received message from {}: {}".format(client_address, message))

        for client in clients:
            if client != client_socket:
                client.send(message.encode('utf-8'))

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
