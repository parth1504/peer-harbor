import hashlib
import struct


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