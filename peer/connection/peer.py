import socket
import sys,os
import threading
import time

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from utils.Port import find_free_port
from strategies.chokingAlgorithm import SeederHandler
from connection.tracker import TrackerThread

class SeedConnection:
    def __init__(self, peer_ip, peer_port, piecify, bit_array, rarity_tracker):
        self.peer_ip = peer_ip 
        self.peer_port = peer_port 
        self.piecify = piecify
        self.bit_array= bit_array
        self.rarity_tracker = rarity_tracker
        self.connection_close = False
        self.thread = threading.Thread(target=self.startup_seed_connection_thread)
        self.Tracker_thread= TrackerThread(rarity_tracker)
        
    def add_socket_to_queue(self, seed_transfer_port):
        seeder_transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        seeder_transfer_socket.bind((self.peer_ip, seed_transfer_port))
        seeder_transfer_socket.listen(1)
        leecher_transfer_socket, _ = seeder_transfer_socket.accept()
        SeederHandler(leecher_transfer_socket, self.piecify, self.bit_array, self.rarity_tracker , server_socket=seeder_transfer_socket)
        
    def startup_seed_connection_thread(self):
        interval_duration = 300  # 5 minutes in seconds
        last_call_time = time.time()

        while not self.connection_close:
            leecher_communication_socket, _ = self.seeder_communication_socket.accept()
            seed_transfer_port = find_free_port()
            leecher_communication_socket.send(str(seed_transfer_port).encode())
            self.Tracker_thread.send_rarity_array_periodically()    #make it so that it is called after 5 minutes
            self.add_socket_to_queue(seed_transfer_port)
            leecher_communication_socket.close()
            current_time = time.time()

            # Check if 5 minutes have passed since the last call
            if current_time - last_call_time >= interval_duration:
                self.Tracker_thread.send_rarity_array_periodically()
                last_call_time = current_time

    def startup_seed_connection(self):
        self.seeder_communication_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.seeder_communication_socket.bind((self.peer_ip, self.peer_port))
        self.seeder_communication_socket.listen(1)
        print("Waiting for leecher on communication ip and port ", self.peer_ip, " ", self.peer_port)
        self.thread.start()

    def close_seed_connection(self):
        self.connection_close = True
        self.seeder_communication_socket.close()
        self.thread.join()
        self.socket_dict.clear()
        
        
class LeechConnection:
    def __init__(self, peer_ip, peer_port):
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.leecher_transfer_socket = None

    def startup_leech_connection(self):
        leecher_communication_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        leecher_communication_socket.connect((self.peer_ip, self.peer_port))
        seeder_transfer_port = int(leecher_communication_socket.recv(1024).decode())
        leecher_communication_socket.close()
        leecher_transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        leecher_transfer_socket.connect((self.peer_ip, seeder_transfer_port))
        self.leecher_transfer_socket = leecher_transfer_socket
        
    def close_leech_connection (self):
        self.leecher_transfer_socket.close()
