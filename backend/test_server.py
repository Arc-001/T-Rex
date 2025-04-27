from com.server_socket import *

socket_server = socket_server()

while True:
    data = input("Enter message to send: ")
    print(socket_server.get_established_connections())
    if data.lower() == 'exit':
        break
    socket_server.send_all(data)
    print(f"Sent message: {data}")

