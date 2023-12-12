import os,sys

from utils.FileManipulation import Piecify

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)


def start_server(ip, port):
    original = Piecify("./Mahabharat.pdf")
    chunk_map = original.generate_chunk_map()
    print(original.chunk_map)

    copy = Piecify("./Mahabharat_copy.pdf", original.piece_size)

    for index in range(731):
        if(index == 727):
            continue
        try:
            sample_piece = original.read_piece(index)
            copy.write_piece(index, sample_piece)
            print(f"Piece {index} copied successfully.")
        except Exception as e:
            print(f"Error copying piece {index}: {e}")

    
    sample_piece = original.read_piece(727)
    copy.write_piece(727, sample_piece)
    print(f"Piece {727} copied successfully.")

    
if __name__ == "__main__":
    server_ip = "127.0.0.1"
    server_port = 6881
    start_server(server_ip, server_port)