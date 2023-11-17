import hashlib
import os
import bencodepy
import os


import os

def get_size(path):
    """
    Get the size of a file or folder.

    Parameters:
    - path (str): The path to a file or folder.

    Returns:
    - int: The size in bytes.
    """
    if os.path.isfile(path):
        # If it's a file, return the file size
        return os.path.getsize(path)
    elif os.path.isdir(path):
        # If it's a folder, calculate the total size of all files in the folder and subfolders
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        return total_size
    else:
        # If the path doesn't exist or is neither a file nor a folder
        raise FileNotFoundError(f"Path '{path}' not found.")


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

    info_dict_bencoded = bencodepy.encode(info_dict)

    info_hash= hashlib.sha1(info_dict_bencoded).digest()

    files_info = [
        {'length':447,'path': 'D:\\backend\p2p\peer-harbor\\utils\\temp.txt'}
    ]

    torrent_data = {
        
        'created by': 'Your Torrent Creator',
        'creation date': int(os.path.getmtime(path)),
        'info':{
            'files':[{'length':447,'path': 'D:\\backend\p2p\peer-harbor\\utils\\temp.txt'}],
            'name':'sahil whore',
            'piece length':piece_size,
            'pieces':pieces,
            
        }
        
    }

    with open(output_torrent_path, 'wb') as torrent_file:
        torrent_file.write(bencodepy.encode(torrent_data))



if __name__ == "__main__":
    folder_path = "D:\\backend\p2p\peer-harbor\\utils\\temp.txt"
    output_torrent_path = "books.torrent"
    announce_url = "http://your.tracker/announce"


    create_torrent(folder_path, output_torrent_path, announce_url)

