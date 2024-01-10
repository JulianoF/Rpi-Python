import socket
import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot Open Camera, a Failure has Occured")
    exit()

# Set up the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.0.28', 12345)  

# Connect to the server
client_socket.connect(server_address)
print(f"Connected to {server_address}")

while True:

    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Send custom data to the server
    print("Sending Frame To Server.")
    
    client_socket.send(frame)

    # Receive a response from the server
    response = client_socket.recv(1024)
    print(f"Server response: {response.decode('utf-8')}")
    #if response.decode('utf-8') == "quit":
    #    break
    if cv.waitKey(1) == ord('q'):
        break

# Close the connection
client_socket.close()
cap.release()
cv.destroyAllWindows()