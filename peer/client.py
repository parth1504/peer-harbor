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

class ClientInfo:
    def __init__(self):
        # Dictionary to store information for each file
        self.file_info = {}

    def create_file_info(self, file_id, total_pieces):
        # Create information for a new file
        if file_id not in self.file_info:
            self.file_info[file_id] = {
                'bitfield': [0] * total_pieces,
                'has_pieces': set(),
                'needed_pieces': set(range(total_pieces)),
            }

    def update_bitfield(self, file_id, piece_index):
        # Update the bitfield and sets for a specific file
        self.file_info[file_id]['bitfield'][piece_index] = 1
        self.file_info[file_id]['has_pieces'].add(piece_index)
        self.file_info[file_id]['needed_pieces'].discard(piece_index)

    def get_file_bitfield(self, file_id):
        # Return the current bitfield for a specific file
        return self.file_info[file_id]['bitfield']

    def get_file_has_pieces(self, file_id):
        # Return the set of pieces the client has for a specific file
        return self.file_info[file_id]['has_pieces']

    def get_file_needed_pieces(self, file_id):
        # Return the set of pieces the client still needs for a specific file
        return self.file_info[file_id]['needed_pieces']


hasher= Piecify("D:/backend/p2p/peer-harbor/README.md",10)
piece_hashes, piece_indices=hasher._generate_piece_data()
print(piece_hashes,piece_indices)

# Example usage:
client_info = ClientInfo()

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

def connect_to_peer(peer_ip, peer_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    message="bitch ass nigga"

    try:
        client_socket.connect((peer_ip, peer_port))
        print(f"Connected to {peer_ip}:{peer_port}")
        send_file(client_socket,"D:/backend/p2p/peer-harbor/README.md")
        #client_socket.sendall(message.encode())

        # You can send/receive data here

    except Exception as e:
        print(f"Error: Unable to connect to {peer_ip}:{peer_port}. {e}")

    finally:
        client_socket.close()

def simulate_peer(peer_ip, peer_port):
    # Simulate peer behavior
    print(f"Simulating peer at {peer_ip}:{peer_port}")
    
    # Simulate some activity or data exchange
    time.sleep(2)

    # Connect to the other peer
    connect_to_peer("127.0.0.1", 6881)  # Replace with the actual IP and port of the other peer


def get_peer_list(tracker_url, info_hash, peer_id, ip, port, uploaded, downloaded, left, compact=0):
    # Build the request URL with all parameters
    request_url = (
        f"{tracker_url}?info_hash={info_hash}&peer_id={peer_id}&ip={ip}&port={port}"
        f"&uploaded={uploaded}&downloaded={downloaded}&left={left}&compact={compact}"
    )

    # Make the HTTP GET request to the tracker
    response = requests.get(request_url)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Parse the response content to get the peer list
        peer_list = response.content
        return peer_list
    else:
        print(f"Error: Unable to get peer list. Status Code: {response.status_code}")
        return None



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




