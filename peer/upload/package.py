import base64
import os
import requests
from utils.TorrentGenerator import TorrentGenerator
from utils.FileManipulation import TorrentReader

class TorrentPackage:
    def __init__(self, file_path, output_torrent_path, name, keywords, created_by, announce_url, server_url, peer_ip, peer_port):
        self.file_path = file_path
        self.output_torrent_path = output_torrent_path
        
        self.name = name
        self.keywords = keywords
        self.created_by = created_by
        
        self.announce_url = announce_url
        self.server_url = server_url
        self.peer_ip = peer_ip  
        self.peer_port = peer_port
        
        torrent_file = TorrentGenerator(self.announce_url, file_path, output_torrent_path)
        torrentReader = TorrentReader(output_torrent_path)
        self.info_hash = torrentReader.calculate_info_hash() 
        self.upload_torrent_to_server()
        self.announce_to_tracker()

    def upload_torrent_to_server(self):
        with open(self.output_torrent_path, 'rb') as file:
            torrent_file_data = file.read()

        torrent_file_base64 = base64.b64encode(torrent_file_data).decode('utf-8')

        files = {
            'name': (None, self.name),
            'keywords': (None, ','.join(self.keywords)),  
            'createdBy': (None, self.created_by),
            'torrentFile': ('torrentFile', torrent_file_base64)  
        }

        response = requests.post(self.server_url, files=files)

        if response.status_code == 200 or response.status_code == 201 :
            print(f"Torrent file {self.output_torrent_path} uploaded successfully to server: {self.server_url}")
        else:
            print(f"Error uploading torrent file {self.output_torrent_path} to server. Status Code: {response.status_code}")
            print(f"Error details: {response.text}")

    def announce_to_tracker(self):
        print("in announce")
        params = {
            'info_hash': self.info_hash,
            'ip': self.peer_ip,
            'port': self.peer_port
        }

        response = requests.get(self.announce_url, params=params)

if __name__ == "__main__":
    # Set the announce URL for the tracker
    announce_url = "http://your.tracker/announce"

    # Set the server URL for uploading
    server_url = "http://localhost:3000/upload"

    # Create an instance of the TorrentPackage class
    torrent_package = TorrentPackage(announce_url, server_url)

    # Get file path input from the user
    file_path = input("Enter the file path: ").strip()

    # Get additional parameters for upload function
    name = input("Enter the name: ").strip()
    keywords = input("Enter the keywords (comma-separated): ").strip().split(',')
    created_by = input("Enter the creator's name: ").strip()

    # Call the package_and_upload method to create the torrent file and upload
    torrent_package.package_and_upload(file_path, name, keywords, created_by)
