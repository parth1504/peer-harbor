import socket
import requests, time, threading
from flask import Flask, request, jsonify

server_address = "http://127.0.0.1:6969"

# Function to periodically send info_hash to the server
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

rarity_arrays = {
    "random_info_hash": [[1,1,1,1,5],[2,1,4,5,6],[1,4,5,1,7]],
}

# Function to periodically send info_hash to the server
def send_rarity_array_periodically(info_hash):
    while True:

        time.sleep(15)  # 15 minutes interval
        try:
            for array in rarity_arrays[info_hash]:
                print("sent")
                requests.post(f"{server_address}/send_info_hash", json={"info_hash":info_hash ,"rarity_array": array})
        except requests.RequestException as e:
            print(f"Error sending info_hash to server: {e}")

# Function to receive UDP messages
def receive_udp_messages():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.bind((UDP_IP, UDP_PORT))
        while True:
            try:
                data, addr = client_socket.recvfrom(1024)
                decoded_data = data.decode('utf-8')
                print(f"Received UDP message: {decoded_data}")
            except Exception as e:
                print(f"Error receiving UDP message: {e}")

# Replace 'your_info_hash' with the actual info_hash for each peer
send_info_hash_thread = threading.Thread(target=send_rarity_array_periodically, args=('random_info_hash',), daemon=True)
send_info_hash_thread.start()

udp_receive_thread = threading.Thread(target=receive_udp_messages, daemon=True)
udp_receive_thread.start()



def get_peer_list(tracker_url, info_hash, peer_id, ip, port, uploaded, downloaded, left, compact=0):
    # Build the request URL with all parameters
    request_url = (
        f"{tracker_url}?info_hash={info_hash}&peer_id={peer_id}&ip={ip}&port={port}"
        f"&uploaded={uploaded}&downloaded={downloaded}&left={left}&compact={compact}"
    )

    # Make the HTTP GET request to the tracker
    response = requests.get(request_url)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Parse the response content to get the peer list
        peer_list = response.content
        return peer_list
    else:
        print(f"Error: Unable to get peer list. Status Code: {response.status_code}")
        return None
    
while True:
    time.sleep(1)