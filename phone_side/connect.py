from com import client_socket
from com import SocketData
import json
import os
import exec_commands as e
from dotenv import load_dotenv
import time

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
            print(f"executing command {raw_command}")
            result = eval(f"e.{raw_command}")
    except Exception as e:
        return (json.dumps({
            "returncode": -1 ,
            "stdout": "",
            "stderr": ""
        }))




if __name__=="__main__":
    #making the client socket(auto establish connection)
    host, port, password = load_env()
    sock = client_socket.socket_client(host = host, port = port, passcode = password)
    time.sleep(2)
    message_box = sock.get_post_box()
    while True:
        print("pre")
        command = message_box.get_msg_from_now()
        print("Post")

        
        #TODO: add a level of indirection in checking what type of command has been sent


        try:
            ans = execute_api_commands(command)
            sock.send_message(str(ans))
        except:
            #talk about laughable error handling
            continue
            
