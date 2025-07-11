from flask import Flask, jsonify, request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from rpc_stub import RPC_Stub_server
from com.server_socket import socket_server
from server import *
import os
from time import sleep
import uvicorn

app = FastAPI()
rpc_caller = start_server()
server_sock = rpc_caller.get_server_sock()
# CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)



@app.get("/api/bat_status_all")
def bat_status()->json:
    response = rpc_caller.bat_status_all()
    return response

@app.get("/api/connected_devices")
def connected_devices()->json:
    response = server_sock.addr_conn_dict
    return jsonify(response)

@app.get("/api/clipboard_get_all")
def clipboard_get()->json:
    response = rpc_caller.termux_clipboard_get_all()
    return response

@app.get("/api/wifi_scan_all")
def wifi_scan()->json:
    response = rpc_caller.termux_wifi_scan_all()
    return response

@app.post("/api/clipboard_set_all")
def clipboard_set()->json:
    data = request.json.get("data", "")
    response = rpc_caller.termux_clipboard_set_all(data)
    return response

if __name__ == "__main__":

    uvicorn.run(app, 
                host="0.0.0.0",
                port = 8000,
                log_level="info",
                reload=True,
                workers=1)









# app = Flask(__name__)
# api = app.blueprint('api', __name__)

# #getting the rpc caller
# rpc_caller = start_server()






