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
    def __init__ (self, announce_url, server_url, file_path, output_torrent_path, name, keywords, created_by, seeder_ip, seeder_port):
        self.announce_url = announce_url
        self.server_url = server_url
        self.file_path = file_path
        self.output_torrent_path = output_torrent_path
        self.name = name
        self.keywords = keywords
        self.created_by = created_by
        self.seeder_ip = seeder_ip
        self.seeder_port = seeder_port
        self.package_and_publish()
        
    def package_and_publish (self):
        # torrent_package = TorrentPackage(self.announce_url, self.server_url, self.file_path, self.output_torrent_path)
        # torrent_package.upload_torrent_to_server(self.output_torrent_path, self.name, self.keywords, self.created_by)
        # info_hash = self.torrentReader.calculate_info_hash(self.output_torrent_path)
        # torrent_package.announce_to_tracker(info_hash)
        self.torrentReader = TorrentReader(output_torrent_path)
        self.piecify = Piecify(self.file_path, self.torrentReader.calculate_piece_length(), self.torrentReader.calculate_total_pieces())
        self.bit_array= BitArray(self.piecify.piece_map, self.file_path, self.output_torrent_path)
        self.rarity_tracker = RarityTracker(self.piecify.total_pieces)
        self.peerInstance = SeedConnection(self.seeder_ip, self.seeder_port, self.piecify, self.bit_array, self.rarity_tracker)
    
    def start_seeding (self):
        self.peerInstance.startup_seed_connection()

    def stop_seeding (self):
        self.peerInstance.close_seed_connection()

file_path="./upload/SH.pdf"
output_torrent_path="./upload/Mahabharat.torrent"
saved_torrent_path="./upload/Mahabharat.torrent"     
torrent_reader = TorrentReader(saved_torrent_path)
test = Seed("announce_url", "server_url",file_path, output_torrent_path, "name", "keywords", "created_by", "127.0.0.1", 9000)
test.start_seeding()
# test.stop_seeding()