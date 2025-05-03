from com.SocketData import post_office
import socket
import threading


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
    
    def get_established_connections(self):
        return self.addr_conn_dict
    
    def send_all(self, data:str):
        for addr in self.addr_conn_dict:
            self.send_message(addr, data)
    
    def wait_conn(self):
        while True:
            self.conn_semaphore.acquire()
            conn, addr = self.sock.accept()
            self.addr_conn_dict[tuple(addr)] = conn
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
            print(f"\n\n\nReceived message from {addr}: {data}")
            # if not data:
            #     self.close_conn(addr)
            #     print(f"Connection closed with {addr}")
            #     break
            self.post_office.add_recv_msg(addr, data)

    def send_message(self,addr, data:str):
        try:
            conn = self.addr_conn_dict[addr]
        except:
            raise socket.error("Connection not yet established")
        print (f"\n\nsending message to {addr}: {data}")
        conn.send(data.encode())
        self.post_office.add_send_msg(addr ,data)
    
    # def send_and_recv_blocking(self, addr, data:str):
    #     try:
    #         conn = self.addr_conn_dict[addr]
    #     except:
    #         raise socket.error("conn does not exisit")


    #     shared_buffer = []


    #     def send_and_recv_block(addr, data):
    #         self.send_message(addr, data)
    #         message_box_recv = self.post_office.get_msg_box(addr)
    #         return shared_buffer.append(data)
        
        
    #     child_blocked_thread = threading.Thread(target=send_and_recv_block, args=(addr, data))
    #     child_blocked_thread.start()
    #     child_blocked_thread.join()

    #     return shared_buffer[0]

    def get_msg_box(self, addr):
        return self.post_office.get_msg_box(addr)

    def get_recv_messages(self, addr):
        return self.post_office.get_msg_box(addr)
    
    def get_sent_messages(self, addr):
        return self.post_office.get_sent_msg_lst(addr)
    
    def get_recv_message(self, addr):
        return self.post_office.get_recv_msg_lst(addr)
    
    def get_post_office(self):
        return self.post_office