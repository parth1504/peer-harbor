import hashlib
import math
import bencodepy

def calculate_piece_length(file_size):
    return max(16384, 1 << int(math.log2(1 if file_size < 1024 else file_size / 1024) + 0.5))

class Piecify:
    def __init__(self, file_path, piece_size):
        self.file_path = file_path
        self.piece_size = piece_size
        self.pieces, self.piece_hashes, self.piece_indices = self._generate_piece_data()

    def read_in_chunks(self, file_object, chunk_size):
        """Generator to read a file in chunks."""
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    def _generate_piece_hashes(self, file_object):
        """Generate piece hashes for a file."""
        for chunk in self.read_in_chunks(file_object, self.piece_size):
            hash_value = hashlib.sha1(chunk).digest()
            yield chunk, hash_value

    def _generate_piece_data(self):
        """Generate piece hashes and indices for a file."""
        pieces=[]
        piece_hashes = []
        piece_indices = []
        index = 0

        with open(self.file_path, 'rb') as file:
            for chunk, hash_value in self._generate_piece_hashes(file):
                pieces.append(chunk)
                piece_hashes.append(hash_value)
                piece_indices.append(index)
                index += 1

        return pieces, piece_hashes, piece_indices

def write_file_from_pieces(pieces, output_file):
    with open(output_file, 'wb') as file:
        for piece in pieces:
            file.write(piece)



def calculate_info_hash(self,torrent_file_path):
        with open(torrent_file_path, 'rb') as file:
        # Load the .torrent file using bencode
            torrent_data = bencodepy.decode(file.read())

            # Extract the 'info' dictionary
            info_dict = torrent_data[b'info']

            # Encode the 'info' dictionary back to bytes
            info_bytes = bencodepy.encode(info_dict)

            # Calculate the SHA-1 hash of the 'info' bytes
            info_hash = hashlib.sha1(info_bytes).digest()

            # Convert the binary hash to a hexadecimal string
            info_hash_hex = info_hash.hex()
            print(info_hash_hex)
            return info_hash_hex
