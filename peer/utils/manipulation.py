import hashlib

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

        return pieces,piece_hashes, piece_indices

