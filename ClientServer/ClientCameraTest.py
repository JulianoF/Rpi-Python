
import sys
import socket
import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot Open Camera, a Failure has Occured")
    exit()

# Set up the client socket
try: 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
except socket.error as e: 
    print ("Error creating socket: %s" % e) 
    sys.exit(1)
    
server_address = (sys.argv[1], 12345)  

# Connect to the server
try: 
    client_socket.connect(server_address)
except socket.error as e: 
    print ("Error Connecting to Server: %s" % e) 
    sys.exit(1)

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
    frameBytes = frame.tobytes()

    client_socket.sendall(len(frameBytes).to_bytes(4, byteorder='big'))
    client_socket.sendall(frameBytes)

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
