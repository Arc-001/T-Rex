from com.server_socket import *
import time
from concurrent.futures import ThreadPoolExecutor



class RPC_Stub_server:
    def __init__(self, sock_obj:socket_server):
        self.sock = sock_obj
    
    def sync_recv(self, addr):
        self.sock.get_msg_box(addr).get_msg_from_now()

    def bat_status_all(self):
        """
        Stub for remote procedure call to get all battery status information.
        """

        self.sock.send_all("batt_stat()")
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
    


sock = socket_server()
print ("sending to sleep for 10 sec, connect the debugging client quickly !!!")
time.sleep(10)
rpc_stub = RPC_Stub_server(sock)
print("Server started")
resp = rpc_stub.bat_status_all()
print(f"final response from all the devices is {resp}")
