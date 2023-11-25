import socket
import sys,os

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)
sys.path.append("D:/backend/p2p/peer-harbor")

from  strategies.pieceSelectionAlgorithm import receive_bitset
from  strategies.pieceSelectionAlgorithm import send_bitset


def connect_to_peer(peer_ip, peer_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    message="bitch ass nigga"

    try:
        client_socket.connect((peer_ip, peer_port))
        print(f"Connected to {peer_ip}:{peer_port}")
        return client_socket

    except Exception as e:
        print(f"Error: Unable to connect to {peer_ip}:{peer_port}. {e}")

    #finally:
       # client_socket.close()