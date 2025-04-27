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

    def add_recv_msg(self, addr, message):
        addr_message_box = self.addr_msg_box[addr]
        addr_message_box.add_recv_message(message)

    def add_send_msg(self, addr, message):
        addr_message_box = self.addr_msg_box[addr]
        addr_message_box.add_send_message(message)

    def get_recv_msg_lst(self, addr):
        try:
            return self.addr_msg_box[addr].get_all_recv_messages()
        except:
            raise Exception(f"Address {addr} does not exist")
        
    def get_sent_msg_lst(self, addr):
        try:
            return self.addr_msg_box[addr].get_all_sent_messages()
        except:
            raise Exception(f"Address {addr} does not exist")
    
    def get_all_msg_box(self):
        return self.addr_msg_box
        
class socket_server:
    def __init__(self, host = "localhost", port = 5000,max_listen = 2, data_len = 1024):
        self.data_len = data_len
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.sock.bind((self.host,self.port))
        self.sock.listen(max_listen)
        self.max_listen = max_listen
        self.post_office = post_office(max_listen)
        self.addr_conn_dict = {}
        self.conn_semaphore = threading.Semaphore(max_listen)
        wait_conn_thread = threading.Thread(target=self.wait_conn)
        wait_conn_thread.start()
    
    def wait_conn(self):
        while True:
            self.conn_semaphore.acquire()
            conn, addr = self.sock.accept()
            self.addr_conn_dict[addr] = conn
            print(f"{addr} connected")
            self.post_office.add_msg_box(addr)
            print(f"{addr} message box created")
            recv_thread = threading.Thread(target=self.recv_message_daemon, args=(addr,))
            # send_thread = threading.Thread(target=self.send_message_daemon, args=(conn, addr))
            recv_thread.start()
            # send_thread.start()
            print(f"{addr} recv and send thread started")
    
    def close_conn(self, addr):
        self.addr_conn_dict[addr].close()
        print(f"{addr} connection closed")
        del self.addr_conn_dict[addr]
        self.post_office.remove_msg_box(addr)
        print(f"{addr} message box removed")
        self.conn_semaphore.release()
        print(f"{addr} semaphore released")

    def close_server(self):
        #closing all the sockets
        for addr, conn in self.addr_conn_dict.items():
            try:
                conn.shutdown(socket.SHUT_RDWR)
            except Exception as e:
                print(f"Unable to send the shutdown signal to {addr}\n\n Error : {e}")
            finally:
                conn.close()
                print(f"Connection with {addr} closed")

        #clearing dictionary
        self.addr_conn_dict.clear()

        #releasing all the semaphores
        while self.conn_semaphore._value < self.max_listen:
            self.conn_semaphore.release()




    def recv_message_daemon(self, addr):
        while True:
            conn = self.addr_conn_dict[addr]
            data = conn.recv(self.data_len).decode()
            if not data:
                self.close_conn(addr)
                print(f"Connection closed with {addr}")
                break
            self.post_office.add_recv_msg(addr, data)

    def send_message(self,addr, data:str):
        try:
            conn = self.addr_conn_dict[addr]
        except:
            raise socket.error("Connection not yet established")
        conn.send(data.encode())
        self.post_office.add_send_msg(addr ,data)

    def get_recv_messages(self, addr):
        return self.post_office.get_msg_box(addr)
    
    def get_sent_messages(self, addr):
        return self.post_office.get_sent_msg_lst(addr)
    
    def get_recv_message(self, addr):
        return self.post_office.get_recv_msg_lst(addr)
    
    def get_post_office(self):
        return self.post_office
    
class socket_client:
    def __init__(self, host = "localhost", port = 5000, data_len = 1024):
        self.data_len = data_len
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.post_box = message_box()
        self.establish_conn()

    def establish_conn(self):
        try:
            self.sock.connect((self.host, self.port))
            recv_thread = threading.Thread(target=self.recv_message_daemon)
        except socket.error as e:
            raise e
        
    def recv_message_daemon(self):
        try:
            while True:
                data = self.sock.recv(self.data_len).decode()
                if not data:

                    #call the gracefull closing of connection

                    break

                self.post_box.add_recv_message(data)

        except socket.error as e:
            raise e
        
    def send_message(self, data:str):
        try:
            self.sock.send(data.encode())
            self.message_box.add_send_message(data)
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
    





