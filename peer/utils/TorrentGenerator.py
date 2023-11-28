import os
import subprocess
import math

class TorrentGenerator:
    def __init__(self, announce_url, file_path, output_torrent_path):
        self.announce_url = announce_url
        self.output_torrent_path = output_torrent_path
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            return

        file_size = os.path.getsize(file_path)

        piece_length = self.calculate_piece_length(file_size)

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

    def calculate_piece_length(self, file_size):
        return max(16384, 1 << int(math.log2(file_size /2 ) + 0.5))

if __name__ == "__main__":
    announce_url = "http://your.tracker/announce"

    # Create an instance of TorrentGenerator
    torrent_generator = TorrentGenerator(announce_url)

    # Get file path input from the user
    file_path = input("Enter the file path: ").strip()

    # Call the method to generate and save the torrent file
    torrent_generator.generate_and_save_torrent(file_path)

