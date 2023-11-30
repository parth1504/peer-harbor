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

from connection.peer import PeerConnection


def receive_pieces(socket):
    if not socket:
        raise ValueError("Socket not connected")

    received_data = b''

    # Adjust the buffer size as needed
    buffer_size = 4096

    while True:
        data = socket.recv(buffer_size)

        if not data:
            break  # Connection closed

        received_data += data

        # Check if the termination string is in the received data
        terminate_index = received_data.find(b'TERMINATE')
        if terminate_index != -1:
            break

    # Remove the termination string and unpack the received data
    received_data = received_data.replace(b'TERMINATE', b'')

    index = []
    pieces = []

    while len(received_data) >= 28:  # Minimum length for a valid message (8 + len(piece_data) + 20)
        # Unpack the header
        header_format = '!Q'
        header_size = struct.calcsize(header_format)
        index_value = struct.unpack(header_format, received_data[:header_size])[0]
        print(index_value)
        # Unpack the piece data
        remaining_data_size = len(received_data) - header_size
        if remaining_data_size < 40:
            # Last piece is smaller than 40 bytes
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
        # Append the index and piece data to the lists
        index.append(index_value)
        pieces.append(piece_data[0])

        # Remove processed data from the received_data buffer
        received_data = received_data[header_size + 40:]

    return index, pieces

class Leech:
    def __init__ (self, announce_url, download_file_path, saved_torrent_path, seeder_ip, seeder_port):
        self.announce_url = announce_url
        self.download_file_path = download_file_path
        self.saved_torrent_path = saved_torrent_path
        self.seeder_ip = seeder_ip
        self.seeder_port = seeder_port
        self.is_running = True  # Flag to control the thread

    def setup_leeching (self):
        peerInstance = PeerConnection(self.seeder_ip, self.seeder_port)
        self.LeecherSocket = peerInstance.leecher_connection()

    def start_leeching(self, info_hash, peer_id, ip, port, uploaded, downloaded, left):
        # Start the background task to refresh info every 30 seconds
        refresh_thread = threading.Thread(target=self.refresh_info_periodically, args=(info_hash, peer_id, ip, port, uploaded, downloaded, left),daemon=True)
        refresh_thread.start()
        # Your code for starting leeching (button click, etc.)

    def refresh_info_periodically(self, info_hash, peer_id, ip, port, uploaded, downloaded, left):
        while self.is_running:
            # Call the method to get info from the tracker
            self.get_info_from_tracker(self.announce_url, info_hash, peer_id, ip, port, uploaded, downloaded, left, compact=0)

            # Sleep for 30 seconds before the next refresh
            time.sleep(30)

    def stop_refreshing(self):
        # Call this method to stop the background refresh thread
        self.is_running = False

    def get_info_from_tracker (self, tracker_url, info_hash, peer_id, ip, port, uploaded, downloaded, left, compact=0):
        # Prepare the query parameters
        params = {
            'info_hash': info_hash
        }

        # Make the HTTP GET request to the tracker
        response = requests.get(tracker_url, params=params)

        if response.status_code == 200:
            # Parse the response content (tracker's response)
            tracker_response = response.json()

            # Extract the list of peers from the tracker response
            peers_info = tracker_response.get('peers', [])

            # Extract and store IP and port for each peer
            peers_data = [{'ip': peer['ip'], 'port': peer['port']} for peer in peers_info]

            # Return the list of dictionaries representing each peer
            return peers_data
        else:
            print(f"Error getting info from tracker. Status Code: {response.status_code}")
            print(f"Error details: {response.text}")
            return None


test = Leech("announce_url", "download_file_path", "saved_torrent_path", "127.0.0.1", 6969)
result = test.get_info_from_tracker("http://127.0.0.1:6969/get_peers", "random_info_hash", "peer_id", "ip", "port", "uploaded", "downloaded", "left", compact=0)
print(result)
