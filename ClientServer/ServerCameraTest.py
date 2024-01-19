
import socket
import threading
import numpy as np
import cv2 as cv

from ultralytics import YOLO

# Load a COCO-pretrained YOLOv8n model
model = YOLO('../YOLOmodels/yolov8n.pt')

# Display model information (optional)
model.info()

##############################################################
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
        frame_array = np.reshape(array_bytes,(480,640,3)) #Use for testing on mylaptop
        #frame_array = np.reshape(array_bytes,(1080,1920,3))
        
        #print("Received array:")
        #print(frame_array)
        ################ YOLOv8
        yolo_predicitons = model(frame_array, stream=True)
        # Process results generator
        for result in yolo_predicitons:
            boxes = result.boxes  # Boxes object for bbox outputs
            probs = result.probs  # Probs object for classification outputs
            classes = result.names
        draw_boxes(frame_array,boxes,probs,classes)
        ################################
        
        ##### HAAR CASCASE TEST
        face_rect = face_cascade.detectMultiScale(frame_array, 
                                              scaleFactor = 1.2, 
                                              minNeighbors = 5)
        for (x, y, w, h) in face_rect:
            cv.rectangle(frame_array, (x, y), 
                      (x + w, y + h), (250, 220, 255), 4)               
        ##########################
        
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


def draw_boxes(image, boxes, scores, class_names): #class_ids, scores, class_names):
    for i, box in enumerate(boxes):
        x, y, w, h = box
        color = (0, 255, 0)  # Green color for the bounding box
        label = "object"#f"{class_names[class_ids[i]]}: {scores[i]:.2f}"
        cv.rectangle(image, (int(x), int(y)), (int(x + w), int(y + h)), color, 2)
        cv.putText(image, label, (int(x), int(y) - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
##############################################################


ip_addr = socket.gethostbyname(socket.gethostname())

try:
    face_cascade = cv.CascadeClassifier('../cascades/haarcascade_frontalface_default.xml')
except cv.error as e:
    print("Error Opening Cascade Data: %s" % e)
    exit(1)
    
# Set up the server socket
try: 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
except socket.error as e: 
    print ("Error creating socket: %s" % e) 
    exit(1)

try: 
    server_socket.bind(('10.160.22.152', 12345))  # Change based on location
    server_socket.listen(5)
except socket.error as e: 
    print ("Error Opening socket: %s" % e) 
    exit(1)
    
print(f"Server {ip_addr} listening on port 12345...")

# List to store client sockets
client_sockets = []
threadList = []

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
