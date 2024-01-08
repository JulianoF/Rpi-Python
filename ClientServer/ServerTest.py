import socket
import threading

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.0.28', 12345))  # Replace 'your_desktop_ip' with your desktop's IP address
server_socket.listen(5)

print("Server listening on port 12345...")

# List to store client sockets
client_sockets = []

def handle_client(client_socket):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received from {client_socket.getpeername()}: {data.decode('utf-8')}")

        # Send a response back to the client
        response = "Message received by the server!"
        client_socket.send(response.encode('utf-8'))

    # Close the client socket when the connection is terminated
    client_socket.close()
    print(f"Connection with {client_socket.getpeername()} closed.")

# Accept connections and start a new thread for each client
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")
    client_sockets.append(client_socket)

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
