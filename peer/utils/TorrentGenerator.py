import os
import sys
import subprocess

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from utils.FileManipulation import calculate_piece_length

'''
This class is used in order to generate a .torrent file which will be stored on a web server from where leechers can download it,
this file will give information regarding which tracker to contact, info hash of file, piece length, etc.
'''
class TorrentGenerator:
    def __init__(self, announce_url, file_path, output_torrent_path):
        self.announce_url = announce_url
        self.output_torrent_path = output_torrent_path
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            return

        file_size = os.path.getsize(file_path)

        piece_length = calculate_piece_length(file_size)

        command = [
            'torrentfile', 'create',
            '--announce', self.announce_url,
            '--source', os.path.basename(file_path),
            '--out', self.output_torrent_path,
            '--piece-length', str(piece_length),
            '--meta-version', '3',
            '--prog', '0',
            file_path
        ]
        subprocess.run(command, check=True)

if __name__ == "__main__":
    announce_url = "http://your.tracker/announce"
    torrent_generator = TorrentGenerator(announce_url)
    file_path = input("Enter the file path: ").strip()
    torrent_generator.generate_and_save_torrent(file_path)

