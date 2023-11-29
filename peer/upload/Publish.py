import hashlib
import os
import sys
import requests

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from Package import TorrentPackage

class Publish:
    def __init__(self, announce_url, server_url, file_path, output_torrent_path, name, keywords, created_by):
        self.torrent_package = TorrentPackage(announce_url, server_url, file_path, output_torrent_path)
        self.torrent_package.upload_torrent_to_server(output_torrent_path, name, keywords, created_by)
        self.info_hash = self.calculate_info_hash(output_torrent_path)
        self.announce_to_tracker(announce_url, self.info_hash)

    

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

