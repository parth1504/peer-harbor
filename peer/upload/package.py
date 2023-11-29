import base64
import os
import requests
from utils.TorrentGenerator import TorrentGenerator

class TorrentPackage:
    def __init__(self, announce_url, server_url, file_path, output_torrent_path):
        self.announce_url = announce_url
        self.server_url = server_url
        self.file_path = file_path
        self.output_torrent_path = output_torrent_path
        # Create the torrent file
        torrent_file_path = TorrentGenerator(self.announce_url, file_path, output_torrent_path)

    def upload_torrent_to_server(self, torrent_file_path, name, keywords, created_by):
        print(torrent_file_path)
    # Read the torrent file as binary data
        with open(torrent_file_path, 'rb') as file:
            torrent_file_data = file.read()

        # Encode the torrent file data as base64
        torrent_file_base64 = base64.b64encode(torrent_file_data).decode('utf-8')

        # Prepare the files to include the torrent file
        files = {
            'name': (None, name),
            'keywords': (None, ','.join(keywords)),  # Assuming keywords should be joined with commas only
            'createdBy': (None, created_by),
            'torrentFile': ('torrentFile', torrent_file_base64)  # Specify the file name as 'torrentFile'
        }

        # Print the constructed files dictionary
        # print(files)

        # Make the HTTP POST request to the server
        response = requests.post(self.server_url, files=files)

        # Check the response status
        if response.status_code == 200 or response.status_code == 201 :
            print(f"Torrent file {torrent_file_path} uploaded successfully to server: {self.server_url}")
        else:
            print(f"Error uploading torrent file {torrent_file_path} to server. Status Code: {response.status_code}")
            print(f"Error details: {response.text}")

    def announce_to_tracker(self, info_hash):
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

        response = requests.get(self.announce_url, params=params)

        # Print the response
        print("peer list: ")
        print(response.text)

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
