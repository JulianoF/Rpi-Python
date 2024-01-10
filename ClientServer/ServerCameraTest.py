import socket
import threading
import numpy as np
import cv2 as cv

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind(('192.168.0.28', 12345))  
server_socket.listen(5)

print("Server listening on port 12345...")

# List to store client sockets
client_sockets = []

def handle_client(client_socket):
    while True:
        # Receive data from the client
        data = client_socket.recv(8192)
        if not data:
            break
        #print(f"Received from {client_socket.getpeername()}: {data.decode('utf-8')}")

        # Display the resulting frame
        cv.imshow('Camera Feed', data)
        if cv.waitKey(1) == ord('q'):
            break

        custom_data = "Uplinka and Camera feed is good"
        client_socket.send(custom_data.encode('utf-8'))

    # Close the client socket when the connection is terminated
    print(f"Connection with {client_socket.getpeername()} closed.")
    client_socket.close()
    cv.destroyAllWindows()

# Accept connections and start a new thread for each client
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")
    client_sockets.append(client_socket)

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
