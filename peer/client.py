import json
import requests
import socket
import time
import sys,os
from os.path import abspath, dirname



current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from utils.manipulation import Piecify
from strategies.pieceSelectionAlgorithm import ClientInfo
from connection.peer import connect_to_peer




hasher= Piecify("D:/backend/p2p/peer-harbor/README.md",10)
piece_hashes, piece_indices=hasher._generate_piece_data()
print(piece_hashes,piece_indices)

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


# Example usage
tracker_url = "http://127.0.0.1:6969/announce"
info_hash = "another_random_hash"  # Replace with the actual info hash
peer_id = "abcdefghij0123456789"  # Replace with the actual peer ID
ip = "127.0.0.1"  # Replace with the actual IP address of your client
port = 6881  # Replace with the actual port number
uploaded = 0  # Replace with the actual amount uploaded by your client
downloaded = 0  # Replace with the actual amount downloaded by your client
left = 1024  # Replace with the actual amount left to download by your client

# peer_list = get_peer_list(tracker_url, info_hash, peer_id, ip, port, uploaded, downloaded, left)
# if peer_list:
#     print(f"Peer list from tracker: {peer_list.decode('utf-8')}")

connect_to_peer("127.0.0.1",6881)




