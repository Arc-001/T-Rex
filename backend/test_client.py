from com.client_socket import *

sock = socket_client()

while True:
    try:
        data = input("Enter message to send: ")
        if data.lower() == 'exit':
            break
        sock.send_message(data)
        print(f"Sent message: {data}")
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"An error occurred: {e}")