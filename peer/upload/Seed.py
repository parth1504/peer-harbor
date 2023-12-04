import os
import sys


current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from connection.peer import SeedConnection
from Package import TorrentPackage
from utils.FileManipulation import Piecify, calculate_info_hash
from strategies.pieceSelectionAlgorithm import RarityTracker
from Handler import Handler

'''
We need to send pieces with their respective indices to the leecher, so we will serialize the indices and data,
calculate the SHA1 hash of pieces and append it to the data and send this to the leecher.
'''

class Seed:
    def __init__ (self, piecify, rarity_tracker, announce_url, server_url, file_path, output_torrent_path, name, keywords, created_by, seeder_ip, seeder_port):
        self.piecify = piecify
        self.rarity_tracker = rarity_tracker
        self.announce_url = announce_url
        self.server_url = server_url
        self.file_path = file_path
        self.output_torrent_path = output_torrent_path 
        self.name = name
        self.keywords = keywords
        self.created_by = created_by
        self.seeder_ip = seeder_ip
        self.seeder_port = seeder_port
        self.peerInstance = SeedConnection(self.seeder_ip, self.seeder_port)
        
    def package_and_publish (self):
        torrent_package = TorrentPackage(self.announce_url, self.server_url, self.file_path, self.output_torrent_path)
        torrent_package.upload_torrent_to_server(self.output_torrent_path, self.name, self.keywords, self.created_by)
        info_hash = calculate_info_hash(self.output_torrent_path)
        torrent_package.announce_to_tracker(info_hash)
    
    def setup_seeding (self):
        self.peerInstance.startup_seed_connection()
        self.SeederSocketList = self.peerInstance.socket_dict
        seeder = Handler(self.file_path, self.SeederSocketList, self.piecify, self.rarity_tracker)

    def stop_seeding (self):
        self.peerInstance.close_seed_connection()
        

file = Piecify(file_path)
file_rarity = RarityTracker(len(piece_map))
test = Seed("announce_url", "server_url", "file_path", "output_torrent_path", "name", "keywords", "created_by", "127.0.0.1", 7000)
test.setup_seeding()