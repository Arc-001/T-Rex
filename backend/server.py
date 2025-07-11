from rpc_stub import *
from com.server_socket import *
from com.SocketData import *

def start_server():
    print("----------------- Initializing the server -----------------")
    sock_server = socket_server(host="0.0.0.0", port=5000, max_listen=2, data_len=3072)

    sleep(1) 

    print("----------------server running on port 5000, starting the remote call stub...}-------------------")
    remote_call = RPC_Stub_server(sock_server)

    print("----------------- Server is ready to accept remote calls -----------------")
    return remote_call



