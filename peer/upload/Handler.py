import hashlib
import struct
import threading

from  download.Handler import LeecherHandler

class SeederHandler:
    def __init__ (self, client_socket, server_socket, piecify, rarity_tracker):
        self.client_socket = client_socket
        self.piecify = piecify
        self.rarity_tracker = rarity_tracker
        self.server_socket = server_socket
        self.lock = threading.Lock()
        self.send_sorted_pieces()
    
    # def start_handler_threads(self):
    #     print("Meow")
    #     threads = []
    #     print(self.SeederInstance.socket_dict)
    #     for client_socket, _ in self.SeederInstance.socket_dict.items():
    #         print("Client socket: ", client_socket)
    #         thread = threading.Thread(target=self.send_sorted_pieces_wrapper, args=(client_socket,))
    #         threads.append(thread)
    #         thread.start()

    #     for thread in threads:
    #         thread.join()

    # def send_sorted_pieces_wrapper(self, client_socket):
    #     try:
    #         self.send_sorted_pieces(client_socket, self.sort_indices_by_rarity(self.rarity_tracker), self.rarity_tracker, self.piecify.generate_piece_map())
    #     except Exception as e:
    #         print(f"Error in send_sorted_pieces_wrapper: {e}")
    
    def sort_indices_by_rarity(self, rarity_tracker):
        with self.lock:
            indices_rarity = [(index, rarity_tracker.get_rarity(index)) for index in range(rarity_tracker.num_pieces)]
        sorted_indices = sorted(indices_rarity, key=lambda x: x[1])
        return [index for index, _ in sorted_indices]
    
    def receive_bit_array(self, client_socket):
        # print("in receive bit array")
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
        #print("In send_sorted_pieces")
        bit_array = self.receive_bit_array(self.client_socket)
        # print(" received bit array:  ", bit_array)
        for index in sorted_indices:
            if bit_array[index] == 1: 
                continue

            piece_data = self.piecify.read_piece(index)
            # print("Printing piece size: ", self.piecify.piece_size)
            #print("piece data: ", piece_data)
            self.send_piece(self.client_socket, index, piece_data)
            
            # LeecherHandler(client_socket, self.piecify, self.rarity_tracker)
            self.client_socket.close()
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
        
        # print("index: ", index)#
        
        serialized_index = struct.pack('!Q',index)
        serialized_piece = struct.pack(f'!{len(piece)}s', piece)
        index_value = struct.unpack('!Q', serialized_index)
        #hash_piece = hashlib.sha1(serialized_index + serialized_piece).digest()

        serialized_data = serialized_index + serialized_piece
        socket.sendall(serialized_data)
        print("sent index ", index)#
        # print("calculated index: ", index_value)

        socket.sendall(b'')