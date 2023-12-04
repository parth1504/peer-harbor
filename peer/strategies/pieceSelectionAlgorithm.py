import json

class RarityTracker:
    def __init__(self, num_pieces, base_smoothing_factor=0.2):
        self.num_pieces = num_pieces
        self.base_smoothing_factor = base_smoothing_factor
        self.piece_metrics = {index: {'rarity': 5, 'base_smoothing_factor': base_smoothing_factor} for index in range(num_pieces)}

    def add_piece(self, piece_index):
        if piece_index not in self.piece_metrics:
            self.piece_metrics[piece_index] = {'rarity': 5, 'base_smoothing_factor': self.base_smoothing_factor}
    
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

    def refresh(self, global_rarity_values):
        for index in range(self.num_pieces):
            if index < len(global_rarity_values):
                self.piece_metrics[index]['rarity'] = global_rarity_values[index]
            else:
                self.piece_metrics[index]['rarity'] = 5