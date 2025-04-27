import socket
import threading
from com.SocketData import message_box


class socket_client:
    def __init__(self, host = "localhost", port = 5000, data_len = 1024):
        self.data_len = data_len
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.post_box = message_box()
        establish_conn_thread = threading.Thread(target=self.establish_conn)
        establish_conn_thread.start()


    def establish_conn(self):
        try:
            self.sock.connect((self.host, self.port))
            recv_thread = threading.Thread(target=self.recv_message_daemon)
            recv_thread.start()
        except socket.error as e:
            raise e
        
    def recv_message_daemon(self):
        try:
            while True:
                data = self.sock.recv(self.data_len).decode()
                print(f"Received message: {data}")
                if not data:

                    #call the gracefull closing of connection

                    break

                self.post_box.add_recv_message(data)

        except socket.error as e:
            raise e
        
    def send_message(self, data:str):
        try:
            self.sock.send(data.encode())
            self.post_box.add_send_message(data)
        except Exception as e:
            print(f"error sending the message: {data}\n error is : {e}")
    
    def close_conn(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print("\n\n\n Error during shutdown of socket")
        finally:
            self.sock.close()
            print("Socket closed")
    
    def get_recv_messages(self):
        return self.post_box.get_recv_message()
    
    def get_sent_messages(self):
        return self.post_box.get_send_message()
    
    def get_all_recv_messages(self):
        return self.post_box.get_all_recv_messages()
    
    def get_all_sent_messages(self):
        return self.post_box.get_all_send_messages()
    
    def get_post_box(self):
        return self.post_box
