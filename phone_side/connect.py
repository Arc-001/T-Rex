from com import client_socket
from com import SocketData
import json
import os
import exec_commands as e
from dotenv import load_dotenv

def load_env():
    """
    Gets the values from the local .env files and 
    returnes the value as

    ------------------
    host, port, password
    -------------------
    """
    load_dotenv()
    host = os.getenv("REMOTE_HOST")
    port = int(os.getenv("REMOTE_PORT"))
    password_for_conn = os.getenv("PASSWORD")
    return host, port, password_for_conn



def execute_api_commands(raw_command:str):
    try:
        while True:
            msg = sock.get_post_box()
            result = eval(f"e.{msg.get_msg_from_now()}")
            sock.send_message(str(result))
    except Exception as e:
        sock.send_messge(json.dumps({
            "returncode": 1 ,
            "stdout": "",
            "stderr": ""
        }))




if __name__=="__main__":
    #making the client socket(auto establish connection)
    host, port, password = load_env()
    sock = client_socket.socket_client(host = host, port = port, passcode = password)
    while True:

