# server.py

import socket
import threading
import config
from devicedata import parse_and_insert_data

def handle_client(client_socket, client_address):
    print(f"New connection established: {client_address}")
    while True:
        try:
            # Receive data from the client
            raw_message = client_socket.recv(2048)
            message = raw_message.decode('utf-8')
            if not message:
                break
            print("Handle client about to call parse_and_insert")
            #print(f"Received raw XML from {client_address}:\n {message}")
            # Parse and insert the data client_socket.recv(2048)
            response_xml = parse_and_insert_data(raw_message)
            # Send the response back to the client
            client_socket.send(response_xml.encode('utf-8'))
        except ConnectionResetError:
            break
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break

    # Close the client socket
    client_socket.close()
    print(f"Connection closed: {client_address}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(config.SERVER_HOST, config.SERVER_PORT)
    server_socket.bind((config.SERVER_HOST, config.SERVER_PORT))
    server_socket.listen(5)
    print(f"Server started, listening on {config.SERVER_HOST}:{config.SERVER_PORT}")

    while True:
        # Accept a new client connection
        client_socket, client_address = server_socket.accept()
        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    start_server()
