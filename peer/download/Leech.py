import os
import sys
import requests
import threading
import time

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from Handler import Handler
from connection.peer import LeechConnection
from utils.FileManipulation import Piecify, TorrentReader
from strategies.pieceSelectionAlgorithm import RarityTracker
from strategies.chokingAlgorithm import PeerSelection

'''
This function will be used by the leecher in order to receive pieces from the socket, It will keep on receiving data until it comes
across the 'TERMINATE' keyword. We use unpack to deserialize the data which was serialized at sender side. The minimum size of a piece
would be 28, index value will require 8 bytes and the SHA1 hash will require 20 bytes, based on this you allocate each piece it's index 
and hash values on the receiver side andcalculate and compare the SHA1 hash will the hash provided to check the integrity of the message.
'''

class Leech:
    def __init__ (self, piecify, rarity_tracker, announce_url, info_hash, download_file_path):
        self.piecify = piecify
        self.rarity_tracker = rarity_tracker
        self.announce_url = announce_url
        self.info_hash = info_hash
        self.is_running = True 
        self.threads = []

    def setup_leeching(self):
        self.selector = PeerSelection(self.announce_url, self.info_hash)
        while self.is_running:
            peers = self.selector.get_info_from_tracker()

            for peer in peers:
                thread = threading.Thread(target=self.setup_connection, args=(peer['ip'], peer['port']))
                thread.start()
                self.threads.append(thread)

            time.sleep(1)

    def setup_connection(self, peer_ip, peer_port):
        peer_instance = LeechConnection(peer_ip, peer_port)
        peer_instance.startup_leech_connection()
        Handler(peer_instance.leecher_transfer_socket, self.piecify, self.rarity_tracker)

    def stop_leeching(self):
        self.is_running = False

        for thread in self.threads:
            thread.join()


   
torrent = TorrentReader(saved_torrent_path)
file = Piecify(download_file_path, torrent.piece_length)
file_rarity = RarityTracker(len(file.generate_piece_map()))  
test = Leech("download_file_path", "saved_torrent_path", "127.0.0.1", 7000)
test.setup_leeching()
print(test.LeecherSocket)