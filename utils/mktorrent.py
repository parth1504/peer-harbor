import hashlib
import os
import bencodepy

def generate_info_dict(path, piece_size):
    if os.path.isfile(path):
        return generate_file_info_dict(path, piece_size)
    elif os.path.isdir(path):
        return generate_folder_info_dict(path, piece_size)
    else:
        raise ValueError(f"Invalid path: {path}")

def generate_file_info_dict(file_path, piece_size):
    file_size = os.path.getsize(file_path)
    pieces = []

    with open(file_path, 'rb') as file:
        while True:
            data = file.read(piece_size)
            if not data:
                break
            pieces.append(hashlib.sha1(data).digest())

    return {
        'length': file_size,
        'path': [os.path.basename(file_path)],
    }

def generate_folder_info_dict(folder_path, piece_size):
    folder_info = {'name': os.path.basename(folder_path), 'files': []}

    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            file_info = generate_file_info_dict(file_path, piece_size)
            folder_info['files'].append(file_info)

    return folder_info

def create_torrent(path, output_torrent_path, announce_url, piece_size=262144):
    info_dict = generate_info_dict(path, piece_size)
    info_dict['piece length'] = piece_size  # Set piece length in the root dictionary

    pieces = b''
    if 'files' in info_dict:
        for file_info in info_dict['files']:
            pieces += file_info['pieces']

    info_dict['pieces'] = pieces

    torrent_data = {
        'info': info_dict,
        'announce': announce_url,
        'creation date': int(os.path.getmtime(path)),
        'created by': 'Your Torrent Creator',
    }

    with open(output_torrent_path, 'wb') as torrent_file:
        torrent_file.write(bencodepy.encode(torrent_data))

if __name__ == "__main__":
    folder_path = "./algorithmic-puzzles.pdf"
    output_torrent_path = "books.torrent"
    announce_url = "http://your.tracker/announce"

    create_torrent(folder_path, output_torrent_path, announce_url)

