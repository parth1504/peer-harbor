import hashlib
import json,os,socket,sys,time
import struct

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from utils.manipulation import Piecify
from connection.peer import PeerConnection, close_connection
from upload.Seed import send_pieces

def start_server(ip, port):
    hasher= Piecify("./output.torrent",20)
    pieces, piece_hashes, piece_indices=hasher._generate_piece_data()
    
    client = PeerConnection(ip, port)
    
    client_socket, client_address, server_socket = client.seed_connection()
    send_pieces(client_socket, piece_indices, pieces)
    close_connection(client_socket)
    close_connection(server_socket)

if __name__ == "__main__":
    server_ip = "127.0.0.1"
    server_port = 6881
    start_server(server_ip, server_port)