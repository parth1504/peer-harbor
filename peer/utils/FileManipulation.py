import hashlib
import math
import bencodepy
import threading
import os

'''
Piecify class is responsible for making a map where we will assign each piece an offset which will be the starting location of that 
piece in the file. We also have read and write functions in this class where we can read or write a specific piece based on it's index
'''
class Piecify:
    def __init__(self, file_path,total_pieces, piece_size):
        file_exists = os.path.exists(file_path)
        if not file_exists:
            with open(file_path, 'wb'):
                pass
        self.file_path = file_path
        self.piece_size = piece_size 
        self.piece_map = {}
        self.total_pieces= total_pieces
        self.lock = threading.Lock()

    def generate_piece_map(self):
        self.piece_map = {}
        piece_length = self.piece_size
        total_pieces = self.total_pieces

        with open(self.file_path, 'rb') as file:
            for index in range(total_pieces):
                self.piece_map[index] = index * piece_length

        return self.piece_map

    def read_piece(self, index):
        with self.lock:
            offset = self.piece_map.get(index)
            if offset is not None:
                with open(self.file_path, 'rb') as file:
                    file.seek(offset)
                    return file.read(self.piece_size)
            else:
                return None

    def write_piece(self, index, piece):
        with self.lock:
            offset = index * self.piece_size
            with open(self.file_path, 'r+b') as file:
                print("writing in file: ", index )
                file.seek(offset)
                file.write(piece)

            self.piece_map[index] = offset

class BitArray:
    def __init__(self, piece_map, file_path):
        print("initiated bitarray")
        self.bit_array = self.generate_bit_array(piece_map, file_path)
        print("bitarray: ", self.bit_array)
        self.piece_map=piece_map

    def check_offset(self,file_path, offset):
        with open(file_path, 'rb') as file:
            file.seek(offset)
            byte = file.read(1)
            return byte != b''

    def generate_bit_array(self,piece_map, file_path):
        max_index = max(piece_map.keys(), default=-1)
        bit_array = [0] * (max_index + 1)
        for piece_index, offset in piece_map.items():
            if self.check_offset(file_path, offset):
                bit_array[piece_index] = 1
        return bit_array


    def set_bit(self, index):
        if 0 <= index < len(self.bit_array):
            self.bit_array[index] = 1
        else:
            raise ValueError("Index out of range.")
    
    def get_bit(self, index):
        if 0 <= index < len(self.bit_array):
            return self.bit_array[index]
        else:
            raise ValueError("Index out of range.")

    def __str__(self):
        return ''.join(map(str, self.bit_array))


class TorrentReader:
    def __init__ (self, torrent_file_path):
        self.torrent_file_path = torrent_file_path
        self.info_hash = self.calculate_info_hash()
        self.piece_length = self.calculate_piece_length()
        self.total_pieces = self.calculate_total_pieces()

    def calculate_total_pieces(self):
        with open(self.torrent_file_path, 'rb') as file:
            torrent_data = bencodepy.decode(file.read())
            pieces = torrent_data[b'info'][b'pieces']
            total_pieces = len(pieces) // 20
            return total_pieces
        
    def calculate_info_hash(self):
        with open(self.torrent_file_path, 'rb') as file:
            torrent_data = bencodepy.decode(file.read())
            pieces = torrent_data[b'info'][b'pieces']
            total_pieces = len(pieces) // 20
            print(total_pieces)
            info_dict = torrent_data[b'info']
            info_bytes = bencodepy.encode(info_dict)
            info_hash = hashlib.sha1(info_bytes).digest()
            info_hash_hex = info_hash.hex()
            return info_hash_hex
        
    def calculate_piece_length(self):
        with open(self.torrent_file_path, 'rb') as file:
            torrent_data = bencodepy.decode(file.read())
            piece_length = torrent_data[b'info'][b'piece length']
            return piece_length
        
def calculate_piece_length(file_size):
    return max(16384, 1 << int(math.log2(1 if file_size < 1024 else file_size / 1024) + 0.5))

temp= TorrentReader("D:/backend/p2p/peer-harbor/peer/Mahabharat.torrent")