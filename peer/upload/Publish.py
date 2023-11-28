import os
import sys

import requests

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from package import TorrentPackage

class Publish:
    def __init__(self, announce_url, server_url, file_path, output_torrent_path, name, keywords, created_by):
        self.torrent_package = TorrentPackage(announce_url, server_url, file_path, output_torrent_path)
        self.torrent_package.upload_torrent_to_server(output_torrent_path, name, keywords, created_by)
        self.announce_to_tracker(announce_url)

    def announce_to_tracker(self, announce_url):
        # Get parameters for the announce request
        info_hash = "your_info_hash"  # Replace with the actual info_hash
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
    file_path = "./marksheets.pdf"
    output_torrent_path = "./output.torrent"

    # Get additional parameters for upload function
    name = "Invoice"
    keywords = "item1, item2"
    created_by = "Meow"

    # Create an instance of the Publish class
    publisher = Publish(announce_url, server_url, file_path, output_torrent_path, name, keywords, created_by)

