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
        #send_file(client_socket,"D:/backend/p2p/peer-harbor/README.md")
        #client_socket.sendall(message.encode())
        bitset= [0]*6
        send_bitset(client_socket,bitset)
        peerBitset=receive_bitset(client_socket)
        print("Peer bitset: ",peerBitset)
        # You can send/receive data here

    except Exception as e:
        print(f"Error: Unable to connect to {peer_ip}:{peer_port}. {e}")

    finally:
        client_socket.close()