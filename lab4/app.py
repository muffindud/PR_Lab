import socket
import signal
import sys
import threading
import json


# Define the server's IP address and port
HOST = '127.0.0.1'                              # IP address to bind to (localhost)
PORT = 8080                                     # Port to listen on

products = json.loads(open("products.json", "r").read())

# Create a socket that uses IPv4 and TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# Function to handle client requests
def handle_request(client_socket):
    # Receive and print the client's request data
    request_data = client_socket.recv(1024).decode('utf-8')
    # print(f"Received Request:\n{request_data}")

    # Parse the request to get the HTTP method and path
    request_lines = request_data.split('\n')
    request_line = request_lines[0].strip().split()
    path = request_line[1]

    # Initialize the response content and status code
    response_content = ''
    status_code = 200

    # Define a simple routing mechanism
    if path == '/':
        response_content = ("<p><a href='/about'>About</a></p>"
                            "<p><a href='/contacts'>Contacts</a></p>"
                            "<p><a href='/product'>Products</a></p>")
    elif path == '/about':
        response_content = 'This is the About page.'
    elif path == '/contacts':
        response_content = 'This is the Contacts page.'
    elif path[0:8] == '/product':
        prod_id = path[9:]
        if prod_id == "":
            for i in range(len(products)):
                response_content += "<a href ='/product/{id}'>{name}</a> <br>".format(
                    id=str(i),
                    name=products[i]['name']
                )
        else:
            try:
                prod_id = int(prod_id)
            except:
                response_content = "ID {id} is invalid.".format(id=prod_id)
                status_code = 404
            else:
                try:
                    product = products[prod_id]
                except IndexError:
                    response_content = "The product with the ID:{id} does not exist.".format(id=str(prod_id))
                    status_code = 404
                else:
                    response_content = (
                        "<p>Name: {name}</p>"
                        "<p>Author: {author}</p>"
                        "<p>Price: {price:.2f}</p>"
                        "<p>Description: {description}</p>"
                    ).format(
                        name=product["name"],
                        author=product["author"],
                        price=product["price"],
                        description=product["description"]
                    )
    else:
        response_content = '404 Not Found'
        status_code = 404

    # Prepare the HTTP response
    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'
    client_socket.send(response.encode('utf-8'))

    # Close the client socket
    client_socket.close()


# Function to handle Ctrl+C and other signals
def signal_handler(sig, frame):
    print("\nShutting down the server...")
    server_socket.close()
    server_socket.detach()
    sys.exit(0)


def main():
    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen(5)                     # Increased backlog for multiple simultaneous connections
    print(f"Server is listening on {HOST}:{PORT}")

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        # Accept incoming client connections
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        # Create a thread to handle the client's request
        client_handler = threading.Thread(target=handle_request, args=(client_socket,))
        client_handler.start()


if __name__ == '__main__':
    main()
