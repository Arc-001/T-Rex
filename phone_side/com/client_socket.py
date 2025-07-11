import socket
import threading
import os
import json

from com.encyption.key_gen import *
from com.SocketData import message_box

class socket_client:
    def __init__(self, host = "localhost", port = 5000, data_len = 3072, passcode= "test_passcode", hostname = os.getlogin()):
        self.data_len = data_len
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.post_box = message_box()
        self.key = None
        self.self_public_key = None

        print("----------------Checking for the PGP key----------------")


        #check the existance of the public and private key
        if os.path.exists('com/encryption/keys/rsa') and os.path.exists('com/encryption/keys/rsa.pub'):
            print("----------------Key found, now setting the attributes----------------")
            self.key = key_from_file('com/encryption/keys/rsa')
            
        else:
            #generate a new key
            print("----------------Key not found, makeing new key----------------")
            self.key = key(os.getlogin(), hostname, passcode)
            self.key.save_key('comm/encryption/keys/rsa')
        
        self.passcode = self.key.password
        self.hostname = self.key.hostname
        self.uuid = self.key.uuid
        self.self_public_key = self.key.get_public_key()
        self.self_private_key = self.key.get_private_key()

        print("----------------Key generated----------------")
        print ("----------------establishing connection----------------")
        establish_conn_thread = threading.Thread(target=self.establish_conn)
        establish_conn_thread.start()


    '''
    client to server -> connection request
    server to client -> connection accepted
    server to client -> message of public key of server
    client to server -> message of public key of client
    server to client -> success 1
    client to server -> success 2 
    -----stage 1 handshake competed----
    client to server -> json of username and password(encrypted)
    server (use private key of server to decrpt)
    server -> search the user to pass sqlite db 

    x:
    if match:
        server to client -> auth success
        conn moved to established conns

    else:
        server to client -> auth failed 
        goto x only 3 attempts
        conn closed

    ----- stage 2 auth handshake complete, conn established-----
    '''
    def auth_handshake(self):

        #sending the auth info / public key exchange

        print("---------------- Initiating the auth handshake(stage 1) ----------------")

        print("sending the pgp public key to server...")
        self.send_message(json.dumps({
            "type": "client_key_info",
            "uuid": self.uuid,
            "hostname": self.hostname,
            "passcode": self.passcode,
            "public_key": str(self.key.get_public_key())
        }))
        
        print("waiting for reception of the server public key...")
        recieved_data=self.post_box.get_msg_from_now()

        print(f"recieved data is {recieved_data}, now decoding it...")
        try:
            data = json.loads(recieved_data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return


        if data["type"] == "server_key_info":
            try:
                self.server_public_key = data["public_key"]
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                self.close_conn()
                return

            print(f"recieved server public key is {self.server_public_key}")
        
        #sending success to server
        print ("sending success handshake to server")
        self.send_message(encrypt_message(self.server_public_key, json.dumps({
            "type": "key_exchange_success"
        })))


        print("waiting for the success from server...")
        recieved_data=self.post_box.get_msg_from_now()
        data = json.loads(recieved_data)
        if data["type"] == "key_exchange_success":
            print("First handshake acknowledged by server")
        


        print("stage 1 key exchange has been executed successfully, now initiating the stage 2 authentication handshake")
        self.send_message(encrypt_message(self.server_public_key,str(json.dumps({
            "type": "client_auth_info",
            "uuid": self.uuid,
            "hostname": self.hostname,
            "password": self.passcode
        }))))
        data = json.loads(decrypt_message(self.self_private_key, self.post_box.get_msg_from_now()))
        if data["type"] == "server_auth_resp":
            if data["auth_status"] == "success":
                print("Authentication successful")
            elif data["auth_status"] == "failed":
                print("Authentication failed")
                self.close_conn()
                return



    def establish_conn(self):
        try:
            self.sock.connect((self.host, self.port))
            recv_thread = threading.Thread(target=self.recv_message_daemon)
            recv_thread.start()
            self.auth_handshake()
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
