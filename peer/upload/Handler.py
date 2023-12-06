import hashlib
import struct
import threading

class SeederHandler:
    def __init__ (self, SeederSocketList, piecify, rarity_tracker):
        self.SeederSocketList = SeederSocketList
        self.piecify = piecify
        self.rarity_tracker = rarity_tracker
        self.start_handler_threads()
        self.lock = threading.Lock()
    
    def start_handler_threads(self):
        threads = []
        for client_socket, _ in self.SeederSocketList.items():
            thread = threading.Thread(target=self.send_sorted_pieces_wrapper, args=(client_socket,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def send_sorted_pieces_wrapper(self, client_socket):
        try:
            self.send_sorted_pieces(client_socket, self.sort_indices_by_rarity(self.rarity_tracker), self.rarity_tracker, self.piecify.generate_piece_map())
        except Exception as e:
            print(f"Error in send_sorted_pieces_wrapper: {e}")
    
    def sort_indices_by_rarity(self, rarity_tracker):
        with self.lock:
            indices_rarity = [(index, rarity_tracker.get_rarity(index)) for index in range(rarity_tracker.num_pieces)]
        sorted_indices = sorted(indices_rarity, key=lambda x: x[1])
        return [index for index, _ in sorted_indices]
    
    def receive_bit_array(self, socket):
        length_bytes = socket.recv(4)
        if not length_bytes:
            return None

        bit_array_length = struct.unpack('!I', length_bytes)[0]

        bit_array_bytes = socket.recv(bit_array_length)
        if not bit_array_bytes:
            return None

        bit_array = list(map(int, bit_array_bytes))

        return bit_array
    
    def send_sorted_pieces(self, socket, sorted_indices, rarity_tracker, piece_map):
        bit_array = self.receive_bit_array(socket)

        for index in sorted_indices:
            if bit_array[index] == 1: 
                continue

            offset = piece_map[index]
            piece_data = self.piecify.read_piece(index)
            self.send_piece(socket, [index], [piece_data])
            
            client_socket = socket
            server_socket = self.SeederSocketList[client_socket]
            LeecherHandler(client_socket, self.piecify, self.rarity_tracker)
            client_socket.close()
            server_socket.close()

            del self.SeederSocketList[client_socket]
            break

        for index, bit_value in enumerate(bit_array):
            with self.lock:
                if bit_value == 0:
                    rarity_tracker.update_rarity(index, accept=True)
                else:
                    rarity_tracker.update_rarity(index, accept=False)

    def send_piece(socket, index, piece):
        if not socket:
            raise ValueError("Socket not connected")

        for piece_index, piece_data in zip(index, piece):
            serialized_index = struct.pack('!Q', piece_index)
            serialized_piece = struct.pack(f'!{len(piece_data)}s', piece_data)

            hash_piece = hashlib.sha1(serialized_index + serialized_piece).digest()

            serialized_data = serialized_index + serialized_piece + hash_piece
            socket.sendall(serialized_data)

        socket.sendall(b'')
        

class SeederHandler:
    def __init__ (self, socket, piecify, rarity_tracker):
        self.socket = socket
        self.piecify = piecify
        self.rarity_tracker = rarity_tracker
        self.send_sorted_pieces(self.socket, self.sort_indices_by_rarity, self.rarity_tracker, self.piecify.piece_map)
    
    def sort_indices_by_rarity(self, rarity_tracker):
        indices_rarity = [(index, rarity_tracker.get_rarity(index)) for index in range(rarity_tracker.num_pieces)]
        sorted_indices = sorted(indices_rarity, key=lambda x: x[1])
        return [index for index, _ in sorted_indices]
    
    def receive_bit_array(self, socket):
        length_bytes = socket.recv(4)
        if not length_bytes:
            return None

        bit_array_length = struct.unpack('!I', length_bytes)[0]

        bit_array_bytes = socket.recv(bit_array_length)
        if not bit_array_bytes:
            return None

        bit_array = list(map(int, bit_array_bytes))

        return bit_array
    
    def send_sorted_pieces(self, socket, sorted_indices, rarity_tracker, piece_map):
        bit_array = self.receive_bit_array(socket)

        for index in sorted_indices:
            if bit_array[index] == 1: 
                continue

            offset = piece_map[index]
            piece_data = self.piecify.read_piece(offset, index, piece_map)
            self.send_piece(socket, [index], [piece_data])
            socket.close()
            break

        for index, bit_value in enumerate(bit_array):
            if bit_value == 0:
                rarity_tracker.update_rarity(index, accept=True)
            else:
                rarity_tracker.update_rarity(index, accept=False)

    def send_piece(socket, index, piece):
        if not socket:
            raise ValueError("Socket not connected")

        for piece_index, piece_data in zip(index, piece):
            serialized_index = struct.pack('!Q', piece_index)
            serialized_piece = struct.pack(f'!{len(piece_data)}s', piece_data)

            hash_piece = hashlib.sha1(serialized_index + serialized_piece).digest()

            serialized_data = serialized_index + serialized_piece + hash_piece
            socket.sendall(serialized_data)

        socket.sendall(b'')