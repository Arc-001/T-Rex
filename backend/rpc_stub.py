from com.server_socket import *
import time
from concurrent.futures import ThreadPoolExecutor



class RPC_Stub_server:
    def __init__(self, sock_obj:socket_server):
        self.sock = sock_obj
    
    def sync_recv(self, addr):
        self.sock.get_msg_box(addr).get_msg_from_now()

    def recieve_all_now(self):
        msg_box_list = self.sock.get_post_office().get_all_msg_box()   
        # this is a addr -> msg for each message recieved after execution of the rpc
        shared_recv_buffer = {}
                 
        with ThreadPoolExecutor(max_workers = len(msg_box_list)) as exec:
            def get_and_push_buffer(addr):
                shared_recv_buffer[addr]= self.sock.get_msg_box(addr).get_msg_from_now()
            exec.map(get_and_push_buffer, msg_box_list.keys())
        
        for addr in msg_box_list.keys():
            print(f"{addr} has given the response of {shared_recv_buffer[addr]}")

        
        return shared_recv_buffer
    


    def bat_status_all(self):
        """
        Stub for remote procedure call to get all battery status information.
        """

        self.sock.send_all("batt_stat()")
        resp = self.recieve_all_now()
        return resp
    
    def call_log_all(self, limit,offset):
        """
        Stub for RPC to get call log
        """

        self.sock.send_all(f"call_log({limit},{offset})")
        resp = self.recieve_all_now()
        return resp
    
    def contact_list(self):
        """
        Stub for RPC to get contact list
        """
        self.sock.send_all(f"contact_list()")
        resp = self.recieve_all_now()
        return resp
    
    def termux_clipboard_set_all(self,data):
        '''
        Stub for RPC to set the clipboard of the remote device
        '''
        self.sock.send_all(f"termux_clipboard_set({data})")
        resp = self.recieve_all_now()
        return resp
    
    def termux_clipboard_get_all(self):
        self.sock.send_all(f"termux_clipboard_get()")
        resp = self.recieve_all_now()
        return resp
    
    def termux_wifi_scan_all(self):
        self.sock.send_all(f"termux_wifi_scan()")
        resp = self.recieve_all_now()
        return resp
    
    def termux_location_gps_all(self):
        self.sock.send_all("termux_location_gps()")
        resp = self.recieve_all_now()
        return resp
    
    def termux_location_network_all(self):
        self.sock.send_all("termux_location_network()")
        resp = self.recieve_all_now()
        return resp

    def termux_download_all(self, url:str, path , request_title="download request", request_body="a download request was initiated"):
        self.sock.send_all(f"termux_download({url},{path},{request_title},{request_body})")
        resp = self.recieve_all_now()
        return resp
    
    def prompt_input_all(self, title = "Enter Input"):
        self.sock.send_all(f"prompt_input({title})")
        resp = self.recieve_all_now()
        return resp
    
    def current_media_info(self):
        self.sock.send_all(f"current_media_info()")
        resp = self.recieve_all_now()
        return resp
    
    def play_media(self):
        self.sock.send_all("play_media()")
        resp = self.recieve_all_now()
        return resp
    
    def play_file(self, path):
        self.sock.send_all(f"play_file({path})")
        resp = self.recieve_all_now()
        return resp
    
    def pause_media(self):
        self.sock.send_all(f"pause_media()")
        resp = self.recieve_all_now()
        return resp
    
    def stop_media(self):
        self.sock.send_all("stop_media()")
        resp = self.recieve_all_now()
        return resp
    
    
sock = socket_server()
print ("sending to sleep for 10 sec, connect the debugging client quickly !!!")
time.sleep(10)
rpc_stub = RPC_Stub_server(sock)
print("Server started")
resp = rpc_stub.bat_status_all()
print(f"final response from all the devices is {resp}")
