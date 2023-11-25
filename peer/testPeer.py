import hashlib
import json,os,socket,sys,time
import struct

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from connection.peer import connect_to_peer
from utils.manipulation import Piecify


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
        print(serialized_data)
        socket.sendall(serialized_data)

    # Indicate the end of pieces transmission
    socket.sendall(b'TERMINATE')


def receive_pieces(socket):
    if not socket:
        raise ValueError("Socket not connected")

    received_data = b''
    while True:
        data = socket.recv(4096)  # Adjust the buffer size as needed

        if not data:
            break  # Connection closed

        received_data += data

        # Check if the end of pieces transmission is reached
        if received_data.endswith(b''):
            break

    # Unpack the received data
    index = []
    pieces = []

    while len(received_data) > 28:  # Minimum length for a valid message (8 + len(piece_data) + 20)
        # Unpack the header
        header_format = '!Q'
        header_size = struct.calcsize(header_format)
        index_value = struct.unpack(header_format, received_data[:header_size])[0]

        # Unpack the piece data
        piece_size = len(received_data) - 28
        piece_data_format = f'!{piece_size}s20s'
        piece_data = struct.unpack(piece_data_format, received_data[header_size:])
        
        # Validate the received data by checking the hash
        hash_piece = hashlib.sha1(struct.pack(f'!Q{piece_size}s', index_value, piece_data[0])).digest()
        if hash_piece != piece_data[1]:
            raise ValueError("Hash mismatch. Data may be corrupted.")

        # Append the index and piece data to the lists
        index.append(index_value)
        pieces.append(piece_data[0])

        # Remove processed data from the received_data buffer
        received_data = received_data[header_size + piece_size + 20:]

    return index, pieces

def simulate_peer(peer_ip, peer_port):
    # Simulate peer behavior
    print(f"Simulating peer at {peer_ip}:{peer_port}")
    
    # Simulate some activity or data exchange
    time.sleep(2)

    # Connect to the other peer
    connect_to_peer("127.0.0.1", 6881)  # Replace with the actual IP and port of the other peer


def receive_file(conn, file_path):
    with open(file_path, 'wb') as file:
        chunk_size = 10
        data = conn.recv(chunk_size)
        while data:
            file.write(data)
            data = conn.recv(chunk_size)

def send_bitset(peer_socket, bitset):
    message = {'type': 'bitset', 'data': bitset}
    peer_socket.sendall(json.dumps(message).encode())


def receive_bitset(peer_socket):
    data = peer_socket.recv(1024)
    if data:
        message = json.loads(data.decode())
        if message['type'] == 'bitset':
            return message['data']
    return None

def start_server(ip, port):
    hasher= Piecify("D:/backend/p2p/peer-harbor/README.md",10)
    pieces,piece_hashes, piece_indices=hasher._generate_piece_data()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)  # Listen for one incoming connection

    print(f"Waiting for incoming connection on {ip}:{port}")
    client_socket, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")
    # Receive and print messages
    #receive_file(client_socket,"D:/backend/p2p/peer-harbor/temp.md")
   
    send_pieces(client_socket, piece_indices,pieces)
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    # Adjust the IP and port to match the server's configuration
    server_ip = "127.0.0.1"
    server_port = 6881
    start_server(server_ip, server_port)
