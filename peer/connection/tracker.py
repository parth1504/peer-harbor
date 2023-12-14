import socket
import requests, time, threading
from flask import Flask, request, jsonify

server_address = "http://127.0.0.1:6969"

rarity_arrays = {
    "random_info_hash": [[5,1,1,1,5],[2,8,4,5,6],[1,4,12,1,7]],
}
class TrackerThread:
    def __init__(self,rarity_tracker):
        self.rarity_tracker=rarity_tracker
        self.rarity_array= rarity_tracker.piece_metrics
        self.info_hash= rarity_tracker.info_hash
        

    def send_rarity_array_periodically(self):
        while True:

            #time.sleep(15)  # 15 minutes interval
            try:
                print("sent")
                response= requests.post(f"{server_address}/send_info_hash", json={"info_hash":self.info_hash ,"rarity_array":self.rarity_array})
                data = response.json()
                new_array=data['new_rarity_array']
                self.rarity_tracker.refresh(new_array)
            except requests.RequestException as e:
                print(f"Error sending info_hash to server: {e}")



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
    