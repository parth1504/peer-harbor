import hashlib
import struct


def receive_pieces(socket):
    if not socket:
        raise ValueError("Socket not connected")

    received_data = b''

    # Adjust the buffer size as needed
    buffer_size = 4096

    while True:
        data = socket.recv(buffer_size)

        if not data:
            break  # Connection closed

        received_data += data

        # Check if the termination string is in the received data
        terminate_index = received_data.find(b'TERMINATE')
        if terminate_index != -1:
            break

    # Remove the termination string and unpack the received data
    received_data = received_data.replace(b'TERMINATE', b'')

    index = []
    pieces = []

    while len(received_data) >= 28:  # Minimum length for a valid message (8 + len(piece_data) + 20)
        # Unpack the header
        header_format = '!Q'
        header_size = struct.calcsize(header_format)
        index_value = struct.unpack(header_format, received_data[:header_size])[0]
        print(index_value)
        # Unpack the piece data
        remaining_data_size = len(received_data) - header_size
        if remaining_data_size < 40:
            # Last piece is smaller than 40 bytes
            piece_data_format = f'!{remaining_data_size-20}s20s'
            read_next=remaining_data_size
        else:
            piece_data_format = '20s20s'
            read_next=40
        piece_data = struct.unpack(piece_data_format, received_data[header_size:header_size + read_next])
        print(piece_data)

        hash_piece = hashlib.sha1(struct.pack( f'!Q{read_next-20}s', index_value, piece_data[0])).digest()
        if hash_piece != piece_data[1]:
            raise ValueError("Hash mismatch. Data may be corrupted.")
        else: print("matched")
        # Append the index and piece data to the lists
        index.append(index_value)
        pieces.append(piece_data[0])

        # Remove processed data from the received_data buffer
        received_data = received_data[header_size + 40:]

    return index, pieces