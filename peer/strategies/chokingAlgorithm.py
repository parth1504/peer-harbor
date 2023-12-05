import threading
import requests
import time

class PeerSelection:
    def __init__(self, announce_url, info_hash):
        self.announce_url = announce_url
        self.info_hash = info_hash

    def get_info_from_tracker(self, tracker_url, info_hash):
        params = {
            'info_hash': info_hash
        }

        response = requests.get(tracker_url, params=params)

        if response.status_code == 200:
            tracker_response = response.json()
            peers_info = tracker_response.get('peers', [])
            peers_data = [{'ip': peer['ip'], 'port': peer['port']} for peer in peers_info]
            return peers_data
        else:
            print(f"Error getting info from tracker. Status Code: {response.status_code}")
            print(f"Error details: {response.text}")
            return None