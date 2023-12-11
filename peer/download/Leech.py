import os
import sys
import requests
import threading
import time
import concurrent.futures

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from strategies.chokingAlgorithm import LeecherHandler
from connection.peer import LeechConnection
from utils.FileManipulation import Piecify, TorrentReader, BitArray
from strategies.pieceSelectionAlgorithm import RarityTracker
from strategies.chokingAlgorithm import PeerSelection
from threading import Thread, Lock


'''
This function will be used by the leecher in order to receive pieces from the socket, It will keep on receiving data until it comes
across the 'TERMINATE' keyword. We use unpack to deserialize the data which was serialized at sender side. The minimum size of a piece
would be 28, index value will require 8 bytes and the SHA1 hash will require 20 bytes, based on this you allocate each piece it's index 
and hash values on the receiver side andcalculate and compare the SHA1 hash will the hash provided to check the integrity of the message.
'''

class Leech:
    def __init__ (self, piecify, bit_array, rarity_tracker, announce_url, info_hash, download_file_path):
        self.piecify = piecify
        self.rarity_tracker = rarity_tracker
        self.announce_url = announce_url
        self.info_hash = info_hash
        self.is_running = True 
        self.bit_array=bit_array
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        self.threads = []

    def setup_leeching(self):
        self.selector = PeerSelection(self.announce_url, self.info_hash)
        while self.is_running:
            lock = Lock()
            peers = self.selector.get_info_from_tracker()

            for peer in peers:
                self.executor.submit(self.start_leeching, peer['ip'], peer['port'], lock)
                # thread = threading.Thread(target=self.start_leeching, args=(peer['ip'], peer['port']))
                # thread.start()
                # self.threads.append(thread)
                #time.sleep(0.1)

    def start_leeching(self, peer_ip, peer_port,lock):
        peer_instance = LeechConnection(peer_ip, peer_port)
        peer_instance.startup_leech_connection()
        # print(peer_instance.leecher_transfer_socket)
        LeecherHandler(peer_instance.leecher_transfer_socket, self.piecify, self.bit_array, self.rarity_tracker, lock)

    def stop_leeching(self):
        self.is_running = False
        self.executor.shutdown(wait=True)


    # def stop_leeching(self):
    #     self.is_running = False

    #     for thread in self.threads:
    #         thread.join()


announce_url = "http://127.0.0.1:6969/get_peers"
info_hash = "random_info_hash"
saved_torrent_path = "D:/backend/p2p/peer-harbor/peer/upload/Mahabharat.torrent"
download_file_path = "./temp.pdf"
torrent = TorrentReader(saved_torrent_path)
file = Piecify(download_file_path, torrent.calculate_piece_length(), torrent.calculate_total_pieces())
bit_array= BitArray(Piecify.generate_piece_map(),download_file_path)
file_rarity = RarityTracker(len(file.generate_piece_map()))  
test = Leech(file, bit_array, file_rarity, announce_url, info_hash,"temp")
test.setup_leeching()
# print(test.LeecherSocket)