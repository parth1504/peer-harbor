import os
import requests
from utils.torrentgeneration import create_torrent

def package_and_upload(file_path, announce_url, server_url):
    # Generate the torrent file using create_torrent function
    output_torrent_path = os.path.splitext(file_path)[0] + ".torrent"
    create_torrent(file_path, output_torrent_path, announce_url)

    # Upload the torrent file to the server
    upload_to_server(output_torrent_path, server_url)

def upload_to_server(torrent_file_path, server_url):
    # Read the torrent file as binary data
    with open(torrent_file_path, 'rb') as file:
        torrent_file_data = file.read()

    # Prepare the files to include the torrent file
    files = {'torrentFile': (os.path.basename(torrent_file_path), torrent_file_data)}

    # Make the HTTP POST request to the server
    response = requests.post(server_url, files=files)

    # Check the response status
    if response.status_code == 200:
        print(f"Torrent file {torrent_file_path} uploaded successfully to server: {server_url}")
    else:
        print(f"Error uploading torrent file {torrent_file_path} to server. Status Code: {response.status_code}")

if __name__ == "__main__":
    # Get file path input from the user
    file_path = input("Enter the file path: ").strip()

    # Set the announce URL for the tracker
    announce_url = "http://your.tracker/announce"

    # Set the server URL for uploading
    server_url = "http://your.upload.server/upload"

    # Call the utility function to package and upload the torrent file
    package_and_upload(file_path, announce_url, server_url)

