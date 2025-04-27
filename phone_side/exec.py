import os
import time
import subprocess
import json

class Output:
    def __init__(self, run_obj):
        self.returncode = run_obj.returncode
        self.stdout = run_obj.stdout
        self.stderr = run_obj.stderr
    
    def __str__(self):
        '''
        Return JSON
        '''
        dict = {
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr
        }
        return json.dumps(dict)
    
    def get_json(self):
        '''
        Return JSON
        '''
        dict = {
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr
        }
        return dict
    


def exec_arb(command_lst):
    return Output(subprocess.run(command_lst, capture_output=True, text=True, check= True))

def batt_stat():
    result = exec_arb(["termux-battery-status"])
    return result
    

def call_log(limit,offset):
    result = exec_arb(["termux-call-log", "-l", f"{limit}", "-o", f"{offset}"])
    return result

def termux_clipboard_get():
    result = exec_arb(["termux-clipboard-get"])
    return result

def termux_clipboard_set(data):
    result = exec_arb(["termux-clipboard-set", data])
    return result

def termux_wifi_scan():
    result = exec_arb(["termux-wifi-scaninfo"])
    return result

def termux_location_gps():
    result = exec_arb(["termux-location","-p","gps"])
    return result

def termux_location_network():
    result = exec_arb(["termux-location", "-p", "network"])
    return result
