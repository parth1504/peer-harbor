import hashlib
from bencoding import bencode

# Example details, replace with your actual information
torrent_data = {
    'announce': 'udp://tracker.example.com:6969/announce',
    'info': {
        'name': 'gta5_folder',
        'piece length': 8,  # 8-byte piece length
        'pieces': b'',  # Placeholder for piece hashes, will be populated later
        # Other info about files, etc.
    }
}

# Convert dictionary to Bencoded data
bencoded_data = bencode(torrent_data)

# Calculate and add piece hashes
with open('D:/Deep learning/ANN/Churn_Modelling.csv', 'rb') as file:
    piece_hashes = []
    while True:
        piece = file.read(8)  # Read 8 bytes at a time
        if not piece:
            break
        piece_hashes.append(hashlib.sha1(piece).digest())
        file.seek(8, 1)  # Move the file pointer 8 bytes forward

# Concatenate the piece hashes and add to the torrent_data
torrent_data['info']['pieces'] = b''.join(piece_hashes)

# Save Bencoded data to a .torrent file
with open('D:/backend/p2p/peer-harbor/utils/gta5.torrent', 'wb') as torrent_file:
    torrent_file.write(bencoded_data)
