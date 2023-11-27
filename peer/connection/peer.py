import socket
import sys,os

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)
     
class PeerConnection:
    def __init__(self, peer_ip, peer_port):
        self.peer_ip = peer_ip 
        self.peer_port = peer_port 
 
    def seed_connection(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        server_socket.bind((self.peer_ip, self.peer_port)) 
        server_socket.listen(1) 
        client_socket, client_address = server_socket.accept()
        return client_socket, client_address, server_socket

    def leecher_connection(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.peer_ip, self.peer_port))
        return client_socket
    
def close_connection(self, socket):
    socket.close()