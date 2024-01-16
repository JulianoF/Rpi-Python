
import socket
import threading
import numpy as np
import cv2 as cv

ip_addr = socket.gethostbyname(socket.gethostname())

# Set up the server socket
try: 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
except socket.error as e: 
    print ("Error creating socket: %s" % e) 
    exit(1)

try: 
    server_socket.bind(('192.168.0.28', 12345))  
    server_socket.listen(5)
except socket.error as e: 
    print ("Error Opening socket: %s" % e) 
    exit(1)
    
print(f"Server {ip_addr} listening on port 12345...")

# List to store client sockets
client_sockets = []
threadList = []

def handle_client(client_socket):
    while True:
        # Receive the size of the array
        size_bytes = client_socket.recv(4)
        array_size = int.from_bytes(size_bytes, byteorder='big')

        # Receive the array data
        array_bytes = bytearray()
        received_bytes = 0

        while received_bytes < array_size:
            chunk = client_socket.recv(min(4096, array_size - received_bytes))
            if not chunk:
                break
            array_bytes.extend(chunk)
            received_bytes += len(chunk)

        # Convert bytes back to NumPy array
        #received_array = np.frombuffer(array_bytes, dtype=np.int64).reshape((1080, 1920,3))
        frame_array = np.reshape(array_bytes,(1080,1920,3))
        print("Received array:")
        print(frame_array)

        # Display the resulting frame
        cv.imshow('Camera Feed', frame_array)
        if cv.waitKey(1) == ord('q'):
            break

        custom_data = "Uplink and Camera feed is good"
        client_socket.send(custom_data.encode('utf-8'))

    # Close the client socket when the connection is terminated
    print(f"Connection with {client_socket.getpeername()} closed.")
    client_socket.close()
    threadList.pop()
    cv.destroyAllWindows()

# Accept connections and start a new thread for each client
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")
    client_sockets.append(client_socket)

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    threadList.append(client_thread)
    client_thread.start()
    if threadList.count() == 0:
        server_socket.close()
        exit()
