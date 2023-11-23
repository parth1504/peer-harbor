import socket

import socket

def receive_file(conn, file_path):
    with open(file_path, 'wb') as file:
        chunk_size = 10
        data = conn.recv(chunk_size)

        while data:
            file.write(data)
            data = conn.recv(chunk_size)



def start_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)  # Listen for one incoming connection

    print(f"Waiting for incoming connection on {ip}:{port}")
    client_socket, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")

    # Receive and print messages
    #while True:
    receive_file(client_socket,"D:/backend/p2p/peer-harbor/temp.md")
        # data = client_socket.recv(1024)  # Adjust buffer size as needed
        # if not data:
        #     break  # Connection closed by the client
        # print(f"Received message: {data.decode()}")

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    # Adjust the IP and port to match the server's configuration
    server_ip = "127.0.0.1"
    server_port = 6881

    start_server(server_ip, server_port)
