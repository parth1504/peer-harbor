import json
import requests
import socket
import time
import sys,os
from os.path import abspath, dirname

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)
sys.path.append("D:/backend/p2p/peer-harbor")

from utils.manipulation import Piecify

# Example usage:
client_info = ClientInfo()
client_info.create_file_info("text",7)
print(client_info.get_file_bitfield("text"))



def receive_file(conn, file_path):
    with open(file_path, 'wb') as file:
        chunk_size = 10
        data = conn.recv(chunk_size)

        while data:
            file.write(data)
            data = conn.recv(chunk_size)

def send_file(conn, file_path):
    with open(file_path, 'rb') as file:
        chunk_size = 10
        data = file.read(chunk_size)

        while data:
            conn.send(data)
            data = file.read(chunk_size)
            print("sahil gay")