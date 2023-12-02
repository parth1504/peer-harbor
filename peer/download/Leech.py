import os
import sys
import requests
import threading
import time
import struct
import hashlib

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from connection.peer import LeechConnection
from utils.FileManipulation import Piecify, TorrentReader
from strategies.pieceSelectionAlgorithm import RarityTracker

'''
This function will be used by the leecher in order to receive pieces from the socket, It will keep on receiving data until it comes
across the 'TERMINATE' keyword. We use unpack to deserialize the data which was serialized at sender side. The minimum size of a piece
would be 28, index value will require 8 bytes and the SHA1 hash will require 20 bytes, based on this you allocate each piece it's index 
and hash values on the receiver side andcalculate and compare the SHA1 hash will the hash provided to check the integrity of the message.
'''
def receive_pieces(socket):
    if not socket:
        raise ValueError("Socket not connected")

    received_data = b''
    buffer_size = 4096

    while True:
        data = socket.recv(buffer_size)

        if not data:
            break

        received_data += data
        terminate_index = received_data.find(b'TERMINATE')
        if terminate_index != -1:
            break

    received_data = received_data.replace(b'TERMINATE', b'')

    index = []
    pieces = []

    while len(received_data) >= 28:
        header_format = '!Q'
        header_size = struct.calcsize(header_format)
        index_value = struct.unpack(header_format, received_data[:header_size])[0]
        print(index_value)
        remaining_data_size = len(received_data) - header_size
        if remaining_data_size < 40:
            piece_data_format = f'!{remaining_data_size-20}s20s'
            read_next=remaining_data_size
        else:
            piece_data_format = '20s20s'
            read_next=40
        piece_data = struct.unpack(piece_data_format, received_data[header_size:header_size + read_next])
        print(piece_data)

        hash_piece = hashlib.sha1(struct.pack( f'!Q{read_next-20}s', index_value, piece_data[0])).digest()
        if hash_piece != piece_data[1]:
            raise ValueError("Hash mismatch. Data may be corrupted.")
        else: print("matched")
        index.append(index_value)
        pieces.append(piece_data[0])

        received_data = received_data[header_size + 40:]

    return index, pieces

class Leech:
    def __init__ (self, announce_url, download_file_path, saved_torrent_path, seeder_ip, seeder_port):
        self.announce_url = announce_url
        self.download_file_path = download_file_path
        self.saved_torrent_path = saved_torrent_path
        self.seeder_ip = seeder_ip
        self.seeder_port = seeder_port
        self.is_running = True 

    def setup_leeching (self):
        torrent = TorrentReader(self.saved_torrent_path)
        self.file = Piecify(self.download_file_path, torrent.piece_length)
        self.file_rarity = RarityTracker(len(self.file.generate_piece_map()))
        peerInstance = LeechConnection(self.seeder_ip, self.seeder_port)
        peerInstance.leecher_connection()
        self.LeecherSocket = peerInstance.leecher_transfer_socket

    def start_leeching(self, info_hash, peer_id, ip, port, uploaded, downloaded, left):
        refresh_thread = threading.Thread(target=self.refresh_info_periodically, args=(info_hash, peer_id, ip, port, uploaded, downloaded, left),daemon=True)
        refresh_thread.start()

    def refresh_info_periodically(self, info_hash, peer_id, ip, port, uploaded, downloaded, left):
        while self.is_running:
            self.get_info_from_tracker(self.announce_url, info_hash, peer_id, ip, port, uploaded, downloaded, left, compact=0)
            time.sleep(30)

    def stop_refreshing(self):
        self.is_running = False

    def get_info_from_tracker (self, tracker_url, info_hash, peer_id, ip, port, uploaded, downloaded, left, compact=0):
        params = {
            'info_hash': info_hash
        }

        response = requests.get(tracker_url, params=params)

        if response.status_code == 200:
            tracker_response = response.json()
            peers_info = tracker_response.get('peers', [])
            peers_data = [{'ip': peer['ip'], 'port': peer['port']} for peer in peers_info]
            return peers_data
        else:
            print(f"Error getting info from tracker. Status Code: {response.status_code}")
            print(f"Error details: {response.text}")
            return None
        
test = Leech("announce_url", "download_file_path", "saved_torrent_path", "127.0.0.1", 7000)
test.setup_leeching()
print(test.LeecherSocket)