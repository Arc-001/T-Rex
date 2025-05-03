from com import client_socket
from com import SocketData
import exec_commands as e

sock = client_socket.socket_client()
try:
    while True:
        msg = sock.get_post_box()
        result = eval(f"e.{msg.get_msg_from_now()}")
        sock.send_message(str(result))
except:
    print("closing conn")
finally:
    sock.close_conn()

