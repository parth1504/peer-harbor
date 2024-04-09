import os,sys

from utils.FileManipulation import Piecify

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)
    
if __name__ == "__main__":
    server_ip = "127.0.0.1"
    server_port = 6881