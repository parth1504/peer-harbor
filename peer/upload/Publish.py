import hashlib
import os
import sys
import bencodepy
import requests

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from package import TorrentPackage

class Publish:
    def __init__(self, announce_url, server_url, file_path, output_torrent_path, name, keywords, created_by):
        self.torrent_package = TorrentPackage(announce_url, server_url, file_path, output_torrent_path)
        self.torrent_package.upload_torrent_to_server(output_torrent_path, name, keywords, created_by)
        self.info_hash = self.calculate_info_hash(output_torrent_path)
        self.announce_to_tracker(announce_url, self.info_hash)

    def calculate_info_hash(self,torrent_file_path):
        with open(torrent_file_path, 'rb') as file:
        # Load the .torrent file using bencode
            torrent_data = bencodepy.decode(file.read())

            # Extract the 'info' dictionary
            info_dict = torrent_data[b'info']

            # Encode the 'info' dictionary back to bytes
            info_bytes = bencodepy.encode(info_dict)

            # Calculate the SHA-1 hash of the 'info' bytes
            info_hash = hashlib.sha1(info_bytes).digest()

            # Convert the binary hash to a hexadecimal string
            info_hash_hex = info_hash.hex()
            print(info_hash_hex)
            return info_hash_hex
        
    def announce_to_tracker(self, announce_url, info_hash):
        # Get parameters for the announce request
        info_hash = info_hash  # Replace with the actual info_hash
        peer_id = "your_peer_id"  # Replace with the actual peer_id
        ip = "yourip2"  # Replace with the actual IP
        port = 123455  # Replace with the actual port
        uploaded = 0  # Replace with the actual uploaded amount
        downloaded = 0  # Replace with the actual downloaded amount
        left = 0  # Replace with the actual amount left

        # Make the announce request
        params = {
            'info_hash': info_hash,
            'peer_id': peer_id,
            'ip': ip,
            'port': port,
            'uploaded': uploaded,
            'downloaded': downloaded,
            'left': left,
        }

        response = requests.get(announce_url, params=params)

        # Print the response
        print("peer list: ")
        print(response.text)



if __name__ == "__main__":
    # Set the announce URL for the tracker
    announce_url = "http://127.0.0.1:6969/announce"

    # Set the server URL for uploading
    server_url = "http://localhost:6969/torrent/upload"

    # Get file path input from the user
    file_path = "D:/backend/p2p/peer-harbor/temp.md"
    output_torrent_path = "D:/backend/p2p/peer-harbor/peer/output.torrent"

    # Get additional parameters for upload function
    name = "sahil hijdi manjar"
    keywords = "sahil, hijda"
    created_by = "sahil hijda lavdya"

    # Create an instance of the Publish class
    publisher = Publish(announce_url, server_url, file_path, output_torrent_path, name, keywords, created_by)

