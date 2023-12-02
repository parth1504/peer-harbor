import socket
import sys,os
import threading
import queue

from utils.Port import find_free_port

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)


class SeedConnection:
    def __init__(self, peer_ip, peer_port):
        self.peer_ip = peer_ip 
        self.peer_port = peer_port 
        self.result_queue = queue.Queue()
        self.seeder_communication_socket = None
        self.startup_seed_connection()
        print("Waiting for leecher on communication ip and port ", self.peer_ip," ", self.peer_port )

        while self.seeder_communication_socket:
            leecher_communication_socket, leecher_communication_address = self.seeder_communication_socket.accept()
            print(f"Accepted connection from {leecher_communication_address}")

            print("Starting side thread operations")

            seed_transfer_port = find_free_port()

            print("Informing leecher of free port ", seed_transfer_port)
            print("Sending free port number ", seed_transfer_port, "to leecher")
            leecher_communication_socket.send(str(seed_transfer_port).encode())
            self.add_socket_to_queue(seed_transfer_port)
            print(self.result_queue.qsize())
            leecher_communication_socket.close()

    def seed_transfer_connection(self, seed_transfer_port):
        seeder_transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        seeder_transfer_socket.bind((self.peer_ip, seed_transfer_port))
        seeder_transfer_socket.listen(1)
        print("Waiting for leecher on trasfer port ", seed_transfer_port)

        leecher_transfer_socket, _ = seeder_transfer_socket.accept()

        print("Accepted connection from leecher on transfer port ", seed_transfer_port)
        
    def add_socket_to_queue(self, seed_transfer_port):
        seeder_transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        seeder_transfer_socket.bind((self.peer_ip, seed_transfer_port))
        seeder_transfer_socket.listen(1)
        print("Waiting for leecher on trasfer port ", seed_transfer_port)

        leecher_transfer_socket, _ = seeder_transfer_socket.accept()

        print("Accepted connection from leecher on transfer port ", seed_transfer_port)

        self.result_queue.put(leecher_transfer_socket)

    def startup_seed_connection(self):
        self.seeder_communication_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.seeder_communication_socket.bind((self.peer_ip, self.peer_port))
        self.seeder_communication_socket.listen(1)

    def close_seed_connection(self):
        self.seeder_communication_socket.close()
        self.result_queue.queue_clear()

class LeechConnection:
    def __init__(self, peer_ip, peer_port):
        self.peer_ip = peer_ip 
        self.peer_port = peer_port
        self.leecher_transfer_socket = None

    def leecher_connection(self):
        print("Trying to connect to: ", self.peer_ip," ", self.peer_port )
        leecher_communication_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        seeder_transfer_port = int(leecher_communication_socket.recv(1024).decode())

        print("Received transfer port from Seeder: ", seeder_transfer_port)
        leecher_communication_socket.close()

        print("Trying to connect to: ", self.peer_ip," ", seeder_transfer_port)
        leecher_transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        leecher_transfer_socket.connect((self.peer_ip, seeder_transfer_port))
        self.leecher_transfer_socket = leecher_transfer_socket
