import socket
import threading

class message_box:
    def __init__(self):
        self.recv_messages = []
        self.recv_messages_cursor = -1
        self.send_messages = []
        self.send_messages_cursor = -1
        self.send_lock = threading.Lock()
        self.recv_lock = threading.Lock()

    def add_recv_message(self, message : str):
        with self.recv_lock:
            self.recv_messages.append(message)
        
    def add_send_message(self, message):
        with self.send_lock:
            self.send_messages.append(message)
    
    def get_recv_message(self):
        with self.recv_lock:
            if self.recv_messages_cursor < len(self.recv_messages) - 1 and len(self.recv_messages)>0:
                self.recv_messages_cursor += 1
                return self.recv_messages[self.recv_messages_cursor]
            else:
                return None
    
    def get_send_message(self):
        with self.send_lock:
            if self.send_messages_cursor < len(self.send_messages) - 1 and len(self.send_messages)>0:
                self.send_messages_cursor += 1
                return self.send_messages[self.send_messages_cursor]
            else:
                return None
    
    def get_all_recv_messages(self):
        with self.recv_lock:
            return self.recv_messages
    
    def get_all_send_messages(self):
        with self.send_lock:
            return self.send_messages
    
    def set_sent_cursor(self, pos):
        with self.send_lock:
            if pos < len(self.send_messages) and pos >= 0:
                self.send_messages_cursor = pos
            else:
                raise IndexError("Cursor position out of range")
        
    def set_recv_cursor(self, pos):
        with self.recv_lock:
            if pos < len(self.recv_messages) and pos >= 0:
                self.recv_messages_cursor = pos
            else:
                raise IndexError("Cursor position out of range")
    
    def clear_recv_messages(self):
        with self.recv_lock:
            self.recv_messages = []
            self.recv_messages_cursor = -1
    
    def clear_send_messages(self):
        with self.send_lock:
            self.send_messages = []
            self.send_messages_cursor = -1



class post_office:
    def __init__(self, no_of_letter_box:int):
        self.addr_msg_box = {}
        self.max_msg_box = no_of_letter_box

    
    def add_msg_box(self, addr):
        if len(self.addr_msg_box) < self.max_msg_box:
            self.addr_msg_box[addr] = message_box()
            return self.addr_msg_box[addr]

        else:
            raise Exception("Max number of message boxes reached")
        
    def remove_msg_box(self, addr):
        if addr in self.addr_msg_box:
            del self.addr_msg_box[addr]
        else:
            raise Exception("Message box not found")
        
    def get_msg_box(self, addr):
        try:
            return self.addr_msg_box[addr]
        except KeyError:
            raise Exception("Message box not found")
        
    def get_all_msg_box(self):
        return self.addr_msg_box
        
    

    
    def get_message_box(self, )

# class socket_server:
#     def __init__(self, host = "localhost", port = 5000,max_listen = 2):
#         self.host = host
#         self.port = port
#         self.sock = socket.socket()
#         self.sock.bind((self.host,self.port))
#         self.sock.listen(max_listen)
#         self.max_listen = max_listen
#         self.post_office = post_office(max_listen)
#         self.addr_conn_dict = {}
#         self.conn_semaphore = threading.Semaphore(max_listen)
#         wait_conn_thread = threading.Thread(target=self.wait_conn)
#         wait_conn_thread.start()
    
#     def wait_conn(self):
#         while True:
#             self.conn_semaphore.acquire()
#             conn, addr = self.sock.accept()
#             self.addr_conn_dict[addr] = conn
#             print(f"{addr} connected")
#             self.post_office.add_msg_box(addr)
#             print(f"{addr} message box created")
#             recv_thread = threading.Thread(target=self.recv_message_daemon, args=(conn, addr))
#             send_thread = threading.Thread(target=self.send_message_daemon, args=(conn, addr))
#             recv_thread.start()
#             send_thread.start()
#             print(f"{addr} recv and send thread started")

    
#     def recv_message()




