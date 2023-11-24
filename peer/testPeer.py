import json
import socket

def receive_file(conn, file_path):
    with open(file_path, 'wb') as file:
        chunk_size = 10
        data = conn.recv(chunk_size)
        while data:
            file.write(data)
            data = conn.recv(chunk_size)

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

def start_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)  # Listen for one incoming connection

    print(f"Waiting for incoming connection on {ip}:{port}")
    client_socket, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")
    # Receive and print messages
    #receive_file(client_socket,"D:/backend/p2p/peer-harbor/temp.md")
    p=[0]*6
    send_bitset(client_socket,p)
    bitset=receive_bitset(client_socket)
    print(bitset)
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    # Adjust the IP and port to match the server's configuration
    server_ip = "127.0.0.1"
    server_port = 6881

    start_server(server_ip, server_port)
