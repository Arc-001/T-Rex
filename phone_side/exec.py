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
    

#-------------------- Helper Functions --------------------#
def exec_arb(command_lst):
    return Output(subprocess.run(command_lst, capture_output=True, text=True, check= True))

#-------------------- Battery commands --------------------#
def batt_stat():
    result = exec_arb(["termux-battery-status"])
    return result
    

#-------------------- Call commands --------------------#
def call_log(limit,offset):
    result = exec_arb(["termux-call-log", "-l", f"{limit}", "-o", f"{offset}"])
    return result

def contact_list():
    result = exec_arb(["termux-contact-list"])
    return result

#-------------------- Clipboard Commands --------------------#
def termux_clipboard_get():
    result = exec_arb(["termux-clipboard-get"])
    return result

def termux_clipboard_set(data):
    result = exec_arb(["termux-clipboard-set", data])
    return result

#-------------------- Wifi commands --------------------#
def termux_wifi_scan():
    result = exec_arb(["termux-wifi-scaninfo"])
    return result


##-------------------- location commands --------------------#
def termux_location_gps():
    result = exec_arb(["termux-location","-p","gps"])
    return result

def termux_location_network():
    result = exec_arb(["termux-location", "-p", "network"])
    return result


#-------------------- Download Commands --------------------#
def termux_download(url,path, requeest_title="download request", request_body="a download request was initiated"):
    result =  exec_arb(["termux-download","-d", request_body,"-t", requeest_title,"-p", path, url])
    return result


#-------------------- Imput Commands --------------------#
def prompt_input(title = "Enter Input"):
    result = exec_arb(["termux-dialog", "text","-t", title])
    return result


#-------------------- Media playback commands --------------------#
def current_media_info():
    result = exec_arb(["termux-media-player","info"])
    return result

def play_media():
    result = exec_arb(["termux-media-player","play"])
    return result

def pause_media():




