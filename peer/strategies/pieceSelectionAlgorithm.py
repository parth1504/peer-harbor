import json


class ClientInfo:
    def __init__(self):
        # Dictionary to store information for each file
        self.file_info = {}

    def create_file_info(self, file_id, total_pieces):
        # Create information for a new file
        if file_id not in self.file_info:
            self.file_info[file_id] = {
                'bitfield': [0] * total_pieces,
                'has_pieces': set(),
                'needed_pieces': set(range(total_pieces)),
            }

    def update_bitfield(self, file_id, piece_index):
        # Update the bitfield and sets for a specific file
        self.file_info[file_id]['bitfield'][piece_index] = 1
        self.file_info[file_id]['has_pieces'].add(piece_index)
        self.file_info[file_id]['needed_pieces'].discard(piece_index)

    def get_file_bitfield(self, file_id):
        # Return the current bitfield for a specific file
        return self.file_info[file_id]['bitfield']

    def get_file_has_pieces(self, file_id):
        # Return the set of pieces the client has for a specific file
        return self.file_info[file_id]['has_pieces']

    def get_file_needed_pieces(self, file_id):
        # Return the set of pieces the client still needs for a specific file
        return self.file_info[file_id]['needed_pieces']
    
def send_bitset(peer_socket, bitset):
    message = {'type': 'bitset', 'data': bitset}
    peer_socket.sendall(json.dumps(message).encode())

def receive_bitset(peer_socket):
    data = peer_socket.recv(1024)
    if data:
        message = json.loads(data.decode())
        if message['type'] == 'bitset':
            return message['data']
    return None