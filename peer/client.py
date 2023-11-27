import hashlib
import json
import struct
import sys,os
from os.path import abspath, dirname

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from utils.manipulation import write_file_from_pieces
from strategies.pieceSelectionAlgorithm import ClientInfo
from connection.peer import PeerConnection
from download.Leech import receive_pieces

client = PeerConnection("127.0.0.1",6881)
client_socket = client.leecher_connection()
data = receive_pieces(client_socket)
write_file_from_pieces(data[1],'./result.torrent')
client_socket.close()