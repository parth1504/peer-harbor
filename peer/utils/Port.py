import socket

def find_free_port():
    """
    Find an available port on the local machine.
    """
    
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_socket.bind(('localhost', 0))
    _, port = temp_socket.getsockname()
    temp_socket.close()
    return port