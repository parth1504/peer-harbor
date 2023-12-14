import json
import socket
import threading
import time
import requests
from server import create_app
from flask import Blueprint, request, jsonify
from server.redisServer import RedisInstance

app = create_app()


peerset=["random_info_hash"]

new_rarity_arrays= {}
 
rarity_arrays = {
    "random_info_hash": [[1,9,2,1,1]],
}      

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
    #data_to_broadcast = {"new rarity array": normalized_values }
    print(index_sums)
    # Broadcast the calculated data using UDP
    return normalized_values

def refresh_periodically():
    while True:
        print("refreshing periodically!!")
        time.sleep(15)  

        for info_hash in peerset:
            print(info_hash)
            normalized_values= calculate_and_broadcast(info_hash)
            print("normalized values:" ,normalized_values)
            new_rarity_arrays[info_hash]=normalized_values
# Start the refresh_periodically function in a separate thread
refresh_thread = threading.Thread(target=refresh_periodically, daemon=True)
refresh_thread.start()

# Endpoint for peers to send their info_hash
@app.route('/send_info_hash', methods=['POST'])
def send_info_hash():
    try:
        data = request.json
        rarity_array = data.get('rarity_array')
        info_hash = data.get('info_hash')
        if info_hash not in new_rarity_arrays.keys():
            rarity_arrays[info_hash] = []
            new_rarity_array=rarity_array
            new_rarity_arrays[info_hash]=new_rarity_array
        else: 
            new_rarity_array=new_rarity_arrays[info_hash]

        rarity_arrays[info_hash].append(rarity_array)
        print(f"Received info_hash: {info_hash}")
        return jsonify({'success': True, 'new_rarity_array': new_rarity_array})
    except Exception as e:
        print(f"Error processing info_hash: {e}")
        return jsonify({'success': False, 'error': str(e)})
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=6969)