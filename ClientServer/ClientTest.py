import socket

# Set up the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.0.10', 12345)  # Replace 'your_desktop_ip' with your desktop's IP address

# Connect to the server
client_socket.connect(server_address)
print(f"Connected to {server_address}")

while True:
    # Send custom data to the server
    custom_data = input("Enter message to send: ")
    client_socket.send(custom_data.encode('utf-8'))

    # Receive a response from the server
    response = client_socket.recv(1024)
    print(f"Server response: {response.decode('utf-8')}")

# Close the connection
client_socket.close()
