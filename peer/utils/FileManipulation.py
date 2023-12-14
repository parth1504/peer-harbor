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
    def __init__(self, file_path, piece_size = None, total_pieces = None):
        file_exists = os.path.exists(file_path)
        if not file_exists:
            with open(file_path, 'wb'):
                pass
        self.file_path = file_path
        self.piece_size = piece_size if piece_size is not None else calculate_piece_length(os.path.getsize(self.file_path))
        self.total_pieces = total_pieces if total_pieces is not None else self.calculate_total_pieces() 
        self.piece_map = {i: None for i in range(total_pieces)}
        self.lock = threading.Lock()
        self.generate_piece_map()

    def calculate_total_pieces(self):
        file_size = os.path.getsize(self.file_path)
        return file_size // self.piece_size + (file_size % self.piece_size != 0)

    def generate_piece_map(self):
        with open(self.file_path, 'rb') as file:
            for index in range(self.total_pieces):
                self.piece_map[index] = index * self.piece_size

        return self.piece_map

    def read_piece(self, index):
        with self.lock:
            if len(self.piece_map) == 0:
                self.generate_piece_map()
            offset = self.piece_map.get(index)
            
            if offset is not None:
                with open(self.file_path, 'rb') as file:
                    file.seek(offset)
                    data = file.read(self.piece_size)
                    return data
            else:
                return None

    def write_piece(self, index, piece):
        with self.lock:
            offset = index * self.piece_size
            with open(self.file_path, 'r+b') as file:
                file.seek(offset)
                file.write(piece)

            self.piece_map[index] = offset

class BitArray:
    def __init__(self, piece_map, file_path,torrent_file):
        self.torrent_file=torrent_file
        self.piece_map=piece_map
        self.have=0
        self.bit_array = [0] * (len(piece_map))
        self.generate_bit_array(piece_map, file_path)
        
    def is_bit_array_complete(self):
        return self.have == len(self.bit_array)

    def check_offset(self, file_path, offset):
        with open(file_path, 'rb') as file:
            file.seek(offset)
            byte = file.read(1)
            return byte != b''
    
    def generate_bit_array(self, piece_map, file_path):
        hash_list = []
        with open(self.torrent_file, 'rb') as file:
            torrent_data = bencodepy.decode(file.read())
            pieces = torrent_data[b'info'][b'pieces']
            total_pieces = len(pieces) // 20
            piece_length = torrent_data[b'info'][b'piece length']
            file_size = torrent_data[b'info'][b'length']

        with open(file_path, 'rb') as file:
            hash_list = []
            for piece_index, offset in piece_map.items():
                file.seek(offset)
                remaining_length = calculate_remaining_length(file_size, piece_length, offset)
                piece_data = file.read(remaining_length)
                hash_object = hashlib.sha1(piece_data)
                piece_hash = hash_object.hexdigest()
                hash_list.append(piece_hash)

        self.bit_array = [0] * (len(piece_map))
        for i, piece_hash in enumerate(hash_list):
            if piece_hash == pieces[i*20:(i+1)*20].hex(): 
                self.bit_array[i] = 1
                self.have += 1
                
            if i==total_pieces-1 and self.check_offset(file_path, piece_map[i]):
                self.bit_array[i] = 1
                self.have += 1
        
        print("number of pieces i have: ", self.have)

    def set_bit(self, index):
        self.bit_array[index] = 1
        self.have+=1

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
        
    def get_announce_url(self):
        return "http://127.0.0.1:6969/get_peers"
        # with open(self.torrent_file_path, 'rb') as torrent_file:
        #     torrent_data = bencodepy.decode(torrent_file.read())
        # announce_list = torrent_data.get('announce-list', [])
        # if not announce_list:
        #     announce_list = [torrent_data.get('announce')]

        # return announce_list
        
def calculate_piece_length(file_size):
    return max(16384, 1 << int(math.log2(1 if file_size < 1024 else file_size / 1024) + 0.5))

def calculate_remaining_length(file_size, piece_size, offset):
    remaining_length = file_size - offset
    return min(remaining_length, piece_size)
