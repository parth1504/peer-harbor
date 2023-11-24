import os
import torrentfile
import math
import subprocess

def calculate_piece_length(file_size):
    return max(16384, 1 << int(math.log2(file_size / 1024) + 0.5))

def create_torrent(file_path, output_torrent_path, announce_url):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    file_size = os.path.getsize(file_path)

    piece_length = calculate_piece_length(file_size)

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
    file_path = input("Enter the file path: ").strip()

    announce_url = "http://your.tracker/announce"

    output_torrent_path = os.path.splitext(file_path)[0] + ".torrent"

    create_torrent(file_path, output_torrent_path, announce_url)