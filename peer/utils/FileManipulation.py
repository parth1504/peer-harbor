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
    def __init__(self, file_path, piece_size=None):
        file_exists = os.path.exists(file_path)
        if not file_exists:
            with open(file_path, 'wb'):
                pass
        self.file_path = file_path
        self.piece_size = piece_size or calculate_piece_length(os.path.getsize(file_path))
        self.chunk_map = {}
        self.lock = threading.Lock()

    def generate_chunk_map(self):
        self.chunk_map = {}
        offset = 0
        index = 0

        with open(self.file_path, 'rb') as file:
            while True:
                data = file.read(self.piece_size)
                if not data:
                    break
                self.chunk_map[index] = offset
                offset += len(data)
                index += 1

        return self.chunk_map

    # def get_chunk_location(self, index):
    #     return self.chunk_map.get(index, None)

    def read_piece(self, index):
        with self.lock:
            offset = self.chunk_map.get(index)
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

            self.chunk_map[index] = offset



def calculate_piece_length(file_size):
    return max(16384, 1 << int(math.log2(1 if file_size < 1024 else file_size / 1024) + 0.5))


def calculate_info_hash(self,torrent_file_path):
        with open(torrent_file_path, 'rb') as file:
            torrent_data = bencodepy.decode(file.read())
            info_dict = torrent_data[b'info']
            info_bytes = bencodepy.encode(info_dict)
            info_hash = hashlib.sha1(info_bytes).digest()
            info_hash_hex = info_hash.hex()
            return info_hash_hex