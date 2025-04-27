import socket_

socket_server = socket_.socket_server()

while True:
    data = input("Enter message to send: ")
    print(socket_server.get_established_connections())
    if data.lower() == 'exit':
        break
    socket_server.send_all(data)
    print(f"Sent message: {data}")

