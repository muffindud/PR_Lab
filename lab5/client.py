import socket
import threading


# Host parameters
HOST = '127.0.0.1'
POST = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def receive_message():
    while True:
        message = client_socket.recv(1024).decode('utf-8')

        if not message:
            break

        print("Received: {}".format(message))


def main():
    client_socket.connect((HOST, POST))
    print("Connected to {}:{}".format(HOST, POST))

    receive_thread = threading.Thread(target=receive_message)
    receive_thread.daemon = True
    receive_thread.start()

    while True:
        message = input("('exit' to quit)> ")

        if message.lower() == 'exit':
            break

        client_socket.send(message.encode('utf-8'))

    client_socket.close()


if __name__ == '__main__':
    main()
