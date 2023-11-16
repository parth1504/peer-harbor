import hashlib

class Piecify:
    def __init__(self, file_path, piece_size):
        self.file_path = file_path
        self.piece_size = piece_size
        self.piece_hashes, self.piece_indices = self._generate_piece_data()

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
            yield hash_value

    def _generate_piece_data(self):
        """Generate piece hashes and indices for a file."""
        piece_hashes = []
        piece_indices = []
        index = 0

        with open(self.file_path, 'rb') as file:
            for hash_value in self._generate_piece_hashes(file):
                piece_hashes.append(hash_value)
                piece_indices.append(index)
                index += len(hash_value)

        return piece_hashes, piece_indices

if __name__ == "__main__":
    file_path = "./algorithmic-puzzles.pdf"
    piece_size = 1024 * 512

    piecify_instance = Piecify(file_path, piece_size)

    print("Piece Hashes and Indices:")
    for i, (hash_value, index) in enumerate(zip(piecify_instance.piece_hashes, piecify_instance.piece_indices)):
        print(f"Piece {i + 1}: Hash={hash_value.hex()}, Index={index}")
