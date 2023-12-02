import os
import sys


current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from connection.peer import SeedConnection
from Package import TorrentPackage
from utils.FileManipulation import Piecify, calculate_info_hash
from strategies.pieceSelectionAlgorithm import RarityTracker
import hashlib
import struct

'''
We need to send pieces with their respective indices to the leecher, so we will serialize the indices and data,
calculate the SHA1 hash of pieces and append it to the data and send this to the leecher.
'''
def send_pieces(socket, index, pieces):
    if not socket:
        raise ValueError("Socket not connected")

    for piece_index, piece_data in zip(index, pieces):
        # Serialize the piece data
        serialized_index = struct.pack('!Q', piece_index)
        serialized_piece = struct.pack(f'!{len(piece_data)}s', piece_data)

        # Calculate the hash of the serialized data
        hash_piece = hashlib.sha1(serialized_index + serialized_piece).digest()

        # Send the index, piece_data, and hash_piece
        serialized_data = serialized_index + serialized_piece + hash_piece
        socket.sendall(serialized_data)

    # Indicate the end of pieces transmission
    socket.sendall(b'')

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
        
    def package_and_publish (self):
        torrent_package = TorrentPackage(self.announce_url, self.server_url, self.file_path, self.output_torrent_path)
        torrent_package.upload_torrent_to_server(self.output_torrent_path, self.name, self.keywords, self.created_by)
        info_hash = calculate_info_hash(self.output_torrent_path)
        torrent_package.announce_to_tracker(info_hash)
    
    def setup_seeding (self):
        file = Piecify(self.file_path)
        self.piece_map = file.generate_piece_map()
        self.file_rarity = RarityTracker(len(self.piece_map))
        peerInstance = SeedConnection(self.seeder_ip, self.seeder_port)
        self.SeederSocketList = peerInstance.socket_dict
        
    # def start_seeding (self):
    
test = Seed("announce_url", "server_url", "file_path", "output_torrent_path", "name", "keywords", "created_by", "127.0.0.1", 7000)
test.setup_seeding()