import json
import time

class ClientInfo:
    def __init__(self):
        self.file_info = {}

    def create_file_info(self, file_id, total_pieces):
        if file_id not in self.file_info:
            self.file_info[file_id] = {
                'bitfield': [0] * total_pieces,
                'has_pieces': set(),
                'needed_pieces': set(range(total_pieces)),
            }

    def update_bitfield(self, file_id, piece_index):
        self.file_info[file_id]['bitfield'][piece_index] = 1
        self.file_info[file_id]['has_pieces'].add(piece_index)
        self.file_info[file_id]['needed_pieces'].discard(piece_index)

    def get_file_bitfield(self, file_id):
        return self.file_info[file_id]['bitfield']

    def get_file_has_pieces(self, file_id):
        return self.file_info[file_id]['has_pieces']

    def get_file_needed_pieces(self, file_id):
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


class RarityTracker:
    def init(self, num_pieces, base_smoothing_factor=0.2):
        self.num_pieces = num_pieces
        self.base_smoothing_factor = base_smoothing_factor
        self.piece_metrics = {index: {'rarity': 5, 'base_smoothing_factor': base_smoothing_factor} for index in range(num_pieces)}

    def update_rarity(self, piece_index, accept=True, network_size=1):
        if piece_index in self.piece_metrics:
            metric = self.piece_metrics[piece_index]
            target_value = 1 if accept else 10
            smoothing_factor = metric['base_smoothing_factor'] / network_size
            metric['rarity'] = (1 - smoothing_factor) * metric['rarity'] + smoothing_factor * target_value

    def get_rarity(self, piece_index):
        if piece_index in self.piece_metrics:
            metric = self.piece_metrics[piece_index]
            return min(10, max(1, metric['rarity']))
        else:
            return None

    def refresh(self, initial_rarity_values):
        for index in range(self.num_pieces):
            if index < len(initial_rarity_values):
                self.piece_metrics[index]['rarity'] = initial_rarity_values[index]
            else:
                self.piece_metrics[index]['rarity'] = 5