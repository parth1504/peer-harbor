import socket
import sys,os
import threading
import queue

from utils.Port import find_free_port

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from utils.Port import find_free_port

class PeerConnection:
    def __init__(self, peer_ip, peer_port):
        self.peer_ip = peer_ip
        self.peer_port = peer_port

    def seed_communication_connection(self):
        result_queue = queue.Queue()

        print("Waiting for leecher on communication ip and port ", self.peer_ip," ", self.peer_port )

        seeder_communication_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        seeder_communication_socket.bind((self.peer_ip, self.peer_port))
        seeder_communication_socket.listen(1)
        leecher_communication_socket, _ = seeder_communication_socket.accept()

        try:
            print("Connected to leecher_communication_socket")
            leecher_handler_thread = threading.Thread(
                target=handle_leecher,
                args=(self.peer_ip, result_queue, leecher_communication_socket)
            )
            leecher_handler_thread.start()

        except Exception as e:
            print(f"Error in seed_connection: {e}")

        finally:
            seeder_communication_socket.close()

<<<<<<< HEAD
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

=======
        self.seed_connection()

        return result_queue

    def seed_transfer_connection(self, seed_transfer_port):
>>>>>>> 8dfb5cd281e2c7e6af44aed4efc36627fe331bce
        seeder_transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        seeder_transfer_socket.bind((self.seeder_ip, seed_transfer_port))
        seeder_transfer_socket.listen(1)
        print("Waiting for leecher on trasfer port ", seed_transfer_port)

        leecher_transfer_socket, _ = seeder_transfer_socket.accept()

<<<<<<< HEAD
        result_queue.put(leecher_transfer_socket)

def close_connection(self, socket):
=======
        print("Accepted connection from leecher on transfer port ", seed_transfer_port)


def handle_leecher(seeder_ip, result_queue, leecher_communication_socket):
    print("Starting side thread operations")

    seed_transfer_port = find_free_port()

    print("Informing leecher of free port ", seed_transfer_port)

    print("Sending free port number ", seed_transfer_port, "to leecher")
    leecher_communication_socket.send(str(seed_transfer_port).encode())

    print("Closing communication socket")
    leecher_communication_socket.close()

    # result_queue.put(leecher_transfer_socket)

    # print("Result queue: ", result_queue.qsize())

class LeechConnection:
    def __init__(self, peer_ip, peer_port):
        self.peer_ip = peer_ip
        self.peer_port = peer_port

    def leecher_connection(self):
        print("Trying to connect to: ", self.peer_ip," ", self.peer_port )
        leecher_communication_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        leecher_communication_socket.connect((self.peer_ip, self.peer_port))

        # print("Connection to seeder_communication_socket made")

        seeder_transfer_port = int(leecher_communication_socket.recv(1024).decode())

        print("Received transfer port from Seeder: ", seeder_transfer_port)
        close_connection(leecher_communication_socket)

        print("Trying to connect to: ", self.peer_ip," ", seeder_transfer_port)
        leecher_transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        leecher_transfer_socket.connect((self.peer_ip, seeder_transfer_port))
        print(leecher_transfer_socket)
        return leecher_transfer_socket

def close_connection(socket):
>>>>>>> 8dfb5cd281e2c7e6af44aed4efc36627fe331bce
    socket.close()