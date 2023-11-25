import hashlib
import json
import struct
import sys,os
from os.path import abspath, dirname

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from utils.manipulation import Piecify
from strategies.pieceSelectionAlgorithm import ClientInfo
from connection.peer import connect_to_peer

def send_pieces(socket, index, pieces):
    if not socket:
        raise ValueError("Socket not connected")

    for piece_index, piece_data in zip(index, pieces):
        # Serialize the piece data
        serialized_index = struct.pack('!Q', piece_index)
        serialized_piece = struct.pack(f'!{len(piece_data)}s', piece_data)

        # Calculate the hash of the serialized data
        hash_piece = hashlib.sha1(serialized_index + serialized_piece).digest()

        # Send the index, piece_data, and hash_piece
        serialized_data = serialized_index + serialized_piece + hash_piece
        socket.sendall(serialized_data)

    # Indicate the end of pieces transmission
    socket.sendall(b'')


def receive_pieces(socket):
    if not socket:
        raise ValueError("Socket not connected")

    received_data = b''
    termination_signal = b'TERMINATE'
      
    while True:
        data = socket.recv(4096)  # Adjust the buffer size as needed

        received_data += data

        # Check if the end of pieces transmission is reached
        if termination_signal in received_data:
            break

    # Unpack the received data
    index = []
    pieces = []
    #print(received_data)
    while len(received_data) > 28:  # Minimum length for a valid message (8 + len(piece_data) + 20)
        # Unpack the header
        header_format = '!Q'
        header_size = struct.calcsize(header_format)
        index_value = struct.unpack(header_format, received_data[:header_size])[0]

        # Unpack the piece data
        piece_size = len(received_data) - 28
        piece_data_format = f'!{piece_size}s20s'
        piece_data = struct.unpack(piece_data_format, received_data[header_size:])
        piece_data = piece_data[0] 
        print(piece_data)

        # Validate the received data by checking the hash
        # hash_piece = hashlib.sha1(struct.pack(f'!Q{piece_size}s', index_value, piece_data)).digest()

        # if hash_piece != piece_data[1]:
        #     raise ValueError("Hash mismatch. Data may be corrupted.")

        # Append the index and piece data to the lists
        index.append(index_value)
        pieces.append(piece_data[0])

        # Remove processed data from the received_data buffer
        received_data = received_data[header_size + piece_size + 20:]

    return index, pieces


def receive_file(conn, file_path):
    with open(file_path, 'wb') as file:
        chunk_size = 10
        data = conn.recv(chunk_size)

        while data:
            file.write(data)
            data = conn.recv(chunk_size)

def send_file(conn, file_path):
    with open(file_path, 'rb') as file:
        chunk_size = 10
        data = file.read(chunk_size)

        while data:
            conn.send(data)
            data = file.read(chunk_size)
            print("sahil gay")


# Example usage
tracker_url = "http://127.0.0.1:6969/announce"
info_hash = "another_random_hash"  # Replace with the actual info hash
peer_id = "abcdefghij0123456789"  # Replace with the actual peer ID
ip = "127.0.0.1"  # Replace with the actual IP address of your client
port = 6881  # Replace with the actual port number
uploaded = 0  # Replace with the actual amount uploaded by your client
downloaded = 0  # Replace with the actual amount downloaded by your client
left = 1024  # Replace with the actual amount left to download by your client

# peer_list = get_peer_list(tracker_url, info_hash, peer_id, ip, port, uploaded, downloaded, left)
# if peer_list:
#     print(f"Peer list from tracker: {peer_list.decode('utf-8')}")

client_socket=connect_to_peer("127.0.0.1",6881)
print(client_socket.type)
data= receive_pieces(client_socket)
print(data)
client_socket.close()




