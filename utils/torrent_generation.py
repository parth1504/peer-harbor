import os
import torrentfile
import math
import hashlib
import subprocess

def read_in_chunks(file_object, chunk_size):
    """Generator to read a file in chunks."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def calculate_piece_length(file_size):
    return max(16384, 1 << int(math.log2(file_size / 1024) + 0.5))

def create_torrent(file_path, output_torrent_path, announce_url):
    # Ensure the file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    # Get file size
    file_size = os.path.getsize(file_path)

    # Calculate piece length using the provided formula
    piece_length = calculate_piece_length(file_size)

    # Generate piece hashes
    piece_hashes = [hashlib.sha1(chunk).digest() for chunk in read_in_chunks(open(file_path, 'rb'), piece_length)]

    # Run the 'torrentfile create' command
    command = [
        'torrentfile', 'create',
        '--announce', announce_url,
        '--source', os.path.basename(file_path),
        '--piece-length', str(piece_length),
        '--meta-version', '3',
        '--prog', '0',
        file_path
    ]
    subprocess.run(command, check=True)

if __name__ == "__main__":
    # Get file path input from the user
    file_path = input("Enter the file path: ").strip()

    # Set the announce URL for the tracker
    announce_url = "http://your.tracker/announce"

    # Generate the output torrent file path (same location as the input file with .torrent extension)
    output_torrent_path = os.path.splitext(file_path)[0] + ".torrent"

    # Call the function to create the torrent file
    create_torrent(file_path, output_torrent_path, announce_url)

