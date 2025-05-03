from com.server_socket import *

socket_server = socket_server()

while True:

    data = input("Enter message to send: ")
    print(socket_server.get_established_connections())
    for addr in socket_server.get_established_connections():
        print(f"Sending to {addr}")
        socket_server.send_message(addr, data)
        print(f"Sent message: {data}")
        msg_box = socket_server.get_msg_box(addr)
        recv = msg_box.get_msg_from_now()
        print(f"recieved data{recv}")




