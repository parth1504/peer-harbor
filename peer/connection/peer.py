import socket
import sys,os
import threading
import queue

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from utils.Port import find_free_port

class PeerConnection:
    def __init__(self, peer_ip, peer_port):
        self.peer_ip = peer_ip
        self.peer_port = peer_port

    def seed_connection(self):
        result_queue = queue.Queue()

        while True:
            seeder_communication_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            seeder_communication_socket.bind((self.peer_ip, self.peer_port))
            seeder_communication_socket.listen(1)

            try:
                leecher_communication_socket, _ = seeder_communication_socket.accept()

                seed_communication_port = find_free_port()
                leecher_handler_thread = threading.Thread(
                    target=self.handle_leecher,
                    args=(self.peer_ip, seed_communication_port, result_queue, leecher_communication_socket)
                )
                leecher_handler_thread.start()

            except Exception as e:
                print(f"Error in seed_connection: {e}")

            finally:
                seeder_communication_socket.close()

            return result_queue

    def leecher_connection(self):
        leecher_communication_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        leecher_communication_socket.connect((self.peer_ip, self.peer_port))
        seeder_transfer_port = int(leecher_communication_socket.recv(1024).decode())
        close_connection(leecher_communication_socket)

        leecher_transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        leecher_transfer_socket.connect((self.peer_ip, seeder_transfer_port))
        return leecher_transfer_socket

    def handle_leecher(seeder_ip, seed_communication_port, result_queue, leecher_communication_socket):
        leecher_communication_socket.send(str(seed_communication_port).encode())
        leecher_communication_socket.close()

        seeder_transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        seeder_transfer_socket.bind((seeder_ip, seed_communication_port))
        seeder_transfer_socket.listen(1)
        leecher_transfer_socket, _ = seeder_transfer_socket.accept()

        result_queue.put(leecher_transfer_socket)

def close_connection(self, socket):
    socket.close()