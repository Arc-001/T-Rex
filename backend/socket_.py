import socket
import threading

class server_socket:
    def __init__(self, host = socket.gethostname(), port = 5000, max_clients = 1):
        self.host = host
        self.port = port
        self.active_clients = 0
        self.connections = []
        self.addresses = []
        self.max_clients = max_clients

        # create a socket object

        try:
            self.server_soc = socket.socket() #default is AF_INET, SOCK_STREAM

            self.server_soc.bind((self.host, self.port))

            self.server_soc.listen(max_clients)
            print(f"Server started at {self.host}:{self.port}")

        except socket.error as e:
            print(f"Unable to create socket: {e}")
        

    def accept_client(self):
        try:
            conn, addr = self.server_soc.accept()
            print(f"Connection from: {addr}")
            self.active_clients += 1
            self.connections.append(conn)
            self.addresses.append(addr)
            return conn, addr
        except socket.error as e:
            print(f"Unable to accept client: {e}")
            return None, None
    
    def deny_client(self, conn):
        try:
            conn.close()
            self.active_clients -= 1
            print("Client disconnected")
        except socket.error as e:
            print(f"Unable to disconnect client: {e}")

    def get_connections(self):
        return self.connections
    
    def get_addresses(self):
        return self.addresses

    def recieve_data(self,conn):
        if conn in self.connections:
            try:
                data = conn.recv(1024).decode()
                return data
            except socket.error as e:
                print(f"Unable to receive data from : {e}")
                return None
        else:
            print("Connection not established")
            return None
        
    def send_data(self, conn, data):
        if conn in self.connections:
            try:
                conn.send(data.encode())
            except socket.error as e:
                print(f"Unable to send data to : {e}")
        else:
            print("Connection not established")
    
    def close(self):
        for conn in self.connections:
            conn.close()
        self.server_soc.close()
        print("Server closed")

class multithreaded_server_socket(server_socket):
    def __init__(self, host = socket.gethostname(), port = 5000, max_clients = 1):
        super().__init__(host, port, max_clients)
        self.threads = []

    def client_recieve(self, conn, addr):
        while True:
            data = self.recieve_data(conn)
            if not data:
                print(f"Client {addr} disconnected")
                self.deny_client(conn)
                break
            print(f"{addr} sent {data}")
            yield data
            
    def client_send(self, conn, addr, data):
        self.send_data(conn, data)
        print(f"Sent {data} to {addr}")
        yield data

    def multithreaded_duplex(self, conn, addr):
        persistant_reception = threading.Thread(target=self.client_recieve, args=(conn, addr))
        persistant_reception.start()
        self.threads.append(persistant_reception)
        while True:
            data = input("Enter data to send: ")
            self.client_send(conn, addr, data)
            if data == "!exit":
                break
    
def example():
    server = multithreaded_server_socket()
    conn, addr = server.accept_client()
    if conn:
        server.multithreaded_duplex(conn, addr)
    else:
        print("No connection established")
    server.close()

if __name__ == "__main__":
    example()


    

        



    







# def start_up():
#     host = socket.gethostname()
#     port = 5000

#     server_socket = socket.socket()  # get instance
#     # look closely. The bind() function takes tuple as argument
#     server_socket.bind((host, port))  # bind host address and port together

#     # configure how many client the server can listen simultaneously
#     server_socket.listen(2)
#     conn, address = server_socket.accept()  # accept new connection
#     print("Connection from: " + str(address))
#     while True:
#         # receive data stream. it won't accept data packet greater than 1024 bytes
#         data = conn.recv(1024).decode()
#         if not data:
#             # if data is not received break
#             break
#         print("from connected user: " + str(data))
#         data = input(' -> ')
#         conn.send(data.encode())  # send data to the client

#     conn.close()  # close the connection


# if __name__ == '__main__':
#     start_up()