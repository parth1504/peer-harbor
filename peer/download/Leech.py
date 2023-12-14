import os
import sys
import concurrent.futures
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from strategies.chokingAlgorithm import LeecherHandler
from connection.peer import LeechConnection
from utils.FileManipulation import Piecify, TorrentReader, BitArray
from strategies.pieceSelectionAlgorithm import RarityTracker
from strategies.chokingAlgorithm import PeerSelection
from threading import Lock

'''
This function will be used by the leecher in order to receive pieces from the socket, It will keep on receiving data until it comes
across the 'TERMINATE' keyword. We use unpack to deserialize the data which was serialized at sender side. The minimum size of a piece
would be 28, index value will require 8 bytes and the SHA1 hash will require 20 bytes, based on this you allocate each piece it's index 
and hash values on the receiver side andcalculate and compare the SHA1 hash will the hash provided to check the integrity of the message.
'''

class Leech:
    def __init__ (self, piecify, bit_array, rarity_tracker, torrent_reader, announce_url):
        self.piecify = piecify
        self.rarity_tracker = rarity_tracker
        self.torrent = torrent_reader
        self.announce_url = announce_url
        self.info_hash = "random_info_hash" #torrent_reader.calculate_info_hash()
        self.is_running = True 
        self.bit_array=bit_array
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        self.threads = []

    def setup_leeching(self):
        self.selector = PeerSelection(self.announce_url, self.info_hash)
        while self.is_running:
            lock = Lock()
            peers = self.selector.get_info_from_tracker()
            # print("infohash: ", self.info_hash)
            # print("peerlist: ",peers)

            for peer in peers:
                self.executor.submit(self.start_leeching, peer['ip'], peer['port'], lock)

    def start_leeching(self, peer_ip, peer_port,lock):
        # print("leeching from: ", peer_ip, " ", peer_port)
        peer_instance = LeechConnection(peer_ip, peer_port)
        peer_instance.startup_leech_connection()
        LeecherHandler(peer_instance.leecher_transfer_socket, self.piecify, self.bit_array, self.rarity_tracker, lock)

    def stop_leeching(self):
        self.is_running = False
        self.executor.shutdown(wait=True)


download_file_path = "./upload/new.pdf"
saved_torrent_path = "./upload/new.torrent"

torrent = TorrentReader(saved_torrent_path)
piecify = Piecify(download_file_path, torrent.calculate_piece_length(), torrent.calculate_total_pieces())
bit_array = BitArray( piecify.generate_piece_map(), download_file_path, saved_torrent_path)

if not bit_array.is_bit_array_complete():
    file_rarity = RarityTracker(len(piecify.generate_piece_map()),torrent.info_hash) 
    test = Leech(piecify, bit_array, file_rarity, torrent, torrent.get_announce_url())
    test.setup_leeching()