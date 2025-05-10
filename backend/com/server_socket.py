from com.SocketData import post_office
import socket
import threading
import json
from com.encyption.key_gen import *

'''
client has 
- own public key
- own private key
- server public key


server hs
- own public key
- own private key

'''

class socket_server:
    def __init__(self, host = "0.0.0.0", port = 5000,max_listen = 2, data_len = 3072):
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

        self.self_public_key = None
        self.self_private_key = None

        print("----------------Checking for the PGP key----------------")


        #check the existance of the public and private key
        if os.path.exists('com/encryption/keys/rsa') and os.path.exists('com/encryption/keys/rsa.pub'):
            print("----------------Key found, now setting the attributes----------------")
            self.key = key_from_file('com/encryption/keys/rsa')
            
        else:
            #generate a new key
            print("----------------Key not found, makeing new key----------------")
            self.key = key(os.getlogin(), os.getlogin(), "server is the best thing in the world(pls change this thanks)")
            self.key.save_key('com/encryption/keys/rsa')
        
        self.passcode = self.key.password
        self.hostname = self.key.hostname
        self.uuid = self.key.uuid
        self.self_public_key = self.key.get_public_key()
        self.self_private_key = self.key.get_private_key()

        print("----------------Key generated----------------")

        #hashing and salting and sqlite db will be done later for now just hardcode the password
        self.uuid_pass_dict = {"arc":"test_passcode"}
        self.uuid_addr_pubkey_dict = {}
        # TODO: function to query csv or db and add it to the uuid_addr_pass_dict

        
    
    def get_established_connections(self):
        return self.addr_conn_dict
    
    def send_all(self, data:str):
        for addr in self.addr_conn_dict:
            self.send_message(addr, data)
    
    def auth_handshake(self,addr):
        #getting the conn object to have com
        conn = self.addr_conn_dict[addr]
        message_box = self.post_office.get_msg_box(addr)

        #reception of client public key
        client_recv = message_box.get_msg_from_now()
        client_data = json.loads(client_recv)
        temp_auth_dict = {}
        if client_data["type"] == "client_key_info":
            temp_auth_dict["uuid"] = client_data["uuid"]
            temp_auth_dict["hostname"] = client_data["hostname"]
            temp_auth_dict["passcode"] = client_data["passcode"]
            temp_auth_dict["public_key"] = client_data["public_key"]

        self.send_message(addr, json.dumps({
            "type": "server_key_info",
            "public_key": self.key.get_public_key()
        }))

        conf = json.loads(decrypt_message(self.self_private_key, message_box.get_msg_from_now()))
        if conf["type"] =="key_exchange_success":
            self.send_message(addr,json.dumps({
                "type":"key_exchange_success"
            }))
        else:
            conf.send_message(addr, json.dumps({
                "type":"key_exchange_failed"
            }))
            self.close_conn()

        print ("stage 1 handshake has been successfull, now starting stage 2")

        credentials = json.loads(decrypt_message(self.self_private_key, message_box.get_msg_from_now()))
        print(f"credentials are {credentials}")
        if credentials["type"] == "client_auth_info" and self.uuid_pass_dict[credentials["uuid"]] and credentials["password"] == self.uuid_pass_dict[credentials["uuid"]]:
            self.send_message(addr, encrypt_message(temp_auth_dict["public_key"],json.dumps({
                "type": "server_auth_resp",
                "auth_status": "success"
            })))
            #shift temp_auth_dict to uuid_addr_pubkey_dict
            self.uuid_addr_pubkey_dict[credentials["uuid"]] = (addr, temp_auth_dict["public_key"])
            print (f"Authentication successful for {addr}")
        else:
            self.send_message(addr, json.dumps({
                "type": "server_auth_resp",
                "auth_status": "failed"
            }))
            self.close_conn(addr)
            print(f"Connection closed with {addr} due to authentication failure")

    






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
            print("Starting authentication handshake")
            self.auth_handshake(addr)
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
