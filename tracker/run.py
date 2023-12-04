import json
import socket
import threading
import time
import requests
from server import create_app
from flask import Blueprint, request, jsonify

app = create_app()
rarity_arrays = {}

peerset = set("temp")  # Assuming you have a set of peers



UDP_IP = "127.0.0.1"
UDP_PORT = 5005

def broadcast_udp_message(info_hash, message):
    params = {
            'info_hash': info_hash,
      
    }
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        print("sending")
        server_socket.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))

def normalize_values(values):
    # Normalize values between 1 and 10
    min_value = min(values)
    max_value = max(values)

    if min_value == max_value:
        # Handle the case where all values are the same
        normalized_values = [5] * len(values)
    else:
        normalized_values = [(value - min_value) / (max_value - min_value) * 9 + 1 for value in values]

    return normalized_values

def calculate_and_broadcast(info_hash):
    # Calculate the data or perform any desired logic
    index_sums = [sum(array[index] for array in rarity_arrays[info_hash]) for index in range(len(rarity_arrays[info_hash][0]))]
    normalized_values = normalize_values(index_sums)
    data_to_broadcast = {"new rarity array": normalized_values }

    # Broadcast the calculated data using UDP
    broadcast_udp_message(info_hash, json.dumps(data_to_broadcast))

def refresh_periodically():
    while True:
        time.sleep(15)  # 15 minutes interval

        for info_hash in peerset:
            calculate_and_broadcast(info_hash)

# Start the refresh_periodically function in a separate thread
refresh_thread = threading.Thread(target=refresh_periodically, daemon=True)
refresh_thread.start()

# Endpoint for peers to send their info_hash
@app.route('/send_info_hash', methods=['POST'])
def send_info_hash():
    try:
        data = request.json
        info_hash = data.get('info_hash')
        rarity_array = data.get('rarity_array')
        if info_hash not in rarity_arrays:
            rarity_arrays[info_hash] = []
        rarity_arrays[info_hash].append(rarity_array)
        print(f"Received info_hash: {info_hash}")
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error processing info_hash: {e}")
        return jsonify({'success': False, 'error': str(e)})
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=6969)