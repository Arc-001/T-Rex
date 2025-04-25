import socket
import threading

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

client_socket = socket.socket()  # instantiate
client_socket.connect((socket.gethostname(), 5000))  # connect to the server

def client_send():

    message = input(" -> ")  # take input
    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        message = input(" -> ")  # again take input

def client_receive():

    while True:
        data = client_socket.recv(1024).decode()  # receive response
        print('Received from server: ' + data)  # show in terminal
        if data.lower().strip() == 'bye':
            break
    client_socket.close()  # close the connection





if __name__ == '__main__':
    send = threading.Thread(target=client_send)
    receive = threading.Thread(target=client_receive)
    send.start()
    receive.start()
