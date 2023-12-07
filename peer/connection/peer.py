import socket
import sys,os

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from utils.Port import find_free_port

class SeedConnection:
    def __init__(self, peer_ip, peer_port):
        self.peer_ip = peer_ip 
        self.peer_port = peer_port 
        self.socket_dict = {}
        self.seeder_communication_socket = None
        self.connection_close=False
        
    def startup_seed_connection(self):
        self.seeder_communication_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.seeder_communication_socket.bind((self.peer_ip, self.peer_port))
        self.seeder_communication_socket.listen(1)
        print("Waiting for leecher on communication ip and port ", self.peer_ip," ", self.peer_port)

        while self.seeder_communication_socket:
            leecher_communication_socket, leecher_communication_address = self.seeder_communication_socket.accept()
            print(f"Accepted connection from {leecher_communication_address}")

            print("Starting side thread operations")

            seed_transfer_port = find_free_port()

            print("Informing leecher of free port ", seed_transfer_port)
            print("Sending free port number ", seed_transfer_port, "to leecher")
            leecher_communication_socket.send(str(seed_transfer_port).encode())
            self.add_socket_to_queue(seed_transfer_port)
            print("socket dictionary: ", self.socket_dict)
            leecher_communication_socket.close()
            if self.connection_close:
                break
            print("in loop")
            

    def close_seed_connection(self):
        self.seeder_communication_socket.close()
        self.socket_dict.clear()
        
    def add_socket_to_queue(self, seed_transfer_port):
        seeder_transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        seeder_transfer_socket.bind((self.peer_ip, seed_transfer_port))
        seeder_transfer_socket.listen(1)
        print("Waiting for leecher on trasfer port ", seed_transfer_port)

        leecher_transfer_socket, _ = seeder_transfer_socket.accept()

        print("Accepted connection from leecher on transfer port ", seed_transfer_port)

        self.socket_dict[leecher_transfer_socket] = seeder_transfer_socket

class LeechConnection:
    def __init__(self, peer_ip, peer_port):
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.leecher_transfer_socket = None

    def startup_leech_connection(self):
        print("Trying to connect to: ", self.peer_ip," ", self.peer_port )
        leecher_communication_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        leecher_communication_socket.connect((self.peer_ip, self.peer_port))
        
        seeder_transfer_port = int(leecher_communication_socket.recv(1024).decode())

        print("Received transfer port from Seeder: ", seeder_transfer_port)
        leecher_communication_socket.close()

        print("Trying to connect to: ", self.peer_ip," ", seeder_transfer_port)
        leecher_transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        leecher_transfer_socket.connect((self.peer_ip, seeder_transfer_port))
        print("connected to port: ",seeder_transfer_port)
        self.leecher_transfer_socket = leecher_transfer_socket

        print(self.leecher_transfer_socket)#
        
    def close_leech_connection (self):
        self.leecher_transfer_socket.close()
