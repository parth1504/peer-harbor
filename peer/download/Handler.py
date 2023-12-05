import struct
import hashlib

class Receive:
    def __init__ (self, socket):
        self.socket = socket
    
    def get_piece(self, index):
        if not self.socket:
            raise ValueError("Socket not connected")

        header = struct.pack('!Q', index)
        self.socket.send(header)

        index_received, piece_received = self.receive_piece()

        if index_received != index:
            raise ValueError("Received piece index does not match the requested index")

        return piece_received
        
    def transfer_handler(socket):
        if not socket:
            raise ValueError("Socket not connected")

        received_data = b''
        buffer_size = 4096

        while True:
            data = socket.recv(buffer_size)

            if not data:
                break

            received_data += data
            terminate_index = received_data.find(b'TERMINATE')
            if terminate_index != -1:
                break

        received_data = received_data.replace(b'TERMINATE', b'')

        index = None
        piece = None

        while len(received_data) >= 28:     #The index will be 8B and hash will be 20B
            header_format = '!Q'
            header_size = struct.calcsize(header_format)
            index_value = struct.unpack(header_format, received_data[:header_size])[0]
            print(index_value)
            remaining_data_size = len(received_data) - header_size
            if remaining_data_size < 40:
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
            index = index_value
            piece = piece_data[0]

            received_data = received_data[header_size + 40:]

        return index, piece