import threading
import queue

class message_box:
    def __init__(self):
        self.recv_messages = []
        self.recv_messages_cursor = -1
        self.send_messages = []
        self.send_messages_cursor = -1
        self.send_lock = threading.Lock()
        self.recv_lock = threading.Lock()
        self.redirect_now = False
        self.trigger_recv = threading.Event()

        self.shared_now_buffer = queue.Queue()
        self.shared_now_buffer_lock = threading.Lock()

    def add_recv_message(self, message : str):
        with self.recv_lock:
            self.recv_messages.append(message)
            if self.redirect_now:
                print("3) redirecting message to a shared buffer")
                with self.shared_now_buffer_lock:
                    self.shared_now_buffer.put(message)
                print("4) the trigger to the wait is released")
                self.trigger_recv.set()
                self.redirect_now = False
        
    def add_send_message(self, message):
        with self.send_lock:
            self.send_messages.append(message)
    
    def get_recv_message(self):
        with self.recv_lock:
            if self.recv_messages_cursor < len(self.recv_messages) - 1 and len(self.recv_messages)>0:
                self.recv_messages_cursor += 1
                return self.recv_messages[self.recv_messages_cursor]
            else:
                return None
    
    def get_send_message(self):
        with self.send_lock:
            if self.send_messages_cursor < len(self.send_messages) - 1 and len(self.send_messages)>0:
                self.send_messages_cursor += 1
                return self.send_messages[self.send_messages_cursor]
            else:
                return None
    
    def get_all_recv_messages(self):
        with self.recv_lock:
            return self.recv_messages
    
    def get_all_send_messages(self):
        with self.send_lock:
            return self.send_messages
    
    def set_sent_cursor(self, pos):
        with self.send_lock:
            if pos < len(self.send_messages) and pos >= 0:
                self.send_messages_cursor = pos
            else:
                raise IndexError("Cursor position out of range")
        
    def set_recv_cursor(self, pos):
        with self.recv_lock:
            if pos < len(self.recv_messages) and pos >= 0:
                self.recv_messages_cursor = pos
            else:
                raise IndexError("Cursor position out of range")
    
    def clear_recv_messages(self):
        with self.recv_lock:
            self.recv_messages = []
            self.recv_messages_cursor = -1
    
    def clear_send_messages(self):
        with self.send_lock:
            self.send_messages = []
            self.send_messages_cursor = -1

    def get_msg_from_now(self):
        print("1) event clearing")
        self.redirect_now = True
        self.trigger_recv.clear()
        print("2) event cleared now waiting")
        self.trigger_recv.wait()
        print("5) event triggered, now getting the message from shared buffer")
        with self.shared_now_buffer_lock:
            return self.shared_now_buffer.get()
            




class post_office:
    def __init__(self, no_of_letter_box:int):
        self.addr_msg_box = {}
        self.max_msg_box = no_of_letter_box

    
    def add_msg_box(self, addr):
        if len(self.addr_msg_box) < self.max_msg_box:
            self.addr_msg_box[addr] = message_box()
            return self.addr_msg_box[addr]

        else:
            raise Exception("Max number of message boxes reached")
        
    def remove_msg_box(self, addr):
        if addr in self.addr_msg_box:
            del self.addr_msg_box[addr]
        else:
            raise Exception("Message box not found")
        
    def get_msg_box(self, addr):
        try:
            return self.addr_msg_box[addr]
        except KeyError:
            raise Exception("Message box not found")

    def add_recv_msg(self, addr, message):
        addr_message_box = self.addr_msg_box[addr]
        addr_message_box.add_recv_message(message)

    def add_send_msg(self, addr, message):
        addr_message_box = self.addr_msg_box[addr]
        addr_message_box.add_send_message(message)

    def get_recv_msg_lst(self, addr):
        try:
            return self.addr_msg_box[addr].get_all_recv_messages()
        except:
            raise Exception(f"Address {addr} does not exist")
        
    def get_sent_msg_lst(self, addr):
        try:
            return self.addr_msg_box[addr].get_all_sent_messages()
        except:
            raise Exception(f"Address {addr} does not exist")
    
    def get_all_msg_box(self):
        return self.addr_msg_box
