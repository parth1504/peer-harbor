import threading
import requests
import struct
from threading import Lock

class PeerSelection:
    def __init__(self, announce_url, info_hash):
        self.announce_url = announce_url
        self.info_hash = info_hash

    def get_info_from_tracker(self):
        params = {
            'info_hash': self.info_hash
        }

        response = requests.get(self.announce_url, params=params)

        if response.status_code == 200:
            tracker_response = response.json()
            peers_info = tracker_response.get('peers', [])
            peers_data = [{'ip': peer['ip'], 'port': peer['port']} for peer in peers_info]
            return peers_data
        else:
            print(f"Error getting info from tracker. Status Code: {response.status_code}")
            print(f"Error details: {response.text}")
            return None
        
class SeederHandler:
    def __init__ (self, client_socket , piecify, bit_array, rarity_tracker, server_socket=None, already_leeched = False):
        self.client_socket = client_socket
        self.piecify = piecify
        self.bit_array= bit_array
        self.rarity_tracker = rarity_tracker
        self.server_socket = server_socket
        self.already_leeched = already_leeched
        self.lock = threading.Lock()
        self.send_sorted_pieces()
    
    def sort_indices_by_rarity(self, rarity_tracker):
        with self.lock:
            indices_rarity = [(index, rarity_tracker.get_rarity(index)) for index in range(rarity_tracker.num_pieces)]
        sorted_indices = sorted(indices_rarity, key=lambda x: x[1])
        return [index for index, _ in sorted_indices]
    
    def receive_bit_array(self, client_socket):
        length_bytes = client_socket.recv(4)
        if not length_bytes:
            return None

        bit_array_length = struct.unpack('!I', length_bytes)[0]

        bit_array_bytes = client_socket.recv(bit_array_length)
        if not bit_array_bytes:
            return None

        bit_array = list(map(int, bit_array_bytes))
        return bit_array
    
    def send_sorted_pieces(self):
        sorted_indices = self.sort_indices_by_rarity(self.rarity_tracker)
        bit_array = self.receive_bit_array(self.client_socket)
        for index in sorted_indices:
            if bit_array[index] == 1: 
                continue

            piece_data = self.piecify.read_piece(index)

            self.send_piece(self.client_socket, index, piece_data)
            
            if not self.already_leeched and not self.bit_array.is_bit_array_complete():
                lock = Lock()
                LeecherHandler(self.client_socket, self.piecify, self.bit_array, self.rarity_tracker, lock, already_seeded=True)
            
            self.client_socket.close()
            if self.server_socket:
                self.server_socket.close()
            break

        for index, bit_value in enumerate(bit_array):
            with self.lock:
                if bit_value == 0:
                    self.rarity_tracker.update_rarity(index, accept=True)
                else:
                    self.rarity_tracker.update_rarity(index, accept=False)

    def send_piece(self, socket, index, piece):
        if not socket:
            raise ValueError("Socket not connected") 
        
        serialized_index = struct.pack('!Q',index)
        serialized_piece = struct.pack(f'!{len(piece)}s', piece)

        serialized_data = serialized_index + serialized_piece
        socket.sendall(serialized_data)
        # print("Sent Index: ", index)
        socket.sendall(b'TERMINATE')
        

class LeecherHandler:
    def __init__(self, leecher_socket, piecify, bit_array, rarity_tracker, lock, already_seeded = False ):
        self.leecher_socket = leecher_socket
        self.piecify = piecify
        self.rarity_tracker = rarity_tracker
        self.lock = lock  
        self.already_seeded = already_seeded  
        self.bit_array= bit_array   
        self.receive_rare_piece()

    def receive_rare_piece (self):
        self.lock.acquire()
        self.send_bit_array(self.leecher_socket, self.bit_array.bit_array)
        index, piece = self.receive_piece(self.leecher_socket)
        self.bit_array.set_bit(index)    
        self.piecify.write_piece(index, piece)
        self.rarity_tracker.add_piece(index)
        self.lock.release()

        if not self.already_seeded:
            SeederHandler(self.leecher_socket, self.piecify, self.bit_array, self.rarity_tracker, already_leeched=True)
    
    def send_bit_array(self, socket, bit_array):
        bit_bytes = bytes(bit_array)
        bit_array_length = len(bit_array)
        message = struct.pack('!I', bit_array_length) + bit_bytes
        socket.sendall(message)
    
    def receive_piece(self, socket):
        piece_size= self.piecify.piece_size
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

        while len(received_data) >= 8:
            header_format = '!Q'
            header_size = struct.calcsize(header_format)
            index_value = struct.unpack(header_format, received_data[:header_size])[0]
            remaining_data_size = len(received_data) - header_size
            if remaining_data_size < piece_size:
                piece_data_format = f'!{remaining_data_size}s'
                read_next=remaining_data_size
            else:
                piece_data_format = f'!{piece_size}s'
                read_next=piece_size
            piece_data = struct.unpack(piece_data_format, received_data[header_size:header_size + read_next])

            received_data = received_data[header_size + piece_size:]

        print("Received index: ", index_value)
        return index_value, piece_data[0]