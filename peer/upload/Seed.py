import os
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from connection.peer import SeedConnection
from Package import TorrentPackage
from utils.FileManipulation import Piecify, TorrentReader, BitArray
from strategies.pieceSelectionAlgorithm import RarityTracker

'''
We need to send pieces with their respective indices to the leecher, so we will serialize the indices and data,
calculate the SHA1 hash of pieces and append it to the data and send this to the leecher.
'''

class Seed:
    def __init__ (self, seeder_ip, seeder_port, piecify, bit_array, rarity_tracker, output_torrent_path):
        self.seeder_ip = seeder_ip
        self.seeder_port = seeder_port
        self.piecify = piecify
        self.bit_array = bit_array
        self.rarity_tracker = rarity_tracker
        self.output_torrent_path = output_torrent_path
        self.package_and_publish()
        
    def package_and_publish (self):
        self.peerInstance = SeedConnection(self.seeder_ip, self.seeder_port, self.piecify, self.bit_array, self.rarity_tracker)
    
    def start_seeding (self):
        self.peerInstance.startup_seed_connection()

    def stop_seeding (self):
        self.peerInstance.close_seed_connection()

if __name__ == "__main__":
    seeder_ip = input("Enter seeder IP: ")
    seeder_port = int(input("Enter seeder port: "))    
    output_torrent_path = input("Enter output torrent path: ")
    file_path = input("Enter file path: ")
    
    if os.path.exists(output_torrent_path):
        torrentReader = TorrentReader(output_torrent_path)
        piecify = Piecify(file_path, torrentReader.calculate_piece_length(), torrentReader.calculate_total_pieces())
    else:
        name = input("Enter name: ")
        keywords = input("Enter keywords: ")
        created_by = input("Enter created by: ")
        announce_url = input("Enter announce URL: ")
        server_url = input("Enter server URL: ")
        torrent_package = TorrentPackage(file_path, output_torrent_path, name, keywords, created_by, announce_url, server_url, seeder_ip, seeder_port)
        piecify = Piecify(file_path)
        
    bit_array = BitArray(piecify.piece_map, file_path, output_torrent_path)
    rarity_tracker = RarityTracker(piecify.total_pieces)
    seed_instance = Seed(seeder_ip, seeder_port, piecify, bit_array, rarity_tracker, output_torrent_path)
    

    while True:
        action = input("Enter 'start' to start seeding, 'pause' to stop seeding, or 'exit' to exit: ")
        
        if action == "start":
            seed_instance.start_seeding()
        elif action == "pause":
            seed_instance.stop_seeding()
        elif action == "exit":
            break
        else:
            print("Invalid command. Try again.")