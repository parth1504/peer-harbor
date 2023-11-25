import os
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from Package import TorrentPackage

class Publish:
    def __init__(self, announce_url, server_url, file_path, output_torrent_path, name, keywords, created_by):
        self.torrent_package = TorrentPackage(announce_url, server_url, file_path, output_torrent_path)
        self.torrent_package.upload_torrent_to_server(output_torrent_path, name, keywords, created_by)

if __name__ == "__main__":
    # Set the announce URL for the tracker
    announce_url = "http://your.tracker/announce"

    # Set the server URL for uploading
    server_url = "http://localhost:6969/torrent/upload"
    
    # Get file path input from the user
    file_path = "./invoice.pdf"
    output_torrent_path = "./output.torrent"

    # Get additional parameters for upload function
    name = "Invoice"
    keywords = "item1, item2"
    created_by = "Meow"

    # Create an instance of the Publish class
    publisher = Publish(announce_url, server_url, file_path, output_torrent_path, name, keywords, created_by)

