import struct
import hashlib
from utils.FileManipulation import BitArray
import threading

class LeecherHandler:
    def __init__(self, leecher_socket, piecify, rarity_tracker):
        print("In handler")
        self.leecher_socket = leecher_socket
        self.piecify = piecify
        self.rarity_tracker = rarity_tracker
        self.receive_rare_piece()
        # self.lock= threading.Lock()

    def receive_rare_piece (self):
        print("in receive rare piece")#
        print(self.piecify.file_path)#
        piece_map=self.piecify.generate_piece_map()
        print(piece_map)
        array_calculator = BitArray(piece_map, self.piecify.file_path) 
        self.send_bit_array(self.leecher_socket, array_calculator.bit_array)
        index, piece = self.receive_piece(self.leecher_socket)
        print("received piece: ", index)
        # with self.lock:
        self.piecify.write_piece(index, piece)
        #self.array_calculator.set_bit(index)
        self.rarity_tracker.add_piece(index)
    
    def send_bit_array(self, socket, bit_array):
        print("In send bit_array")#
        bit_bytes = bytes(bit_array)
        bit_array_length = len(bit_array)
        message = struct.pack('!I', bit_array_length) + bit_bytes
        socket.sendall(message)
        print("sent")
    
    def receive_piece(self, socket):
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

        while len(received_data) >= 28:
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
            else:
                print("matched")
                index = index_value
                piece = piece_data[0]

                received_data = received_data[header_size + 40:]

        return index, piece